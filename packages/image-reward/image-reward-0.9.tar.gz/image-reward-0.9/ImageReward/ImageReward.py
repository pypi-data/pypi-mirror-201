'''
@File       :   ImageReward.py
@Time       :   2023/04/05 19:18:00
@Auther     :   Jiazheng Xu
@Contact    :   xjz22@mails.tsinghua.edu.cn
* Based on CLIP code base
* https://github.com/openai/CLIP
'''

import hashlib
import os
import urllib
import warnings
from typing import Any, Union, List
from .model import ImageReward
import torch
from tqdm import tqdm
from huggingface_hub import hf_hub_download

_MODELS = {
    "ImageReward-v1": "https://huggingface.co/THUDM/ImageReward/blob/main/ImageReward.pt",
}


def _download(url: str, root: str):
    os.makedirs(root, exist_ok=True)
    filename = os.path.basename(url)
    download_target = os.path.join(root, filename)
    hf_hub_download(repo_id="THUDM/ImageReward", filename=filename, local_dir=root)
    return download_target


def available_models() -> List[str]:
    """Returns the names of available ImageReward models"""
    return list(_MODELS.keys())


def load(name: str = "ImageReward-v1", device: Union[str, torch.device] = "cuda" if torch.cuda.is_available() else "cpu", download_root: str = None):
    """Load a ImageReward model

    Parameters
    ----------
    name : str
        A model name listed by `ImageReward.available_models()`, or the path to a model checkpoint containing the state_dict

    device : Union[str, torch.device]
        The device to put the loaded model

    download_root: str
        path to download the model files; by default, it uses "~/.cache/ImageReward"

    Returns
    -------
    model : torch.nn.Module
        The ImageReward model
    """
    if name in _MODELS:
        model_path = _download(_MODELS[name], download_root or os.path.expanduser("~/.cache/ImageReward"))
    elif os.path.isfile(name):
        model_path = name
    else:
        raise RuntimeError(f"Model {name} not found; available models = {available_models()}")

    print('load checkpoint from %s'%model_path)
    state_dict = torch.load(model_path, map_location='cpu')
    
    # med_config
    med_config = _download("https://huggingface.co/THUDM/ImageReward/blob/main/med_config.json", download_root or os.path.expanduser("~/.cache/ImageReward"))
    
    model = ImageReward(device=device, med_config=med_config).to(device)
    msg = model.load_state_dict(state_dict,strict=False)
    print("checkpoint loaded")
    model.eval()

    return model