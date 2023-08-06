# -*- coding: utf-8 -*-
# 作者: xwy
# 时间: 2022/7/22 18:54
# 版本: python3.10
import os
import shutil

import numpy as np
from tqdm import tqdm
from pathlib import Path
from easyrv.easy_os import make_dirs


def data_random_group(data_path, train_path, test_path, info_list, ratio):
    """
    对数据集进行分组，随机分组
    info_list说明：该变量为四个str数据组成的列表，对应下述hyp的变量。
                文件类型1的后缀名，文件类型2的后缀名，文件类型1的文件夹，文件类型2的文件夹
    hyp = {
    'suffix_1': 'jpg',
    'suffix_2': 'txt',
    'path_1': 'images',
    'path_2': 'labels'
    }
    :param data_path: 总数据的路径
    :param train_path: 训练数据路径
    :param test_path: 测试数据路径
    :param info_list: 详见上面
    :param ratio: 训练数据比重 0·1
    :return: 无
    """
    hyp = {
        'suffix_1': info_list[0],
        'suffix_2': info_list[1],
        'path_1': info_list[2],
        'path_2': info_list[3]
    }

    make_dirs([train_path, hyp['path_1']])
    make_dirs([train_path, hyp['path_2']])
    make_dirs([test_path, hyp['path_1']])
    make_dirs([test_path, hyp['path_2']])

    prefixes = []
    for file_name in tqdm(os.listdir(os.path.join(data_path, hyp['path_1']))):
        prefix = Path(str(file_name)).stem
        prefixes.append(prefix)

    prefixes_len = len(prefixes)

    move_num = []
    for i in tqdm(range(int(prefixes_len * (1 - ratio)))):
        move_num.append(int(np.random.uniform(0, prefixes_len - 1)))

    for num in tqdm(range(prefixes_len)):
        if num in move_num:
            shutil.copy(os.path.join(data_path, hyp['path_1'], str(prefixes[num]) + '.' + hyp['suffix_1']),
                        os.path.join(test_path, hyp['path_1'], str(prefixes[num]) + '.' + hyp['suffix_1']))
            shutil.copy(os.path.join(data_path, hyp['path_2'], str(prefixes[num]) + '.' + hyp['suffix_2']),
                        os.path.join(test_path, hyp['path_2'], str(prefixes[num]) + '.' + hyp['suffix_2']))
        else:
            shutil.copy(os.path.join(data_path, hyp['path_1'], str(prefixes[num]) + '.' + hyp['suffix_1']),
                        os.path.join(train_path, hyp['path_1'], str(prefixes[num]) + '.' + hyp['suffix_1']))
            shutil.copy(os.path.join(data_path, hyp['path_2'], str(prefixes[num]) + '.' + hyp['suffix_2']),
                        os.path.join(train_path, hyp['path_2'], str(prefixes[num]) + '.' + hyp['suffix_2']))
    print("完成！")
