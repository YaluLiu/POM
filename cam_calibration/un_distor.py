import pickle
import cv2
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cam',help="input the digital number",type=int)
args = parser.parse_args()
cam_id = args.cam

pickle_name = 'cam_param_{}.pickle'.format(cam_id)
image_path = "./images/origin/cam{}/*.jpg".format(cam_id)
with open(pickle_name, 'rb') as handle:
    cam_dict = pickle.load(handle)

print(cam_dict.keys())
mtx = cam_dict["matrix"]
dist = cam_dict["dist"]
images = glob.glob(image_path)

cnt = 0
for fname in images:
  print(fname)
  # img = cv2.imread(fname)
  # #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  # h,  w = img.shape[:2]
  # print(h,w)

  # factor = 1
  # alpha  = 1
  # print(dist)
  # newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist[0],(w,h),alpha,(int(w * factor),int(h * factor)))
  # # print(roi)

  # # undistort
  # dst = cv2.undistort(img, mtx, dist[0], None, newcameramtx)

  # # crop the image
  # x,y,w,h = roi
  # if(x + y + w + h != 0):
  #   dst = dst[y:y+h, x:x+w]
  #   cv2.imshow("no_distor",dst)
  #   cv2.waitKey(100)

  # cnt += 1
  # cv2.imwrite("./images/cam0/undist/{}.jpg".format("undist" + str(cnt)),dst)
  # #cv2.imwrite('calibresult.png',dst)
