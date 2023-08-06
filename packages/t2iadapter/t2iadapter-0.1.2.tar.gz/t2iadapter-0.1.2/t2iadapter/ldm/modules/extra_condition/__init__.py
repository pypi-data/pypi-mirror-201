# -*- coding: utf-8 -*-
import torch
from .midas import *
from .openpose import *

from t2iadapter.ldm.modules.extra_condition.utils import load_file_from_url
from t2iadapter.ldm.modules.extra_condition.model_edge import pidinet
import mmcv
from mmdet.apis import init_detector
from mmpose.apis import init_pose_model
from t2iadapter.ldm.modules.extra_condition.midas.api import MiDaSInference
from transformers import CLIPProcessor, CLIPVisionModel
from t2iadapter.ldm.modules.extra_condition.openpose.api import OpenposeInference


def init_sketch_model(model_name, device='cuda'):
    if model_name == 'pidinet':

        # "pidinet"
        model = pidinet()
        model_url = 'https://huggingface.co/TencentARC/T2I-Adapter/blob/main/third-party-models/table5_pidinet.pth'
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    model_path = load_file_from_url(url=model_url, model_dir='~/.cache/t2iadapter', file_name=None)
    state_dict = torch.load(model_path, map_location='cpu')['state_dict']
    model.load_state_dict({k.replace('module.', ''): v for k, v in state_dict.items()}, strict=True)
    model.eval()
    model = model.to(device)
    return model


def init_keypose_model(model_name, device='cuda'):
    if model_name == 'mmpose':

        # "mmpose"
        det_config = 'configs/mm/faster_rcnn_r50_fpn_coco.py'
        det_url = 'https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'
        pose_config = 'configs/mm/hrnet_w48_coco_256x192.py'
        pose_url = 'https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'
        det_config_mmcv = mmcv.Config.fromfile(det_config)
        pose_config_mmcv = mmcv.Config.fromfile(pose_config)

    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    pose_model_path = load_file_from_url(
        url=pose_url, model_dir='/root/.cache/t2iadapter', progress=True, file_name=None)
    pose_model = init_pose_model(pose_config_mmcv, pose_model_path, device=device)
    det_model_path = load_file_from_url(url=det_url, model_dir='~/.cache/t2iadapter', progress=True, file_name=None)
    det_model = init_detector(det_config_mmcv, det_model_path, device=device)

    model = {'pose_model': pose_model, 'det_model': det_model}
    return model


def init_depth_model(model_name, device='cuda'):
    if model_name == 'midas':

        # "midas"
        model = MiDaSInference(model_type='dpt_hybrid')
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    model.eval()
    model = model.to(device)
    return model


def init_zoedepth_model(model_name, device='cuda'):
    if model_name == 'zoedepth':

        # "zoedepth"
        from handyinfer.depth_estimation import init_depth_estimation_model
        model = init_depth_estimation_model('ZoeD_N', device=device, model_rootpath='/root/.cache/t2iadapter')
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    model.eval()
    model = model.to(device)
    return model


def init_style_model(model_name, device='cuda'):
    if model_name == 'clip-vit-large':

        # "clip-vit-large"
        version = '/root/.cache/t2iadapter/openai/clip-vit-large-patch14'
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    processor = CLIPProcessor.from_pretrained(version)
    clip_vision_model = CLIPVisionModel.from_pretrained(version)
    clip_vision_model = clip_vision_model.to(device)
    model = {'processor': processor, 'clip_vision_model': clip_vision_model}
    return model


def init_openpose_model(model_name, device='cuda'):
    if model_name == 'openpose':

        # "openpose"
        model = OpenposeInference()
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')
    model.eval()
    model = model.to(device)
    return model