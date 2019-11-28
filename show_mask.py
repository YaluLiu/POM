# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os 
import PIL
from tqdm import tqdm
import torch
import torchvision
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import pickle
import numpy as np
from torchvision import transforms
import png
import cv2

#dir_path = "/media/yalu/6066C1DD66C1B3D6/images/pom/campus"
dir_path = "/media/yalu/6066C1DD66C1B3D6/images/my"
masks_path = "{}/masks.npy".format(dir_path)

masks = np.load(masks_path)
print(masks.shape)

# new_masks = np.zeros((3,1700,360,288,3))
# for cam in range (3):
#        for frame in range(1700):
#               new_masks[cam][frame] = masks[cam][frame][:,:].transpose() 
# print(new_masks.shape)

new_masks = masks.swapaxes(2,3)
print(new_masks.shape)

#dir_path
start = 200
cam_param_path = "{}/camera_parameter.pickle".format(dir_path)
config_path = "{}/constants.txt".format(dir_path)

# image paths
img_names = []
cam_num = 3
for cam_id in range(cam_num):
    cam_imgs_root = "{}/cam{}".format(dir_path,str(cam_id))
    imgs_one_cam = os.listdir(cam_imgs_root)
    imgs_one_cam.sort(key = lambda x:int(x.split('.')[0]))
    img_paths = [os.path.join( cam_imgs_root, img_name) for img_name in imgs_one_cam]
    img_names.append(img_paths)


def getImgs(img_names, idx):
    
    img_0_name = img_names[0][idx]
    img_1_name = img_names[1][idx]
    img_2_name = img_names[2][idx]

    img_0_pil = PIL.Image.open(img_0_name).convert("RGB")
    img_1_pil = PIL.Image.open(img_1_name).convert("RGB")
    img_2_pil = PIL.Image.open(img_2_name).convert("RGB")
    
    #img_0 = np.array(img_0_pil)
    #img_1 = np.array(img_1_pil)
    #img_2 = np.array(img_2_pil)
    
    return [img_0_pil, img_1_pil, img_2_pil]
    

cv2.namedWindow("img",0);
cv2.resizeWindow("img", 640, 480);
cv2.namedWindow("mask",0);
cv2.resizeWindow("mask", 640, 480);

for idx in range(280,500):
    print(idx)
    img_pils = getImgs(img_names, idx)
    imgs_show = []
    masks_show = []
    for cam_id in range(3):
        mask = new_masks[cam_id][idx]
        img  = cv2.imread(img_names[cam_id][idx])
        imgs_show.append(img)
        masks_show.append(mask)
       #  print("Img:",img.shape)
       #  print("Mask:",mask.shape)
    stack_img = np.vstack((imgs_show[0],imgs_show[1],imgs_show[2]))
    stack_mask = np.vstack((masks_show[0],masks_show[1],masks_show[2]))
    cv2.imshow("img",stack_img)
    cv2.imshow("mask",stack_mask)
    key = cv2.waitKey(0)
    
    if(key == ord('q')):
        break
    if(key == ord('s')):
        print(idx)

cv2.destroyAllWindows()

               
    
    
    


              


