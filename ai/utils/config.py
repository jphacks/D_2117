from box import Box
import os
import torch
import numpy as np
import random

def get_config():

    config = {
        'input':{
            'image_dir':'./input/kaggle_dogs'
        },
        'plot':'./plot',
        'seed':0,
        "transforms":{
            "size":(512, 512),
            "mean":(0.485, 0.456, 0.406),
            "std":(0.229, 0.224, 0.225),
        },
        'hparams':{
            'batch_size':16,
        },
    }
    config = Box(config)
    return config

def seed_torch(seed:int):
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

