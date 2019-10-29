# coding: utf-8
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cam',help="input the digital number",type=int)
args = parser.parse_args()
cam_id = args.cam

img_id = 30

img_path = "cam{}.jpg".format(cam_id)
txt_path = "points_door_cam{}.txt".format(cam_id)

img = cv2.imread(img_path)
print(img.shape)

roi = [0, 0, img.shape[0], img.shape[1]]
#roi = [460, 444, 770, 553]
roi_x1 = roi[0]
roi_y1 = roi[1]
roi_x2 = roi[2]
roi_y2 = roi[3]
roi_w = roi[2] - roi[0]
roi_h = roi[3] - roi[1]

#roi_image = img[roi_y1:roi_y2,roi_x1:roi_x2,:]
roi_image = img

points_lst = []
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(roi_image, (x, y), 1, (0, 0, 255), thickness=-1)
        points = (x+roi_x1,y+roi_y1)
        print(points[0],points[1])
        points_lst.append(points)
        #cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", roi_image)
        cv2.waitKey(1)


cv2.namedWindow("image", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("image", roi_w * 4,roi_h * 4)
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", roi_image)

while (True):
    try:
        if(cv2.waitKey(100) & 0xFF == ord("q")):
          break
    except Exception:
        cv2.destroyAllWindows()
        break

print("Start to write to {}".format(txt_path))
with open(txt_path, 'w') as f:
    for points in points_lst:
        f.write("{} {}\n".format(points[0],points[1]))

print("write end")
cv2.destroyAllWindows()
