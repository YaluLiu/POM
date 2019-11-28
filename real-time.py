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

use_student = True
cam_num = 2
config_path = "./constant.txt"
cam_param_path = "./camera_parameter_merge.pickle"

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

parsepom.update_room(room_data)
parsepom.update_room(pom_data)
print("UPDATE_POM")  

if use_student == False:
    #model of get mask
    seg_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    seg_model = seg_model.cuda()
    seg_model = seg_model.eval()
else:
    import torch
    #device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    #seg_model = TinyNet(device, 2).to(device)
    seg_model = torch.load('student.pkl')

# get imgs path 
dir_path = "/media/yalu/6066C1DD66C1B3D6/images"
img_names = []
for cam_id in range(cam_num):
    cam_imgs_root = "{}/cam{}".format(dir_path,str(cam_id))
    imgs_one_cam = os.listdir(cam_imgs_root)
    imgs_one_cam.sort()
    img_paths = [os.path.join( cam_imgs_root, img_name) for img_name in imgs_one_cam]
    img_names.append(img_paths)

frames_num = len(imgs_one_cam)

print("Start to compute")
 
#start  = time.clock() #240 
for frame in range(frames_num):
    for cam in range(cam_num):
        #get mask
        img_path = img_names[cam][frame]
        print(img_path)
        png_data = genBackground_one(seg_model, img_path, score_thresh = 0.9, binary_thresh = 0.5, cuda=True,use_student = use_student)
        #update img under each camera by frame 
        parsepom.sendImg(cam,png_data)
    
    #compute the probabilty ndarray [(num_location), dytpe = np.float64]
    proba_presence = np.array(parsepom.solve(frame))

#end = time.clock()
#print("start:{},end:{}".format(str(start),str(end)))
#print("Time of one frame:",(end - start)/(cam_num * frames_num))
print("Work Success!")
