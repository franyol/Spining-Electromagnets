import modules.spining_electromagnets as sp
import modules.spining_simulator as ss

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import numpy as np


prot = []
prot2 = []

circulo = sp.coil_gen_circle(0.03, 20)
circulo.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(1, 0, 0)))
circulo.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(0, 0, 1)))

# ss.plot_torque_vs_angle(circulo, sp.Vector(1, 0, 0), ax)

circulo2 = sp.coil_gen_circle(0.03, 20)
circulo2.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(1, 0, 0)))
# circulo.plot()

prot.append(circulo)
prot.append(circulo2)

simu = sp.Spinner(prot, sp.RotationAxis(sp.Vector(-0.03, 0, 0), sp.Vector(0, 0, 1)))

simu.move(sp.Vector(-0.03, 0, 0))

circulo3 = sp.coil_gen_circle(0.03, 20)
circulo3.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(1, 0, 0)))
circulo3.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(0, 0, 1)))


circulo4 = sp.coil_gen_circle(0.03, 20)
circulo4.rotate(3.1416/2, sp.RotationAxis(sp.Vector(0, 0, 0), sp.Vector(1, 0, 0)))
# circulo.plot()

prot2.append(circulo3)
prot2.append(circulo4)

simu2 = sp.Spinner(prot2, sp.RotationAxis(sp.Vector(0.03, 0, 0), sp.Vector(0, 1, 1)))

simu2.move(sp.Vector(0.03, 0, 0))


i_c1 = []
i_c2 = []

for i in range(500):
    i_c1.append(0.1*10)
    i_c2.append(0.1*10)

b_field = sp.Vector(0.5, 0, 0)
b_field = b_field.unit()
b_field = b_field.scalar_mul(0.007)

ss.simulate_movement([simu, simu2], 
                     b_field, 
                     [list([i_c1, i_c2]), list([i_c2, i_c1])], 
                     0.03)
