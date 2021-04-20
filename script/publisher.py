#!/usr/bin/env python
# coding:utf-8
###############################
# python代码加密与License控制例子
#    这是需要License控制的脚本
###############################
from decrypt import Get_License 
import time
import datetime

import rospy
from std_msgs.msg import Int32

class Today():
    def __init__(self):
        self.license = Get_License()
        self.condition, self.LicInfo = self.license.getLicenseInfo()

    def get_time(self):     
        if self.condition == True and self.LicInfo == 'Valid':
            print('test!')
            rospy.init_node('topic_publisher')
            pub = rospy.Publisher('counter', Int32)
            print(datetime.datetime.now())
            rate = rospy.Rate(2)
            count = 0
            while not rospy.is_shutdown():
                pub.publish(count)
                count += 1
                rate.sleep()
        else:
            print('未权授！')

    def say(self):
        if self.condition == True and self.LicInfo == 'Valid':
            print('hello world!')
            localtime = time.asctime( time.localtime(time.time()) )
            print("The local time is now:", localtime)
        else:
            print('未权授！')

