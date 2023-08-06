# -*- coding: utf-8 -*-
# 作者: xwy
# 时间: 2022/7/22 18:37
# 版本: python3.10
import math

import cv2
import numpy as np


def draw_collimation(image, point, length=5, color=(0, 255, 0), thickness=1):
    """
    画十字线
    :param image: 输入的图像
    :param point: 点坐标
    :param length: 线十字长度
    :param color: 线颜色
    :param thickness: 线粗
    :return: 画完的图像
    """
    img_out = image.copy()
    img_out = cv2.line(img_out, (point[0] - length, point[1]), (point[0] + length, point[1]), color, thickness)
    img_out = cv2.line(img_out, (point[0], point[1] - length), (point[0], point[1] + length), color, thickness)
    return img_out

