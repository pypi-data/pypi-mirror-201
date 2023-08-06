# -*- coding: utf-8 -*-
"""
@Time: 2023/3/2 14:16
@Auth: 除以七  ➗7️⃣
@File: cv.py
@E-mail: divided.by.07@gmail.com
@Github: https://github.com/divided-by-7
@info: None
"""
import cv2
from tqdm import tqdm
import os


def batch_resize(dir,save_dir,w_rate=1.,h_rate=1.):
    """
    目前只支持jpg、png
    :param dir:输入图片的路径
    :param save_dir: 保存路径
    :param w_rate: 宽度缩放比例
    :param h_rate: 高度缩放比例
    :return: 图像批量resize并保存到save_dir中
    """
    #--------------------------------------------------------------------------
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    tqdm_bar = tqdm(os.listdir(dir))
    for img_file_name in tqdm_bar:
        tqdm_bar.set_description("正在批量resize "+"将路径\t{}\t下图片缩放后保存在路径\t{}\t图像宽放大{}倍，高放大{}倍".format(dir,save_dir,w_rate,h_rate))
        img_dir = dir + "/" + img_file_name
        if ".png" in img_dir or ".jpg" in img_dir:
            img = cv2.imread(img_dir)
            h,w,c = img.shape
            scale_img = cv2.resize(img,(int(w*w_rate),int(h*h_rate)))
            # 保存图片
            cv2.imwrite(save_dir+"/"+img_file_name,scale_img)
    print("已将路径\t{}\t下图片缩放后保存在路径\t{}\n图像宽放大{}倍，高放大{}倍".format(dir,save_dir,w_rate,h_rate))
