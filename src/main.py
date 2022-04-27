import modules.spining_electromagnets as sp
import modules.spining_simulator as ss

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import numpy as np

a = sp.Vector(0.3, -0.5, 0.3)
b = sp.Vector(0.1, 0.2, 0.3)

c = sp.Vector(0.5, 0.2, 0.6)

x = sp.Vector(0, 0, 0)
y = sp.Vector(0, 0, 1)

cl = []
ho = sp.Cable(a, b, 1)
cl.append(sp.Cable(a, b, 1)) 
cl.append(sp.Cable(b, c, 1))

cc = sp.Coil(cl)

ax = sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(0, 0, 1))

"""

print(ho.head)
print(ho.tail)
print(ho.head - ho.tail)
print(abs(ho.head - ho.tail))

print("")

ho.rotate(-3.1416/2, ax)

print(ho.head)
print(ho.tail)
print(ho.head - ho.tail)
print(abs(ho.head - ho.tail))
print("")
"""


circulo = sp.coil_gen_circle(1, 20)
circulo.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(1, 0, 0)))
circulo.plot()

ss.plot_torque_vs_angle(circulo, sp.Vector(1, 0, 0), ax)

a1 = sp.Vector(1, 0, 0)
a2 = sp.Vector(1, 0, 1)
a3 = sp.Vector(1+0.6, 0, 0)
a4 = sp.Vector(1+0.6, 0, 1)

vx= []

vx.append(sp.Cable(a2, a1, 1))
vx.append(sp.Cable(a3, a2, 1))
vx.append(sp.Cable(a4, a3, 1))
vx.append(sp.Cable(a1, a4, 1))

corbatin = sp.Coil(vx)
corbatin.plot()

ss.plot_torque_vs_angle(corbatin, sp.Vector(1, 0, 0), ax)

# plt.savefig('books_read.png')
