import torch.nn as nn
import torch
from torchvision import models
import numpy as np
import cv2

class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.segment_model = models.segmentation.fcn_resnet50(pretrained=True)
        sem_classes = [
            '__background__', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
            'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
            'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
        ]
        self.sem_class_to_idx = {cls: idx for (idx, cls) in enumerate(sem_classes)}
        self.class_dim = 1


        base_model = models.vgg19(pretrained=True)
        self.features = base_model.features
        self.avgpool = base_model.avgpool
        self.linear = base_model.classifier[0]

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _trimming_img(self, img, i):

        
        sum_x = np.sum(img, axis=1)
        sum_y = np.sum(img, axis=0)

        try:
            x_min = np.nonzero(sum_x)[0].min()
            x_max = np.nonzero(sum_x)[0].max()
            y_min = np.nonzero(sum_y)[0].min()
            y_max = np.nonzero(sum_y)[0].max()
        except ValueError:  # 真っ黒な画像(0, 0, 0)
            print(f"{i} : All Pixels are zeros.")
            x_min = y_min = 0
            x_max = img.shape[0]
            y_max = img.shape[1]

        # 犬を切り取る
        cropped_img = img[x_min:x_max, y_min:y_max, :]

        # 余白を追加して正方形に変更
        cropped_img_h, cropped_img_w = cropped_img[:,:,0].shape
        if cropped_img_h > cropped_img_w:
            add_pad = cropped_img_h - cropped_img_w
            top = bottom =  0
            left = add_pad // 2
            right = add_pad - left
        elif cropped_img_h < cropped_img_w:
            add_pad = cropped_img_w - cropped_img_h
            left = right =  0
            top = add_pad // 2
            bottom = add_pad - top
        else:
            left = right = top = bottom = 0
        square_img = cv2.copyMakeBorder(cropped_img, top, bottom, left, right, cv2.BORDER_CONSTANT, (0, 0, 0))
        square_img = cv2.resize(square_img,(512,512))
        square_img = square_img.transpose(2, 0, 1)


        return square_img
        
    def forward(self, img):
        orig_img = img
        
        # Segmentation Cut
        img = img.to(self.device)
        masks_out = self.segment_model(img)['out']
        normalized_masks = torch.nn.functional.softmax(masks_out, dim=1)
        boolean_dog_masks = (normalized_masks.argmax(self.class_dim) == self.sem_class_to_idx['dog'])

        masks_np = boolean_dog_masks.float().to('cpu').detach().numpy().copy()
        m3_list = [
            np.array([masks_np[i], masks_np[i], masks_np[i]]) \
            for i in range(masks_np.shape[0])
        ]
        m3_np = np.array(m3_list)
        img_np = img.float().to('cpu').detach().numpy().copy()
        cut_img_np = img_np * m3_np

        cut_trimed_img_np_list = [self._trimming_img(cut_img_np[i].transpose(1, 2, 0), i=i) for i in range(cut_img_np.shape[0])]
        cut_img_np = np.array(cut_trimed_img_np_list)


        img = torch.from_numpy(cut_img_np.astype(np.float32)).clone()
        
        # BaseModel get vector
        img = img.to(self.device)
        out = self.features(img)
        out = self.avgpool(out)
        out = out.view(out.shape[0], -1)
        out = self.linear(out)
        return out