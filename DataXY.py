from math import *
import numpy as np

angle = 1.42
distance = 295
x = np.arccos(angle) * distance
y = np.arcsin(angle) * distance
# x = acos(angle) * distance
# y = asin(angle) * distance
print(x,y)