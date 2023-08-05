#!/usr/bin/env python
# coding=utf-8
'''
brief        :  
Author       : knightdby knightdby@163.com
Date         : 2023-02-24 21:40:04
FilePath     : /wheel/manifast/manifast/iostream/imagestream.py
Description  : 
LastEditTime : 2023-02-24 23:22:16
LastEditors  : knightdby
Copyright (c) 2023 by Inc, All Rights Reserved.
'''


import os
import cv2
import numpy as np
from PIL import Image


def readImageFilebyCv(path):
    '''
    description: 读取图像数据
    param       {*} path 图像路径
    return      {*} 图像数据
    '''

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def readImagFilebyPillow(path):
    with open(path, "rb") as f:
        img = Image.open(f)
        return img.convert("RGB")


def plusImageMask(img, mask):
    """
     description: 将彩色图像与mask相叠加
     param       {*} img h*w*c
     param       {*} mask h*w
     return      {*} 叠加效果图
    """
    if mask.ndim == 3:
        mask = mask.squeeze()  # 去掉batch維度
    mask = mask.astype(np.uint8)
    display_mask = np.zeros_like(img)
    display_mask[mask == 1, 0] = 255
    masked = cv2.add(img, np.zeros(
        np.shape(img), dtype=np.uint8), mask=mask)
    masked = cv2.addWeighted(img, 0.5, display_mask, 0.5, 0)
    return masked
