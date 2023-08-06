# -*- coding: utf-8 -*-
"""
Project: mySetup
Author: xwy
Time: 2022/9/11 10:29
Python: python3.10
"""

import cv2
import numpy as np

from easyrv.MvImport.CameraParams_header import *
from easyrv.MvImport.MvCameraControl_class import *
from easyrv.MvImport.MvErrorDefine_const import *


# ch: 枚举设备 | en:Enum device
def enum_device(def_tlayer_type, def_device_list):
    ret = MvCamera.MV_CC_EnumDevices(def_tlayer_type, def_device_list)
    if ret != 0:
        print("enum devices fail! ret[0x%x]" % ret)

    if def_device_list.nDeviceNum == 0:
        print("find no device!")

    print("查询到 %d 台相机!" % def_device_list.nDeviceNum)

    cam_ip = []
    for i in range(0, def_device_list.nDeviceNum):
        mvcc_dev_info = cast(def_device_list.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            # 输出设备名字
            str_mode_name = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                if per != 0:
                    str_mode_name = str_mode_name + chr(per)
            # 输出设备ID
            nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            print("相机名称: %s" % str_mode_name,
                  "IP地址 Gige-" + str(i) + ":" + str(nip1) + "." + str(nip2) + "." + str(nip3) + "." + str(nip4))
            cam_ip.append(str(nip1) + "." + str(nip2) + "." + str(nip3) + "." + str(nip4))
    return cam_ip


class HkVideoCapture:
    def __init__(self, n_connection_num, def_device_list, color_set=cv2.COLOR_BAYER_BG2BGR):
        self.image = None
        self._nConnectionNum = n_connection_num
        self._cam = None
        self._data_buf = None
        self._nPayloadSize = None
        self.def_deviceList = def_device_list
        self._color_set = color_set

    def enable_device(self, reverse_y=False):
        """
        设备使能
        """
        # ch:创建相机实例 | en:Creat Camera Object
        self._cam = MvCamera()

        # ch:选择设备并创建句柄 | en:Select device and create handle
        # cast(typ, val)，这个函数是为了检查val变量是typ类型的，但是这个cast函数不做检查，直接返回val
        st_device_list = cast(self.def_deviceList.pDeviceInfo[int(self._nConnectionNum)],
                              POINTER(MV_CC_DEVICE_INFO)).contents

        ret = self._cam.MV_CC_CreateHandle(st_device_list)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)

        # ch:打开设备 | en:Open device
        ret = self._cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != MV_OK:
            print("open device fail! ret[0x%x]" % ret)

        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if st_device_list.nTLayerType == MV_GIGE_DEVICE:
            n_packet_size = self._cam.MV_CC_GetOptimalPacketSize()
            if int(n_packet_size) > 0:
                ret = self._cam.MV_CC_SetIntValue("GevSCPSPacketSize", n_packet_size)
                if ret != 0:
                    print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print("Warning: Get Packet Size fail! ret[0x%x]" % n_packet_size)

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = self._cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)

        ret = self._cam.MV_CC_SetBoolValue("ReverseY", reverse_y)

        # 从这开始，获取图片数据
        # ch:获取数据包大小 | en:Get payload size
        st_param = MVCC_INTVALUE()
        memset(byref(st_param), 0, sizeof(MVCC_INTVALUE))
        ret = self._cam.MV_CC_GetIntValue("PayloadSize", st_param)
        if ret != 0:
            print("get payload size fail! ret[0x%x]" % ret)

        self._nPayloadSize = st_param.nCurValue

        # ch:开始取流 | en:Start grab image
        ret = self._cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
        #  返回获取图像缓存区。
        self._data_buf = (c_ubyte * self._nPayloadSize)()
        #  date_buf前面的转化不用，不然报错，因为转了是浮点型

    def get_image(self, exposure_time=20000, frame_rate=60, reverse_x=False, reverse_y=False):
        # --------------- 设置曝光时间 和 缓冲区信息 -----------------------------------
        st_frame_info = MV_FRAME_OUT_INFO_EX()
        memset(byref(st_frame_info), 0, sizeof(st_frame_info))

        st_float_param_exposure_time = MVCC_FLOATVALUE()
        memset(byref(st_float_param_exposure_time), 0, sizeof(MVCC_FLOATVALUE))

        ret = self._cam.MV_CC_SetFloatValue("ExposureTime", float(exposure_time))
        ret = self._cam.MV_CC_SetFloatValue("AcquisitionFrameRate", float(frame_rate))
        ret = self._cam.MV_CC_SetBoolValue("ReverseX", reverse_x)
        ret = self._cam.MV_CC_SetBoolValue("ReverseY", reverse_y)

        # 采用超时机制获取一帧图片，SDK内部等待直到有数据时返回，成功返回0
        ret = self._cam.MV_CC_GetOneFrameTimeout(self._data_buf, self._nPayloadSize, st_frame_info, 1000)

        self.image = np.asarray(self._data_buf)  # 将c_ubyte_Array转化成ndarray得到（3686400，）
        self.image = self.image.reshape((st_frame_info.nHeight, st_frame_info.nWidth, -1))  # 根据自己分辨率进行转化
        self.image = cv2.cvtColor(self.image, self._color_set)
        return self.image

    def close_device(self):
        """
        关闭设备
        """
        # ch:停止取流 | en:Stop grab image
        ret = self._cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            del self._data_buf

        # ch:关闭设备 | Close device
        ret = self._cam.MV_CC_CloseDevice()
        if ret != 0:
            print("close deivce fail! ret[0x%x]" % ret)
            del self._data_buf

        # ch:销毁句柄 | Destroy handle
        ret = self._cam.MV_CC_DestroyHandle()
        if ret != 0:
            print("destroy handle fail! ret[0x%x]" % ret)
            del self._data_buf

        del self._data_buf
        print('设备%d停止！' % self._nConnectionNum)
