#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import base64

from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex

import socket
import struct
import fcntl

'''
TODO: 
    使用密钥将MAC加密

USAGE:
    python CreateLicense.py 
'''

seperateKey = "HG.%*-*&@hfygyhuubj,mxzxcvgdrsiml,9946132376rdhkn8952;.lk!)i(^jcdxrgvl,mnbh/.?'""{}+*zxcflklm\lkp-786602jbzk';;ll[l,kpssmgfwwdfgd#~0^38J:"       # 随意输入一组字符串
aesKey = "3112006230547154"     # 加密与解密所使用的密钥，长度必须是16的倍数
aesIv = "1351602663171919"      # initial Vector,长度要与aesKey一致
aesMode = AES.MODE_CBC          # 使用CBC模式

class CreatLicense():
    def encrypt(self, text):
        #参考：https://www.cnblogs.com/loleina/p/8418108.html
        cryptor = AES.new(aesKey, aesMode, aesIv) 
        # # padding
        add, length = 0, 16
        count = len(text)
        if count % length != 0:
            add = length - (count % length)
        text = text + ('\0' * add)      # '\0'*add 表示add个空格,即填充add个直至符合16的倍数
        ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题  
        #所以这里统一把加密后的字符串转化为16进制字符串 ,当然也可以转换为base64加密的内容，可以使用b2a_base64(self.ciphertext)
        resr = b2a_hex(ciphertext).upper()
        resr = str(resr)
        return resr

    def getHwAddr(self, ifname): 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
        return ''.join(['%02x' % ord(char) for char in info[18:24]])

    def getLicense(self, mac_name): 
        hostInfo = self.getHwAddr(mac_name)   # hostInfo是运行此脚本时传入的mac地址
        encryptText = self.encrypt(hostInfo)     # 将mac地址第一次加密
        encryptText = encryptText + seperateKey + "Valid" 
        encryptText = self.encrypt(encryptText)  # 将加密之后的密文再次加密
    
        with open("./license.lic", "w+") as licFile:
            licFile.write(encryptText)
            licFile.close()
    
        print("生成license成功!")
