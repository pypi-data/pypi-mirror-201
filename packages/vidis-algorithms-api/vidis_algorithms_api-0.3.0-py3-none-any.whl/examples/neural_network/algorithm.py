import torch
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from vidis_algorithms_api import Task

import json

from model.model import *


INPUT_DIM = 17
OUTPUT_DIM = 16
pallete = sns.color_palette("flare", n_colors=16)
pca_explained_variance = np.load(f'data/kfold0_PcaExplainedVariance_.npy')
pca_mean = np.load(f'data/kfold0_PcaMean.npy')
pca_components = np.load(f'data/kfold0_PcaComponents.npy')
DATA_STANDARTIZATION_PARAMS_PATH = f'data/data_standartization_params_kfold0.json'
with open(DATA_STANDARTIZATION_PARAMS_PATH, 'r') as f:
    DATA_STANDARTIZATION_PARAMS = json.load(f)


def pca_transformation(x):
    if len(x.shape) == 3:
        x_t = x.reshape((x.shape[0], -1)) # (C, H, W) -> (C, H * W)
        x_t = np.transpose(x_t, (1, 0)) # (C, H * W) -> (H * W, C)
        x_t = x_t - pca_mean
        x_t = np.dot(x_t, pca_components.T) / np.sqrt(pca_explained_variance)
        return x_t.reshape((x.shape[1], x.shape[2], pca_components.shape[0])).astype(np.float32, copy=False) # (H, W, N)
    elif len(x.shape) == 4:
        # x - (N, C, H, W)
        x_t = np.transpose(x, (0, 2, 3, 1)) # (N, C, H, W) -> (N, H, W, C)
        x_t = x_t - pca_mean
        x_t = np.dot(x_t, pca_components.T) / np.sqrt(pca_explained_variance)
        x_t = np.transpose(x_t, (0, -1, 1, 2)) # (N, H, W, C) -> (N, C, H, W)
        return x_t.astype(np.float32, copy=False)
    else:
        raise ValueError(f"Unknown shape={x.shape}, must be of len 3 or 4.")
        
        
def standartization(img, mean, std):
    img -= mean
    img /= std
    return img

def standartization_pool(mean, std):
    # X shape - (N, C, H, W)
    # from shape (comp,) -> (1, comp, 1, 1)
    mean = np.expand_dims(np.expand_dims(np.array(mean, dtype=np.float32), axis=-1), axis=-1)
    std = np.expand_dims(np.expand_dims(np.array(std, dtype=np.float32), axis=-1), axis=-1)
    
    return lambda x: standartization(x, mean=mean, std=std)


def preprocessing(hsi, mask):
    mean, std = (
        DATA_STANDARTIZATION_PARAMS.get('means'), 
        DATA_STANDARTIZATION_PARAMS.get('stds')
    )
    assert mean is not None and std is not None
    hsi = np.asarray(hsi, dtype=np.float32)
    hsi = pca_transformation(hsi)
    hsi = standartization(hsi, mean, std)
    return hsi, mask


def predict(hsi):
    hsi = preprocessing(hsi, None)[0]
    hsi = np.expand_dims(hsi, 0)
    hsi = np.transpose(hsi, [0, 3, 1, 2])

    with torch.no_grad():
        preds = model(torch.from_numpy(hsi))

    pred = nn.functional.softmax(preds, dim=1).numpy()
    pred = np.transpose(pred, [0, 2, 3, 1])
    pred = np.argmax(pred, axis=-1)[0]
    return pred


def make_seg_map(pred):
    seg_map = np.zeros((*pred.shape, 3), dtype=np.float32)

    for i in range(OUTPUT_DIM):
        seg_map[pred == i] = np.array(pallete[i][::-1]) * 255
    return cv2.cvtColor(seg_map.astype(np.uint8), cv2.COLOR_RGB2GRAY)


class Algorithm(Task):
    def run(self, hyperspecter: np.ndarray, **kwargs) -> np.ndarray:
        shape = hyperspecter.shape[1:]
        result = predict(hyperspecter)
        seg_map = make_seg_map(result)
        # NN always returns even shape
        seg_map = cv2.resize(seg_map, shape)
        return seg_map

    def get_type_name(self) -> str:
        return 'oursnet'


if __name__ == '__main__':
    net = MySuperNetLittleInput(INPUT_DIM, OUTPUT_DIM) 
    model = NnModel.load_from_checkpoint(
        'data/model-epoch=69-mean_iou=0.00.ckpt',
        loss=nn.CrossEntropyLoss(), model=net
    )
    net = model.model
    net.eval()
    alg = Algorithm()
    print(alg.get_type_name())
    alg.serve()
