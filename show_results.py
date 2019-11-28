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


cv2.namedWindow("results",cv2.WINDOW_NORMAL);
# cv2.resizeWindow("results", 640, 480);

for frame in range(290,350):
    imgs = []
    for cam_id in range(3):
        img_path = "results/result-f{}-c{}.png".format(frame,cam_id)
        img = cv2.imread(img_path)
        #cv2.putText(img,str(frame),(20,20))
        imgs.append(img)
    stack_img = np.hstack((imgs[0],imgs[1],imgs[2]))
    cv2.imshow("results",stack_img)

    key = cv2.waitKey(0)
    
    if(key == ord('q')):
        break
    if(key == ord('s')):
        print(idx)

cv2.destroyAllWindows()
    