from re import X
import modules.spining_electromagnets as sp

a = sp.Vector(3, -5, 3)
b = sp.Vector(1, 2, 3)

c = sp.Vector(12, 20, 30)

x = sp.Vector(0, 0, 0)
y = sp.Vector(0, 1, 0)

ho = sp.Cable(a, b, 1)

ax = sp.RotationAxis(x, y)

print(ho.head)
print(ho.tail)
print(ho.head - ho.tail)

print("")

ho.rotate(3.1416/2, ax)

print(ho.head)
print(ho.tail)
print(ho.head - ho.tail)
print("")