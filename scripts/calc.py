import numpy as np 
import math
rad = 11.9
camera_h = 1.5
floor_h = 2.6
pos = (floor_h - camera_h)/np.tan(math.radians(rad))
print(pos)
