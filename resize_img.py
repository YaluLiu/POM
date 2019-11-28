#!/usr/bin/env python
# coding: utf-8# In[1]:


import os
import shutil

def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        #dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        #dir_list = sorted(dir_list,  key=lambda x:x)
        dir_list = sorted(dir_list,  key=lambda x: int(x.split(".")[0]))
        # print(dir_list)
        return dir_list

def resize_image():
    return True



Just_Test = True



s = []
cnt = 0
for cam_id in range(3):
    cnt = 0
    path = "/media/yalu/6066C1DD66C1B3D6/images/my_4K/cam{}".format(cam_id) #文件夹目录
    dst_path = "/media/yalu/6066C1DD66C1B3D6/images/my/cam{}".format(cam_id) #文件夹目录
    files = get_file_list(path) #得到文件夹下的所有文件名称
    for file in files[140:800]: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
        cnt = cnt + 1
        print(file, end = ": ")
        newName = str(cnt) + ".jpg"
        print(newName)
        
        if Just_Test == True:
            dst_name = os.path.join(dst_path,newName)
            src_name = os.path.join(path,file)
            cmd  = "ffmpeg -y -i {} -vf scale=1280:720 {}".format(src_name,dst_name)
            os.system(cmd)
print("END!")


