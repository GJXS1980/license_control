#!/usr/bin/env python
# coding:utf-8
###############################
# python代码加密与License控制例子
#    这是需要License控制的脚本
###############################
import socket, fcntl, datetime, os, struct
from Crypto.Cipher import AES 
from binascii import b2a_hex, a2b_hex 
import time

import rospy
from std_msgs.msg import Int32

import netifaces

class Get_License(object):
    def __init__(self):
        super(Get_License, self).__init__()
        
        # 定义秘钥信息
        self.seperateKey = "HG.%*-*&@hfygyhuubj,mxzxcvgdrsiml,9946132376rdhkn8952;.lk!)i(^jcdxrgvl,mnbh/.?'""{}+*zxcflklm\lkp-786602jbzk';;ll[l,kpssmgfwwdfgd#~0^38J:"
        self.aesKey = "3112006230547154"
        self.aesIv = "1351602663171919"
        self.aesMode = AES.MODE_CBC
        

    def getHwAddr(self, ifname):
        """
        获取主机物理地址
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
        return ''.join(['%02x' % ord(char) for char in info[18:24]])

    def decrypt(self, text):
        """
        从.lic中解密出主机地址
        """
        try:
            cryptor = AES.new(self.aesKey, self.aesMode, self.aesIv)
        
            plain_text = cryptor.decrypt(a2b_hex(text))
            return plain_text.rstrip('\0')
        except:
            return ""

    def interfaces_name(self):
        """
        解析出主机网卡接口名称
        """
        int_name = netifaces.interfaces()
        return int_name[1]
        
    def getLicenseInfo(self, filePath = None):
        int_name = self.interfaces_name()
        if filePath == None:
            filePath = "/usr/lib/license.lic"
        
        if not os.path.isfile(filePath):
            print("请联系工作人员获取激活license")
            os._exit(0)
            return False, 'Invalid'             
        
        encryptText = ""
        with open(filePath, "r") as licFile:
            encryptText = licFile.read()
            licFile.close()
        try:
            hostInfo = self.getHwAddr(int_name)
        except IOError:
            hostInfo = self.getHwAddr(int_name)
        
        decryptText = self.decrypt(encryptText)
        pos = decryptText.find(self.seperateKey)
        if -1 == pos:
            return False, "Invalid"
        licHostInfo = self.decrypt(decryptText[0:pos])
        licenseStr = decryptText[pos + len(self.seperateKey):]

        if licHostInfo == hostInfo:
            return True, licenseStr
        else:
            return False, 'Invalid'