#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import math
import numpy as np

import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# In[2]:


f = open('./results/proba-f0.dat','r') 
lines = f.readlines()
print(len(lines))


# In[3]:


for i in range(len(lines)):
    tmp = lines[i].split(" ")
    print(type(tmp[1]))
    break


# In[ ]:





# In[4]:


num_rectangle = len(lines)
num_x = 36 * 2
num_y = 28 * 2


# In[5]:


dat = np.zeros((num_x,num_y),dtype = np.float32)


# In[6]:


for i in range(len(lines)):
    tmp = lines[i].split(" ")
    x = i // num_y
    y = i % num_y
    dat[x][y] = tmp[1]


# In[7]:


# setup the figure and axes
fig = plt.figure(figsize=(num_x,num_y))
ax = fig.add_subplot(111, projection='3d')

# fake data
_x = np.arange(num_x)
_y = np.arange(num_y)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()

top = dat.ravel()
bottom = np.zeros_like(top)
width = depth = 5

ax.bar3d(x, y, bottom, width, depth, top, shade=True)

plt.show()


# In[ ]:




