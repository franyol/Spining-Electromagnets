import modules.spining_electromagnets as sp
import modules.spining_simulator as ss

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import numpy as np


prot = []
prot2 = []

espira = []
espira2 = []

espira.append(sp.Cable(sp.Vector(-0.02, 0, -0.02), sp.Vector(-0.02, 0, 0.02), 1))
espira.append(sp.Cable(sp.Vector(-0.02, 0, 0.02), sp.Vector(0.02, 0, 0.02), 1))
espira.append(sp.Cable(sp.Vector(0.02, 0, 0.02), sp.Vector(0.02, 0, -0.02), 1))
espira.append(sp.Cable(sp.Vector(0.02, 0, -0.02), sp.Vector(-0.02, 0, -0.02), 1))

espira2.append(sp.Cable(sp.Vector(0, -0.02, -0.02), sp.Vector(0, -0.02, 0.02), 1))
espira2.append(sp.Cable(sp.Vector(0, -0.02, 0.02), sp.Vector(0, 0.02, 0.02), 1))
espira2.append(sp.Cable(sp.Vector(0, 0.02, 0.02), sp.Vector(0, 0.02, -0.02), 1))
espira2.append(sp.Cable(sp.Vector(0, 0.02, -0.02), sp.Vector(0, -0.02, -0.02), 1))

espi = sp.Coil(espira)
espi2 = sp.Coil(espira2)

prot.append(espi)
prot.append(espi2)
# prot.append(circulo2)

simu = sp.Spinner(prot, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(0, 0, 1)))


# circulo.plot()



i_c1 = []
i_c2 = []

for i in range(800):
    i_c1.append(0.1*10)
    i_c2.append(0.1*10)

b_field = sp.Vector(1, 0, 0)
b_field = b_field.unit()
b_field = b_field.scalar_mul(0.07)

ss.simulate_movement([simu], 
                     b_field, 
                     [list([i_c1, i_c2])], 
                     0.07)
