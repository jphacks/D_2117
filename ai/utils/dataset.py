import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

import os
from PIL import Image

class ImageTransform():
    """
    Class for image preprocessing.
    
    Attributes
    ----------
    resize : int
        224
    mean : (R, G, B)
        Average value for each color channel
    std : (R, G, B)
        Standard deviation for each color channel
    """
    
    def __init__(self, resize, mean, std):
        self.data_transform = {
            'train': transforms.Compose([
                #transforms.Resize(resize),
                #transforms.CenterCrop(resize),
                transforms.RandomResizedCrop(
                    resize, scale=(0.5, 1.0)),
                transforms.RandomHorizontalFlip(),
                #transforms.ColorJitter(),  # Randomly change brightness, contrast, saturation, and hue. 
                #transforms.RandomAffine(degrees=[-10, 10]),  # random affine transformations.
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ]),
            'val': transforms.Compose([
                #transforms.Resize(resize),
                transforms.CenterCrop(512),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ]),
            'test': transforms.Compose([
                transforms.Resize(resize),
                #transforms.CenterCrop(resize),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ]),
            'sub': transforms.Compose([
                transforms.Resize(resize),
                #transforms.CenterCrop(resize),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ])
        }
    
    def __call__(self, img, phase="train"):
        """
        Parameters
        ----------
        phase: 'train' or 'val' or 'test'
            Specify the mode of preprocessing
        """
        return self.data_transform[phase](img)


class CustomDataset(Dataset):
    def __init__(self, df, config, phase='test'):
        self.df = df
        self.config = config
        self.transform = ImageTransform(config.transforms.size, config.transforms.mean, config.transforms.std)
        self.phase = phase
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        # Image
        img_path = self.df.loc[idx, 'path']
        img = Image.open(img_path)
        img = self.transform(img, self.phase)

        # label
        label = torch.tensor(-1)

        # filename
        path = self.df.loc[idx, 'path']
        
        return img, label, path

