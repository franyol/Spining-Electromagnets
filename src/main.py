import modules.spining_electromagnets as sp
import modules.spining_simulator as ss

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

bobina = sp.coil_gen_coil(0.02, 4, 15, 5, 0.005)

bobina.plot(ax)

plt.show()