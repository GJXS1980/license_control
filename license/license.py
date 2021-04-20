#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from CreateLicense import CreatLicense
import netifaces

#   获取网卡名称函数
def interfaces_name():
    int_name = netifaces.interfaces()
    return int_name[1]

#   获取网卡名称
int_name = interfaces_name()
#   实例化类
license = CreatLicense()
#   生成license
license.getLicense(int_name)
