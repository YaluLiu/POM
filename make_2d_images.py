import os
import math
import numpy as np
import random
import pickle
import cv2
from PIL import Image
from tqdm import tqdm

import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.animation import FuncAnimation, writers


# setup the figure and axes
fig = plt.figure(figsize=(24, 8))

grid = plt.GridSpec(2, 2,wspace = 0, hspace = 0)
ax1 = fig.add_subplot(grid[0,0])
ax2 = fig.add_subplot(grid[1,0])
ax3 = fig.add_subplot(grid[:,1])

fps   = 1
start = 0
end   = 280
bitrate = 1000
config_dict = {}
f = open("constant.txt")
for line in f.readlines():
    line = line.strip().split(" ")
    config_dict[line[0]] = line[1]
f.close()

width = float(config_dict["WIDTH"])
height = float(config_dict["HEIGHT"])

nb_width = int(config_dict["NB_WIDTH"])
nb_height = int(config_dict["NB_HEIGHT"])

img_w = int(config_dict["IMG_W"])
img_h = int(config_dict["IMG_H"])

man_ray = float(config_dict["MAN_RAY"])
man_height = float(config_dict["MAN_HEIGHT"])

origin_x = float(config_dict["ORIGINE_X"])
origin_y = float(config_dict["ORIGINE_Y"])
    
def make_proba_images(frame,ax):
    img_name = "proba_images/{}.png".format(frame)
    dat_path = './results/proba-f{}.dat'.format(str(frame))
    f = open(dat_path,'r')
    lines = f.readlines()
    
    num_rectangle = len(lines)
    assert(num_rectangle == nb_height * nb_width)
    dat = np.zeros((nb_height,nb_width),dtype = np.float64)
    for i in range(num_rectangle):
        tmp = lines[i].split(" ")
        h = i // nb_width
        w = i % nb_width
        dat[h][w] = tmp[1]
        # if(i == 0 or i == num_rectangle - 1):
        #     dat[h][w] = 1
        # else:
        #     dat[h][w] = 0
    
    #plt.figure(figsize=(12.8, 7.2))
    ax.imshow(dat,origin = 'lower')
    fig.savefig(img_name)

def make_points(img_name,points_2d,ax):
    '''
    '''
    img = Image.open(img_name)
    
    ax.axis('off') # 关掉坐标轴为 off
    ax.scatter(points_2d[:,0,0], points_2d[:,0,1], c='tab:blue')
    ax.scatter(points_2d[0][0][0], points_2d[0][0][1], c='tab:red')
    ax.scatter(points_2d[1][0][0], points_2d[1][0][1], c='tab:red')
    ax.scatter(points_2d[nb_width+1][0][0], points_2d[nb_width+1][0][1], c='tab:red')
    ax.scatter(points_2d[-1][0][0], points_2d[-1][0][1], c='tab:red')
    ax.imshow(img)


cam_id = 0
#dir_path = "/media/yalu/6066C1DD66C1B3D6/ubuntu/MyProjects/cam_calibration/images/test0"
dir_path = "./images/origin"
cam_imgs_root = ["{}/cam{}".format(dir_path,str(cam_id)) for cam_id in range(2)]
def get_draw_par(cam_id):
    cam_param_path  = "cam_param_{}.pickle".format(cam_id)
    with open(cam_param_path, "rb") as handle:
        cam_param = pickle.load(handle)

    world = np.zeros((nb_height*nb_width,3),dtype = np.float64)
    for i in range(nb_height):
        for j in range(nb_width):
            tmpw = j / nb_width * width
            tmph = i / nb_height * height
            world[i*nb_width +j][0] = tmpw + origin_x
            world[i*nb_width +j][1] = tmph + origin_y
            world[i*nb_width +j][2] = 0.0

    rvec = cam_param['rvec']
    tvec = cam_param['tvec']
    cameraMatrix = cam_param['matrix']
    dist = cam_param['dist']
    points_2d,tmp = cv2.projectPoints(world, rvec, tvec, cameraMatrix, dist)
    img_names = os.listdir(cam_imgs_root[cam_id])
    img_names.sort()
    imgs_cam = [os.path.join(cam_imgs_root[cam_id], img_name) for img_name in img_names]
    return points_2d, imgs_cam
    

points_cam0,imgs_cam0 = get_draw_par(0)
points_cam1,imgs_cam1 = get_draw_par(1)
for i in tqdm(range(start,end)):
    make_points(imgs_cam0[i],points_cam0,ax1)
    make_points(imgs_cam1[i],points_cam1,ax2)
    make_proba_images(i,ax3)

