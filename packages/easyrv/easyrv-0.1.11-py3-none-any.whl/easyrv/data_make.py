# -*- coding: utf-8 -*-
# 作者: xwy
# 时间: 2022/7/22 18:27
# 版本: python3.10
import math
import numpy as np


def gauss_heat_map(img_w, img_h, point_y, point_x, sigma):
    """
    绘制高斯热力图
    :param img_w: 图像宽
    :param img_h: 图像高
    :param point_y: X坐标
    :param point_x: Y坐标
    :param sigma: sigma
    :return: 热力图
    """
    heat_map = np.zeros((img_h, img_w), dtype=np.float32)

    for i in range(img_h):
        for j in range(img_w):
            e_pow = -((i - point_x) ** 2 + (j - point_y) ** 2) / (2 * sigma * sigma)
            heat_map[i, j] = math.exp(e_pow)

    return heat_map


def yolo_label_resize(input_label, input_shape):
    """
    把yolo的标签结果转换成正方形的
    :param input_label: yolo输出的标签
    :param input_shape: 图像原始形状
    :return: 转换后标签
    """
    def_img_h, def_img_w = input_shape[0], input_shape[1]
    def_x, def_y, def_w, def_h = def_img_w * input_label[1], def_img_h * input_label[2], \
                                 def_img_w * input_label[3], def_img_h * input_label[4]
    label_out = [input_label[0],
                 def_x / max(def_img_w, def_img_h),
                 def_y / max(def_img_w, def_img_h),
                 def_w / max(def_img_w, def_img_h),
                 def_h / max(def_img_w, def_img_h)]
    return label_out
