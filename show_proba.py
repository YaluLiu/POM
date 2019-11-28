import os
import math
import numpy as np
import random
import pickle
import cv2
from PIL import Image
from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib.cm as cm
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.animation import FuncAnimation, writers


start =  300
end   =  400
cams_num = 3
config_dict = {}
#dir_path = "/media/yalu/6066C1DD66C1B3D6/ubuntu/MyProjects/cam_calibration/images/test0"
dir_path = "/media/yalu/6066C1DD66C1B3D6/images/my"
f = open("{}/constants.txt".format(dir_path))
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


grid = plt.GridSpec(3, 3,wspace = 0, hspace = 0)
fig = plt.figure(figsize=(24, 8))

def setup():
    # setup the figure and axes
    ax_cam = []
    mask_cam = []
    ax_cam.append(fig.add_subplot(grid[0,0]))
    ax_cam.append(fig.add_subplot(grid[1,0]))
    ax_cam.append(fig.add_subplot(grid[2,0]))
    mask_cam.append(fig.add_subplot(grid[0,1]))
    mask_cam.append(fig.add_subplot(grid[1,1]))
    mask_cam.append(fig.add_subplot(grid[2,1]))
    ax_result = fig.add_subplot(grid[:,2])
    # ax4 = fig.add_subplot(grid[0,1])
    # ax5 = fig.add_subplot(grid[1,1])
    return ax_cam,mask_cam,ax_result
    
def make_proba_images(frame,ax):
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
    
    ax.imshow(dat,origin = 'lower')
    return dat

def make_points(img_name,points_2d,dat, ax):
    img = Image.open(img_name)
    
    ax.axis('off') # 关掉坐标轴为 off
    ax.scatter(points_2d[:,0,0], points_2d[:,0,1], c=dat.flatten())
    ax.imshow(img)

def make_mask_img(frame, cam_id, ax):
    ax.axis('off') # 关掉坐标轴为 off
    img_path = "results/result-f{}-c{}.png".format(frame,cam_id)
    img = Image.open(img_path)
    ax.imshow(img)


cam_id = 0

cam_imgs_root = ["{}/cam{}".format(dir_path,str(cam_id)) for cam_id in range(cams_num)]

def mat_mul(pts_3d,cam,pts_2d):
    len_pts = len(pts_3d)
    for i in range(len_pts):
        pt_2d = cam.dot(pts_3d[i])
        #print("===={}====".format(i))
        #print(pt_2d)
        pt_2d[0] /= pt_2d[2]
        pt_2d[1] /= pt_2d[2]
        pts_2d.append(pt_2d)

def get_draw_par(cam_id):

    if True:
        cam_param_path  = "{}/camera_parameter.pickle".format(dir_path)
        with open(cam_param_path, "rb") as handle:
            cam_param = pickle.load(handle)
        cam_param = cam_param['P'][cam_id]
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
        #print(points_2d.shape)  (num_locations,1,2)
    else:
        cam_param_path  = "{}/camera_parameter.pickle".format(dir_path)
        with open(cam_param_path, "rb") as handle:
            cam_param = pickle.load(handle)
        cam_param = cam_param['P'][cam_id]
        world = []
        for i in range(nb_height):
            for j in range(nb_width):
                tmpw = j / nb_width * width
                tmph = i / nb_height * height
                world.append(np.array((tmpw + origin_x,tmph + origin_y, 0.0,1.0),dtype = np.float64))
        M0 = cam_param
        points_2d = []
        mat_mul(world, M0, points_2d) 
        #change (num_locations,3)->(num_locations,1,2)
        points_2d = np.array(points_2d)
        points_2d = points_2d[:,:2]
        points_2d = points_2d.reshape(-1,1,2)
        #print(points_2d.shape)


    img_names = os.listdir(cam_imgs_root[cam_id])
    img_names.sort(key = lambda x:int(x.split('.')[0]))
    imgs_cam = [os.path.join(cam_imgs_root[cam_id], img_name) for img_name in img_names]
    return points_2d, imgs_cam
    
points_cam0,imgs_cam0 = get_draw_par(0)
points_cam1,imgs_cam1 = get_draw_par(1)
points_cam2,imgs_cam2 = get_draw_par(2)

img_names = os.listdir(cam_imgs_root[cam_id])
frames_num = len(img_names)
# for img in  imgs_cam0:
#     print(img)

plt.ion()
for i in tqdm(range(start,end)):
    ax_cam,mask_cam,ax_result = setup()
    dat = make_proba_images(i,ax_result)
    make_points(imgs_cam0[i],points_cam0, dat, ax_cam[0])
    make_points(imgs_cam1[i],points_cam1, dat, ax_cam[1])
    make_points(imgs_cam2[i],points_cam2, dat, ax_cam[2])
    # make_mask_img(i, 0, mask_cam[0])
    # make_mask_img(i, 1, mask_cam[1])
    # make_mask_img(i, 2, mask_cam[2])

    # img_name = "proba_images/{}.png".format(i)
    # fig.savefig(img_name)

    plt.show()
    plt.pause(1)
    plt.clf()  #清除图像

