import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
from albumentations import (
    HorizontalFlip, VerticalFlip, IAAPerspective, ShiftScaleRotate, CLAHE, RandomRotate90,
    Transpose, ShiftScaleRotate, Blur, OpticalDistortion, GridDistortion, HueSaturationValue,
    IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, MedianBlur, IAAPiecewiseAffine, RandomResizedCrop,
    IAASharpen, IAAEmboss, RandomBrightnessContrast, Flip, OneOf, Compose, Normalize, Cutout, CoarseDropout,
    ShiftScaleRotate, CenterCrop, Resize
)
from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt


def detect_leaf(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # find the brown color
    mask_brown = cv2.inRange(hsv, (8, 60, 20), (30, 255, 200))
    # find the yellow and green color in the leaf
    mask_yellow_green = cv2.inRange(hsv, (10, 39, 64), (86, 255, 255))
    # find any of the three colors(green or brown or yellow) in the image
    mask = cv2.bitwise_or(mask_yellow_green, mask_brown)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)
    return res

SEED = 1234

DATA_PATH = "../input/cassava-leaf-disease-classification/"
# Where the imgaes/audio are stored
FILE_PATH = "../input/cassava-leaf-disease-classification/train_images/"
TRAIN_DF_FILE = 'train.csv'
TARGET_COL = 'label'
ID_COL = 'image_id'
# For predictions
TEST_FILE_PATH = "../input/cassava-leaf-disease-classification/test_images/"


def resize(image, size=None):
    if size is not None:
        h, w, _ = image.shape
        new_w, new_h = int(w * size / h), size
        image = cv2.resize(image, (new_w, new_h))

    return image


def normalize(image, mean=None, std=None):
    image = image / 255.0
    if mean is not None and std is not None:
        image = (image - mean) / std
    #return np.moveaxis(image, 2, 0).astype(np.float32)
    return image.astype(np.float32)

    

# Data loader
class CustomDataset(Dataset):
    def __init__(self, df, file_path, train=True, transforms=None):
        self.train = train
        self.df = df
        self.file_path = file_path
        self.filename = df[ID_COL].values
        self.transforms = transforms
        if self.train:
            self.y = df[TARGET_COL]

    def __len__(self):
        return len(self.filename)

    def __getitem__(self, idx: int):
        # Return audio and sampling rate
        file = self.file_path + self.filename[idx]
        image = cv2.imread(file)
        orig_image = image.copy()

        # Special user defined mask
        if Config.cv_mask:
            image = detect_leaf(image)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Normalize if no augmentation. Test set also needs this
        if not self.transforms:
            image = cv2.resize(image, dsize=(Config.img_size, Config.img_size), interpolation=cv2.INTER_LINEAR)
            image = normalize(image, mean=None, std=None)
        # Augment
        else:
            #image = cv2.resize(image, dsize=(Config.img_size, Config.img_size), interpolation=cv2.INTER_LINEAR)
            #image = normalize(image, mean=None, std=None)
            image = self.transforms(image=image)['image']

        # Uncomment to switch channel to first dimension if image shape is H x W x C
        # image = np.transpose(image, axes=[2,0,1])

        # Return image and raw data
        if self.train:
            return image, ONE_HOT[self.df[TARGET_COL][idx]]
        elif Config.test_loader:
            return image, orig_image
        else:
            return image
# Test the data loader and augments
def test_loader(df, samples):
    train_df = df.sample(n=samples)
    if Config.augment:
        dataset = CustomDataset(df=train_df, file_path=FILE_PATH, train=False, transforms=get_sample_transforms())
    else:
        dataset = CustomDataset(df=train_df, file_path=FILE_PATH, train=False)
    data_loader = DataLoader(
        dataset,
        batch_size=samples,
        shuffle=True,
        drop_last=False,
        pin_memory=True,
        num_workers=NUM_WORKERS,
    )

    for images, orig_images in (data_loader):
        for i in range(len(images)):
            img = images[i]
            orig_image = orig_images[i]
            plt.figure(figsize=(40, 20))

            plt.subplot(1, 2, 1)
            plt.imshow(orig_image)
            
            plt.subplot(1, 2, 2)
            plt.imshow(img)
            plt.show()
def get_sample_transforms():
    return Compose([
        # Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], max_pixel_value=255.0, p=1.0),
        RandomResizedCrop(Config.aug_img_size, Config.aug_img_size, p=1),
        HorizontalFlip(p=0.5),
        # VerticalFlip(p=0.5),
        #RandomRotate90(p=0.5),
        # Transpose(p=0.5),
        # ShiftScaleRotate(p=0.5),
        # HueSaturationValue(hue_shift_limit=0.2, sat_shift_limit=0.2, val_shift_limit=0.2, p=0.5),
        # RandomBrightnessContrast(brightness_limit=(-0.1, 0.1), contrast_limit=(-0.1, 0.1), p=0.5),
        # CoarseDropout(p=0.5),
        # Cutout(p=0.5),
        ToTensorV2(p=1.0),
    ], p=1.)

NUM_WORKERS = 4

class Config:
    augment = False
    # Value to resize to
    img_size = 512
    aug_img_size = 512
    cv_mask = True
    test_loader = True
train_df_path = os.path.join(DATA_PATH, TRAIN_DF_FILE)
train_df = pd.read_csv(train_df_path)

test_loader(train_df,2 )