# coding:utf-8
import sys

import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cam',help="input the digital number",type=int)
args = parser.parse_args()
cam_id = args.cam

url = []
url.append("rtsp://linye:linye123@192.168.200.253:554/Streaming/Channels/101")
url.append("rtsp://linye:linye123@192.168.200.253:554/Streaming/Channels/301")

cap = []
cap.append(cv2.VideoCapture(url[0]))
cap.append(cv2.VideoCapture(url[1]))

frame_cnt = 0

fourcc =  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
# 第三个参数则是镜头快慢的，20为正常，小于二十为慢镜头
out = []
out.append(cv2.VideoWriter('camera_0.avi', fourcc,20,(1280,720)))
out.append(cv2.VideoWriter('camera_1.avi', fourcc,20,(1280,720)))

flag_start = False
while True:
    ret0,frame0 = cap[0].read()
    ret1,frame1 = cap[1].read()
    if ret0 == True and ret1 == True:
        cv2.imshow("frame0", frame0)
        cv2.imshow("frame1", frame1)

        key = cv2.waitKey(1) & 0xFF
        if(key == ord("s")):
          flag_start = True
        if(key == ord("q")):
          break
        if(flag_start):
          out[0].write(frame0)
          out[1].write(frame1)
    else:
        break
# 释放摄像头资源
cap[0].release()
cap[1].release()
cv2.destroyAllWindows()
