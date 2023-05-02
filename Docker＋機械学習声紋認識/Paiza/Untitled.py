#!/usr/bin/env python
# coding: utf-8

# In[2]:

import numpy as np

np.random.seed(1)

x = np.arange(10)
y = np.random.randint(1, 100, 10)
print(x)
print(y)


# In[5]:


import matplotlib.pyplot as plt

plt.plot(x, y)
plt.show()


# In[ ]:




