# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
from torch.hub import download_url_to_file, get_dir
from urllib.parse import urlparse
import subprocess
import shlex

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

skeleton = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12], [5, 11], [6, 12], [5, 6], [5, 7], [6, 8], [7, 9], [8, 10],
            [1, 2], [0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6]]

pose_kpt_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], [0, 255, 0],
                  [255, 128, 0], [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0],
                  [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0]]

pose_link_color = [[0, 255, 0], [0, 255, 0], [255, 128, 0], [255, 128, 0],
                   [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], [0, 255, 0], [255, 128, 0],
                   [0, 255, 0], [255, 128, 0], [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255],
                   [51, 153, 255], [51, 153, 255], [51, 153, 255]]


def imshow_keypoints(img, pose_result, kpt_score_thr=0.1, radius=2, thickness=2):
    """Draw keypoints and links on an image.

    Args:
            img (ndarry): The image to draw poses on.
            pose_result (list[kpts]): The poses to draw. Each element kpts is
                a set of K keypoints as an Kx3 numpy.ndarray, where each
                keypoint is represented as x, y, score.
            kpt_score_thr (float, optional): Minimum score of keypoints
                to be shown. Default: 0.3.
            thickness (int): Thickness of lines.
    """

    img_h, img_w, _ = img.shape
    img = np.zeros(img.shape)

    for idx, kpts in enumerate(pose_result):
        if idx > 1:
            continue
        kpts = kpts['keypoints']
        # print(kpts)
        kpts = np.array(kpts, copy=False)

        # draw each point on image
        assert len(pose_kpt_color) == len(kpts)

        for kid, kpt in enumerate(kpts):
            x_coord, y_coord, kpt_score = int(kpt[0]), int(kpt[1]), kpt[2]

            if kpt_score < kpt_score_thr or pose_kpt_color[kid] is None:
                # skip the point that should not be drawn
                continue

            color = tuple(int(c) for c in pose_kpt_color[kid])
            cv2.circle(img, (int(x_coord), int(y_coord)), radius, color, -1)

        # draw links

        for sk_id, sk in enumerate(skeleton):
            pos1 = (int(kpts[sk[0], 0]), int(kpts[sk[0], 1]))
            pos2 = (int(kpts[sk[1], 0]), int(kpts[sk[1], 1]))

            if (pos1[0] <= 0 or pos1[0] >= img_w or pos1[1] <= 0 or pos1[1] >= img_h or pos2[0] <= 0 or pos2[0] >= img_w
                    or pos2[1] <= 0 or pos2[1] >= img_h or kpts[sk[0], 2] < kpt_score_thr
                    or kpts[sk[1], 2] < kpt_score_thr or pose_link_color[sk_id] is None):
                # skip the link that should not be drawn
                continue
            color = tuple(int(c) for c in pose_link_color[sk_id])
            cv2.line(img, pos1, pos2, color, thickness=thickness)

    return img


# def load_file_from_hf_url(url, model_dir=None, file_name=None):
#     """Ref:https://github.com/1adrianb/face-alignment/blob/master/face_alignment/utils.py
#     """
#     if model_dir is None:
#         hub_dir = get_dir()
#         model_dir = os.path.join(hub_dir, 'checkpoints')

#     os.makedirs(model_dir, exist_ok=True)

#     parts = urlparse(url)
#     filename = os.path.basename(parts.path)
#     if file_name is not None:
#         filename = file_name
#     cached_file = os.path.abspath(os.path.join(model_dir, filename))
#     if not os.path.exists(cached_file):
#         print(f'Downloading: "{url}" to {cached_file}\n')
#         subprocess.run(shlex.split(f'wget {url} -O {cached_file}'))
#     return cached_file


def load_file_from_url(url, model_dir=None, progress=True, file_name=None):
    """Ref:https://github.com/1adrianb/face-alignment/blob/master/face_alignment/utils.py
    """
    if model_dir is None:
        hub_dir = get_dir()
        model_dir = os.path.join(hub_dir, 'checkpoints')

    os.makedirs(model_dir, exist_ok=True)

    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    if file_name is not None:
        filename = file_name
    cached_file = os.path.abspath(os.path.join(model_dir, filename))
    if not os.path.exists(cached_file):
        print(f'Downloading: "{url}" to {cached_file}\n')
        download_url_to_file(url, cached_file, hash_prefix=None, progress=progress)
    return cached_file
