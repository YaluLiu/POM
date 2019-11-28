import pickle
import cv2
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cam',help="input the digital number",type=int)
args = parser.parse_args()
cam_id = args.cam

pickle_name = './MyOwn/cam_param_{}.pickle'.format(cam_id)
image_path = "/media/yalu/6066C1DD66C1B3D6/images/my/cam{}/*.jpg".format(2)
with open(pickle_name, 'rb') as handle:
    cam_dict = pickle.load(handle)


#print(cam_dict.keys())
mtx = cam_dict["matrix"]
dist = cam_dict["dist"]

print(mtx)
print(dist)

# images = glob.glob(image_path)
# images.sort()

# cnt = 0
# for fname in images:
#   print(fname)
#   img = cv2.imread(fname)
#   h,  w = img.shape[:2]

#   factor = 1
#   alpha  = 1
#   newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),alpha,(int(w * factor),int(h * factor)))
#   # print(roi)

#   # undistort
#   dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

#   # crop the image
#   x,y,w,h = roi
#   dst = dst[y:y+h, x:x+w]
#   # cv2.imshow("no_distor",dst)
#   # cv2.waitKey(100)

#   cnt += 1
#   cv2.imwrite("./images/adjust/cam{}/{}.jpg".format(cam_id,cnt),dst)
#   #cv2.imwrite('calibresult.png',dst)
