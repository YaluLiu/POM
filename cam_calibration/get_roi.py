# coding: utf-8
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cam',help="input the digital number",type=int)
args = parser.parse_args()
cam_id = args.cam
img_id = 30

img_path = "./cam{}/{}.jpg".format(cam_id,img_id)
img = cv2.imread(img_path)

print(img.shape) # 720,1280 y*x

points_lst = []
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        points = (x,y)
        print(points)
        points_lst.append(points)
        #cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)
        cv2.waitKey(1)


cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", img.shape[1],img.shape[0])
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)

while (True):
    try:
        if(cv2.waitKey(100) & 0xFF == ord("q")):
          break
    except Exception:
        cv2.destroyAllWindows()
        break

#with open(txt_path, 'w') as f:
#    for item in points_lst:
#        f.write("{} {}".format(item[0],item[1]))
print(points_lst[0][0], end = ", ") #roi_x1
print(points_lst[2][1], end = ", ") #y1

print(points_lst[1][0], end = ", ") #roi_x2
print(points_lst[3][1]) #roi_y2

cv2.waitKey(0)
cv2.destroyAllWindows()
