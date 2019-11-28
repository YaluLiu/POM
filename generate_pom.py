import numpy as np
import os 
import cv2

#cam(3,4) pt_3d(4,1) pt_2d(3,1)
def mat_mul(pts_3d,cam,pts_2d):
    len_pts = len(pts_3d)
    for i in range(len_pts):
        pt_2d = cam.dot(pts_3d[i])
        #print("===={}====".format(i))
        #print(pt_2d)
        pt_2d[0] /= pt_2d[2]
        pt_2d[1] /= pt_2d[2]
        pts_2d.append(pt_2d)


def make_pom(cam_id,cam_param,config_dict):

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

    #define the ground
    world = []
    #eight point of cube
    points = []
    #points of projections
    points_projections = []

    #end data, all rectangles of projections
    pom = []

    for i in range(nb_height):
        for j in range(nb_width):
            tmpw = j * width / nb_width
            tmph = i * height / nb_height
            world.append(np.array((tmpw + origin_x,tmph + origin_y, 0.0, 1.0),dtype = np.float64))


    #define the points, 8 by position
    num_positions = nb_width * nb_height
    for i in range(len(world)):
        x = world[i][0]
        y = world[i][1]
        z = world[i][2]
        points.append(np.array((x + man_ray, y + man_ray, z, 1.0),dtype = np.float64))
        points.append(np.array((x + man_ray, y - man_ray, z, 1.0),dtype = np.float64))
        points.append(np.array((x - man_ray, y + man_ray, z, 1.0),dtype = np.float64))
        points.append(np.array((x - man_ray, y - man_ray, z, 1.0),dtype = np.float64))

        points.append(np.array((x + man_ray, y + man_ray, z + man_height, 1.0),dtype = np.float64))
        points.append(np.array((x + man_ray, y - man_ray, z + man_height, 1.0),dtype = np.float64))
        points.append(np.array((x - man_ray, y + man_ray, z + man_height, 1.0),dtype = np.float64))
        points.append(np.array((x - man_ray, y - man_ray, z + man_height, 1.0),dtype = np.float64))

    if("more_param" in cam_param.keys()):
        rvec = cam_param["P"][cam_id]['rvec']
        tvec = cam_param["P"][cam_id]['tvec']
        cameraMatrix = cam_param["P"][cam_id]['matrix']
        dist = cam_param["P"][cam_id]['dist']
        # axis = np.float64([[0,0,0], [0,1,0], [1,1,0], [1,0,0],
        #                   [0,0,-1],[0,1,-1],[1,1,-1],[1,0,-1] ])
        for i in range(len(points)):
            points[i] = points[i][:3]
        points = np.array(points,dtype = np.float64)
        #print("Shape of Points:",points.shape)
        points_projections,tmp = cv2.projectPoints(points, rvec, tvec, cameraMatrix, dist)
        #print("Shape of points_projections:",points_projections.shape)
        points_projections = np.squeeze(points_projections)

    else:
        cameraMatrix = cam_param["P"][cam_id]
        mat_mul(points, cameraMatrix, points_projections)
    
    

    for i in range(num_positions):
        xmin = int(points_projections[8 * i][0])
        ymin = int(points_projections[8 * i][1])
        xmax = int(points_projections[8 * i][0])
        vec = []
        for j in range(8):
            x = int(points_projections[8 * i + j][0])
            y = int(points_projections[8 * i + j][1])
            xmin = min(xmin,x)
            ymin = min(ymin,y)
            xmax = max(xmax,x)
            vec.append((y,x))
        vec.sort()
        yMid = 0
        for j in range(4,8):
            yMid += vec[j][0]
        yMid /= 4

        #solve 
        visible = True
        
        ymax = int(yMid)
        if(xmin >= img_w - 2 or ymin >= img_h - 2):
            visible = False
        elif(xmax >= img_w or ymax >= img_h):
            visible = False
        elif(xmax <= 1 or ymax <= 1):
            visible = False  
        elif(xmin < 0 or ymin < 0):
            visible = False 
        elif(ymax - ymin < xmax - xmin):
            visible = False 
        elif(xmax - xmin > img_w / 3):
            visible = False  
        else:
            visible = True   
        
        line = "RECTANGLE {} {}".format(cam_id, i)
        if(visible):
            line += " {} {} {} {}".format(xmin, ymin, xmax, ymax)
        else:
            line += " notvisible"
        
        line = line.split(" ")
        pom.append(line)
    return pom



# cam_id = 0

# cam_param_path = "./camera_parameter.pickle"
# with open(cam_param_path, 'rb') as fp:
#     cam_param = pickle.load(fp)
# cameraMatrix = cam_param["P"][cam_id]
# #print(cameraMatrix.dtype,cameraMatrix.shape)


# config_path = "./constant.txt"
# config_dict = {}
# f = open(config_path)
# for line in f.readlines():
#     line = line.strip().split(" ")
#     config_dict[line[0]] = line[1]
# f.close()
# #print(config_dict)

# pom = make_pom(cam_id,cameraMatrix,config_dict)
# print(pom[:10])

def get_room_data(cams_num,config_dict):
    num_locations = int(config_dict["NB_WIDTH"]) * int(config_dict["NB_HEIGHT"])
    room_data = [['ROOM', config_dict["IMG_W"], config_dict["IMG_H"], str(cams_num), str(num_locations)]]
    return room_data

def get_pom_data(cams_num,cam_param,config_dict,result_view_image = False):
    pom = []
    for cam_id in range(cams_num):
        pom += make_pom(cam_id,cam_param,config_dict)

    path = "./results"
    if not os.path.exists(path):
        os.makedirs(path)
    if(result_view_image):
        pom.append(['RESULT_VIEW_FORMAT', './results/result-f%f-c%c.png'])
    #pom.append(['RESULT_FORMAT', './results/proba-f%f.dat'])
    pom.append(['PROBA_IGNORED', '0.9999'])
    return pom


