import pickle
import cv2
import numpy as np

cam_params = []

for cam_id in range(2):
    cam_param_path  = "cam_param_{}.pickle".format(cam_id)
    with open(cam_param_path, 'rb') as fp:
        cam_param = pickle.load(fp)
        #print(cam_param)
        cam_params.append(cam_param)

save_param = dict()
save_param["P"] = cam_params
save_param["more_param"] = False
cam_param_path = "camera_parameter_merge.pickle"
with open(cam_param_path, 'wb') as handle:
    pickle.dump(save_param, handle)






    




