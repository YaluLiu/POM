import os
import math
import numpy as np
import random

import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.animation import FuncAnimation, writers


# setup the figure and axes
fig = plt.figure(figsize=(8, 3))
ax1 = fig.add_subplot(111, projection='3d')

fps = 1
limit = 16
bitrate = 1000
num_x = 36
num_y = 29
    
def update_video(frame):
    dat_path = './results/proba-f{}.dat'.format(str(frame))
    f = open(dat_path,'r')
    lines = f.readlines()
    
    num_rectangle = len(lines)
    dat = np.zeros((num_x,num_y),dtype = np.float32)
    for i in range(num_rectangle):
        tmp = lines[i].split(" ")
        x = i // num_y
        y = i % num_y
        dat[x][y] = tmp[1]
    
    # fake data
    _x = np.arange(num_x)
    _y = np.arange(num_y)
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    top = dat.ravel()
    bottom = np.zeros_like(top)
    width = depth = 1
    if(frame > 0):
        ax1.collections.pop()
    bar3d = ax1.bar3d(x, y, bottom, width, depth, top, shade=True,color='C0')
    print('{}/{}      '.format(frame, limit), end='\r')


anim = FuncAnimation(fig, update_video, frames=np.arange(0, limit), interval=1000/fps, repeat=False)
output = "results.mp4"
if output.endswith('.mp4'):
    Writer = writers['ffmpeg']
    writer = Writer(fps=fps, metadata={}, bitrate=bitrate)
    anim.save(output, writer=writer)
elif output.endswith('.gif'):
    anim.save(output, dpi=80, writer='imagemagick')
else:
    raise ValueError('Unsupported output format (only .mp4 and .gif are supported)')
plt.close()
