import modules.spining_electromagnets as sp

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


circulo = sp.coil_gen_circle(1, 100)
circulo.plot()

circulo.rotate(3.1416/4, sp.RotationAxis(sp.Vector(1, 0, 0), sp.Vector(0, 1, 0)))
circulo.plot()


# plt.savefig('books_read.png')