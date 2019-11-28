# -*- coding: utf-8 -*-
#  只使用mask和parse_pom模块.
import sys
import os
import math
import numpy as np
import pickle
import time

from generate_pom import get_pom_data,get_room_data
from utils import   genBackground_one
import parsepom
from studentnets import TinyNet

use_student = False
cam_num = 3
human_idx = 4

#dir_path = "/media/yalu/6066C1DD66C1B3D6/images/"
dir_path = "/media/yalu/6066C1DD66C1B3D6/images/my"
cam_param_path = "{}/camera_parameter.pickle".format(dir_path)
config_path = "{}/constants_{}.txt".format(dir_path,human_idx)
masks_path = "{}/masks.npy".format(dir_path)

config_dict = {}
f = open(config_path)
for line in f.readlines():
    line = line.strip().split(" ")
    config_dict[line[0]] = line[1]
f.close()
print(config_dict)

with open(cam_param_path, 'rb') as fp:
    cam_param = pickle.load(fp)

room_data = get_room_data(cam_num,config_dict)
pom_data = get_pom_data(cam_num,cam_param,config_dict,result_view_image = False)

parsepom.update_room(room_data)
parsepom.update_room(pom_data)
print("UPDATE_POM")  


print("Start to compute")


masks = np.load(masks_path) #(cam,frame,h,w,3)                                                                                                                                                                                              
#masks = masks.swapaxes(2,3) #(cam,frame,w,h,3)

for frame in range(0,500):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    for cam in range(cam_num):
        mask_data = masks[cam][frame]
        parsepom.sendImg(cam,mask_data) #mask_data(w,h,3)
    #compute the probabilty ndarray [(num_location), dytpe = np.float64]
    proba_presence = np.array(parsepom.solve(frame))
    npy_name = "./results/{}/proba-f{}.npy".format(human_idx,frame)
    np.save(npy_name,proba_presence)
    print("save {}".format(npy_name))
    
print("Work Success!")

