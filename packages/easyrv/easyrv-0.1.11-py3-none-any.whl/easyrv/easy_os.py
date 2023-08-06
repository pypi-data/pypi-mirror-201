# -*- coding: utf-8 -*-
# 作者: xwy
# 时间: 2022/7/22 18:43
# 版本: python3.10
import ctypes
import inspect
import os
import pickle
import threading
import time


def make_dirs(path):
    """
    合并路径名
    基于 os.path.join() 若无则创建
    :param path:  文件夹、文件名列表 list []
    :return: 返回路径名
    """
    path_out = ''
    for folder in path:
        path_out = os.path.join(path_out, folder)

    if not os.path.exists(path_out):
        os.makedirs(path_out)
        print('文件夹{}创建成功'.format(path_out))
    return path_out


def save_variable(file_name, v):
    f = open(file_name, 'wb')
    pickle.dump(v, f)
    f.close()


def load_variable(file_name):
    ff = open(file_name, 'rb')
    r = pickle.load(ff)
    ff.close()
    return r


def thread_close(c_t):
    if c_t.is_alive():
        tid = ctypes.c_long(c_t.ident)
        exc_type = SystemExit
        if not inspect.isclass(SystemExit):
            exc_type = type(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


def thread_find():
    thread_l = []
    while True:
        # threading.enumerate(): 返回一个包含正在运行的线程的list，包含线程名称和标识id。
        thread_num = len(threading.enumerate())
        thread_l = threading.enumerate()
        print("线程数量是%d" % thread_num)
        print(threading.enumerate())
        if thread_num <= 1:
            break
        time.sleep(1)
    return thread_l
