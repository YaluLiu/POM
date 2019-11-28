# -*- coding: utf-8 -*-

import sys
import os
import math
import numpy as np
import torchvision
import pickle
import time

from generate_pom import get_pom_data,get_room_data
from utils import   genBackground_one
import parsepom
from studentnets import TinyNet

use_student = False
cam_num = 3

#dir_path = "/media/yalu/6066C1DD66C1B3D6/images/"
dir_path = "/media/yalu/6066C1DD66C1B3D6/images/my"
cam_param_path = "{}/camera_parameter.pickle".format(dir_path)
config_path = "{}/constants.txt".format(dir_path)
masks_path = "{}/masks.npy".format(dir_path)
mask_rect_path = "{}/rects.npy".format(dir_path)

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
pom_data = get_pom_data(cam_num,cam_param,config_dict,result_view_image = True)

def parse_pom(pom_data):
    num_rects = int(len(pom_data)/cam_num)
    pom_rects = np.zeros((cam_num,num_rects,4),dtype=np.int32)
    for data in pom_data[:100]:
        cam_id = int(data[1])
        rect_id = int(data[2])
        if(data[3] == 'notvisible'):
            pom_rects[cam_id][rect_id] = np.zeros(4,dtype=np.int32)
        else:
            x1 = int(data[3])
            x2 = int(data[4])
            y1 = int(data[5])
            y2 = int(data[6])
            pom_rects[cam_id][rect_id] = np.array((x1,y1,x2,y2),dtype=np.int32)
    return pom_rects

pom_rects = parse_pom(pom_data)
mask_rects = np.load(mask_rect_path)

#判断两个矩形是否相交
def is_overlap(rect1, rect2):
    x1,y1,x2,y2 = rect1
    x3,y3,x4,y4 = rect2

    minx = max(x1 , x3)
    miny = max(y1 , y3)

    maxx = min(x2, x4)
    maxy = min(y2, y4)
    if minx > maxx and miny > maxy:
        return True
    return False

frame_idx = 1
num_rects = int(len(pom_data)/cam_num)

#pom_rects.shape (3,1369,4)
#mask_rects #(cam_id, frame_idx,10,4)
#results[frame][1369]

results = np.ones((500,1369),dtype=bool)

#对于固定的位置,固定的相机,从10个mask_rect中寻找是否有对应的
def find_mask():


#判断某个位置是否有人
def has_person(pom_rects,mask_rects,frame_idx,pos_idx,cam_num):
    for cam_id in range(3):
        pom_rect  = pom_rects[cam_id][pos_idx]
        if(find_mask)
        mask_rect = mask_rects[cam_id][frame_idx][0]
    return True


for frame_idx in range(100):
    for pos_idx in range(num_rects):
        results[frame_idx][pos_idx] = has_person()
        

for pos in range(num_rects):
    for cam_id in range(cam_num):
        if(pom_rects[cam_id][pos])
        if(not is_overlap(pom_rects)):
            results[frame_idx][pos] = False
            break

        
    




