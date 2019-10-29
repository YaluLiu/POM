# coding:utf-8
import sys

import cv2
import numpy as np

cam_id = 0

url = []
url.append("rtsp://linye:linye123@192.168.200.253:554/Streaming/Channels/101")
url.append("rtsp://linye:linye123@192.168.200.253:554/Streaming/Channels/301")

cap = []
cap.append(cv2.VideoCapture(url[0]))
cap.append(cv2.VideoCapture(url[1]))

frame_cnt = 28
while True:
    ret0,frame0 = cap[0].read()
    ret1,frame1 = cap[1].read()
    if ret0 == True and ret1 == True:
        cv2.imshow("frame0", frame0)
        cv2.imshow("frame1", frame1)
        key = cv2.waitKey(1) & 0xFF
        if(key == ord("s")):
          frame_cnt+=1
          image_name = "./cam{}/{}.jpg".format(0,frame_cnt)
          cv2.imwrite(image_name,frame0)
          image_name = "./cam{}/{}.jpg".format(1,frame_cnt)
          cv2.imwrite(image_name,frame1)
          print("save {} frame".format(frame_cnt))
        if(key == ord("q")):
          break
    else:
        break
# 释放摄像头资源
cap[0].release()
cap[1].release()
cv2.destroyAllWindows()
