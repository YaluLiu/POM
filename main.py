# -*- coding: utf-8 -*-

import sys
import os
import math
import numpy as np
import torchvision
import pickle
import time

#from get_pom import get_pom_data,get_room_data
from utils import   genBackground_one
from generate_pom import get_pom_data,get_room_data
import parsepom

config_path = "./constant.txt"
cam_param_path = "./camera_parameter.pickle"

config_dict = {}
f = open(config_path)
for line in f.readlines():
    line = line.strip().split(" ")
    config_dict[line[0]] = line[1]
f.close()

with open(cam_param_path, 'rb') as fp:
    cam_param = pickle.load(fp)
cams_num = cam_param["P"].shape[0]

room_data = get_room_data(cams_num,config_dict)
pom_data = get_pom_data(cams_num,cam_param,config_dict)

# for line in pom_data:
#     if(len(line) < 3):
#         print(line)
#     elif(line[2] == "15" or line[2] == "16"):
#         print(line)

parsepom.update_room(room_data)
parsepom.update_room(pom_data)

print("UPDATE_POM")

#model of get mask
seg_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
seg_model = seg_model.cuda()
seg_model = seg_model.eval()

# get imgs path 
cam_imgs_root = ["./images/{}".format(str(cam_id)) for cam_id in range(cams_num)]
img_names = []
for cam_id in range(cams_num):
    imgs_one_cam = [os.path.join(cam_imgs_root[cam_id], img_name) for img_name in os.listdir(cam_imgs_root[cam_id])]
    img_names.append(imgs_one_cam)

frames_num = len(imgs_one_cam)

 
start  = time.clock()
for frame in range(frames_num):
    for cam in range(cams_num):
        #get mask
        img_path = img_names[cam][frame]
        png_data = genBackground_one(seg_model, img_path, score_thresh = 0.9, binary_thresh = 0.5, cuda=True)
        #update img under each camera by frame 
        parsepom.sendImg(cam,png_data)
    
    #compute the probabilty ndarray [(num_location), dytpe = np.float64]
    proba_presence = np.array(parsepom.solve(frame))

end = time.clock()
print("start:{},end:{}".format(str(start),str(end)))
print("Time of one frame:",(end - start)/(cams_num * frames_num))
print("Work Success!")
