import numpy as np
import cv2
import glob
import os 
import pickle
import argparse

w = 9
h = 8

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
fisheye_flags = cv2.CALIB_RATIONAL_MODEL


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((w*h,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
objp *= 10
print("coordinate of chessboard:")
#print(objp.shape)
#print(objp)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane
images = [] # images path
point_counts = 0

for cam_id in range(2):
  for img_id in range(31):
    file_path = "./images/cam{}/{}.jpg".format(cam_id,img_id)
    if(os.path.exists(file_path)):
      images.append(file_path)

  for fname in images:
      img = cv2.imread(fname)
      gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      print(gray.shape[::-1])
      # Find the chess board corners
      ret, corners = cv2.findChessboardCorners(gray, (w,h),None)
      # print(corners)

      # If found, add object points, image points (after refining them)
      if ret == True:
          print("found in {}".format(fname))
          objpoints.append(objp)

          corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
          imgpoints.append(corners2)
          #print("corners2")
          #print(corners2.shape)
          #print(corners2[0])
          #print(type(corners),corners.dtype)

          # Draw and display the corners
          #print("W{}H{}".format(w,h))
          #img = cv2.drawChessboardCorners(img, (w,h), corners2,ret)
          #cv2.imshow('img',img)
          #cv2.waitKey(0)
      else:
          print("not found in {}".format(fname))
          points_lst = []
          points_path = "points_lst_cam{}.txt".format(cam_id)
          f = open(points_path)
          lines = f.read().split("\n")
          for line in lines:
            line = line.split(" ")
            if(len(line) < 2):
              break
            points_lst.append((int(line[0]),int(line[1])))
          f.close()
          num_points = len(points_lst)
          assert(num_points == 72)
          corners2 = np.zeros((72,1,2),dtype = np.float32)
          for i in range(72):
            corners2[i,:,0] = points_lst[i][0]
            corners2[i,:,1] = points_lst[i][1]
          objpoints.append(objp)
          imgpoints.append(corners2)
          img = cv2.drawChessboardCorners(img, (w,h), corners2,ret)
          cv2.imshow('img',img)
          cv2.waitKey(1000)


  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,  gray.shape[::-1],None,None,flags = fisheye_flags)
  #print(objpoints[0].shape) #(72,3)
  #print(imgpoints[0].shape) #(72,1,2)


  #cam_dict= {"matrix": mtx, "rvecs":rvecs,"tvecs":tvecs}
  cam_dict= {"matrix": mtx, "dist":dist,"rvec":rvecs[-1],"tvec":tvecs[-1]}

  pickle_path = './pickle/cam_param_{}.pickle'.format(cam_id)
  with open(pickle_path, 'wb') as handle:
      pickle.dump(cam_dict, handle)

cv2.destroyAllWindows()



