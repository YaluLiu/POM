import pickle
import cv2
import numpy as np

# test pickle if right

cam_id = 1
cam_param_path  = "./pickle/cam_param_{}.pickle".format(cam_id)
with open(cam_param_path, "rb") as handle:
    cam_param = pickle.load(handle)
print(cam_param)


test_img = "cam{}.jpg".format(cam_id)
img= cv2.imread(test_img)
assert(img is not None)



width = 400
height = 800
nb_width = 20
nb_height = 40
origin_x = 0
origin_y = -100

world = []
for i in range(nb_height):
    for j in range(nb_width):
        tmpw = j / nb_width * width
        tmph = i / nb_height * height
        world.append(np.array((tmpw + origin_x,tmph + origin_y, 0.0),dtype = np.float64))

objp = np.array(world,dtype = np.float64)
objp = objp.reshape(-1,1,3)


rvec = cam_param['rvec']
tvec = cam_param['tvec']
cameraMatrix = cam_param['matrix']
dist = cam_param['dist']
points_2d,tmp = cv2.projectPoints(objp, rvec, tvec, cameraMatrix, dist)
print(points_2d.shape)  

cnt = 0
for point_2d in points_2d:
    x = int(point_2d[0][0])
    y = int(point_2d[0][1])
    if(x < 0 or x > 1280 or y < 0 or y > 720):
        continue
    cv2.circle(img,(x,y),2,(255,0,0),2)
#cv2.circle(img,(points_2d[0][0][0],points_2d[0][0][1]),2,(0,0,255),2)
#cv2.circle(img,(points_2d[-1][0][0],points_2d[-1][0][1]),2,(0,255,0),2)


#add single point
new_point = np.array(([0,0,0]),dtype = np.float64)
new_point = new_point.reshape(-1,1,3)
point_2d,tmp = cv2.projectPoints(new_point, rvec, tvec, cameraMatrix, dist)
print(point_2d)
print(point_2d.shape)
cv2.circle(img,(int(point_2d[0][0][0]),int(point_2d[0][0][1])),2,(0,0,255),2)

#add real world points
num_points = 9
points_lst = []
points_path = "./points/points_real_door.txt"
f = open(points_path)
lines = f.read().split("\n")
for line in lines:
    line = line.split(" ")
    if(len(line) < 3):
        break
    print(line)
    points_lst.append((int(line[0]),int(line[1]),int(line[2])))
f.close()

objpoints = np.zeros((num_points,1,3),dtype = np.float32)
for i in range(num_points):
    objpoints[i][0][0]  = points_lst[i][0]
    objpoints[i][0][1]  = points_lst[i][1]
    objpoints[i][0][2]  = points_lst[i][2]

points_2d,tmp = cv2.projectPoints(objpoints, rvec, tvec, cameraMatrix, dist)
for point in points_2d:
    print(point)
    cv2.circle(img,(int(point[0][0]),int(point[0][1])),2,(0,0,255),2)

cv2.imshow("",img)
cv2.waitKey(0)

cv2.destroyAllWindows()