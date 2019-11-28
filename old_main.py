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

# if use_student == False:
#     #model of get mask
#     seg_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
#     seg_model = seg_model.cuda()
#     seg_model = seg_model.eval()
# else:
#     import torch
#     #device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
#     #seg_model = TinyNet(device, 2).to(device)
#     seg_model = torch.load('student.pkl')

# get imgs path 

img_names = []
for cam_id in range(cam_num):
    cam_imgs_root = "{}/cam{}".format(dir_path,str(cam_id))
    imgs_one_cam = os.listdir(cam_imgs_root)
    imgs_one_cam.sort(key = lambda x:int(x.split('.')[0]))
    img_paths = [os.path.join( cam_imgs_root, img_name) for img_name in imgs_one_cam]
    img_names.append(img_paths)

frames_num = len(imgs_one_cam)
frames_num =  1600

print("Start to compute")


masks = np.load(masks_path) #(cam,frame,h,w,3)                                                                                                                                                                                              
#masks = masks.swapaxes(2,3) #(cam,frame,w,h,3)

#start  =                               time.clock                          () #240 
for frame in range(0,599):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    for cam in range(cam_num):
        #get mask
        # img_path = img_names[cam][frame]
        # print(img_path)
        #mask_data = genBackground_one(seg_model, img_path, score_thresh = 0.2, binary_thresh = 0.9, cuda=True,use_student = use_student)
        #mask_data (360,288,3)
        mask_data = masks[cam][frame]
        #update img under each camera by frame 
        parsepom.sendImg(cam,mask_data)
    
    #compute the probabilty ndarray [(num_location), dytpe = np.float64]
    proba_presence = np.array(parsepom.solve(frame))

#end = time.clock()
#print("start:{},end:{}".format(str(start),str(end)))
#print("Time of one frame:",(end - start)/(cam_num * frames_num))
print("Work Success!")

