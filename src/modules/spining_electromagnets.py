'''
Coded by Francisco Valbuena
GitHub: franyol
e-mail: f.valbuenao64@gmail.com
'''

# =============================================================================

# Standard library imports
import math
from re import U

# Third party imports
import numpy as np
import matplotlib as plt

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# =============================================================================


class Vector:
    """!
    Class for having vector variables and some basic operations
    """
    
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):

        self.i = x
        self.j = y
        self.k = z
        
    def __str__(self):

        cadena = ""
        if self.i < 0:
            cadena += "- "
        cadena += str(abs(self.i)) + "i "

        if self.j < 0:
            cadena += "- "
        else:
            cadena += "+ "
        cadena += str(abs(self.j)) + "j "

        if self.k < 0:
            cadena += "- "
        else:
            cadena += "+ "
        cadena += str(abs(self.k)) + "k"

        return cadena
        
    def __add__(self, other):

        sum = Vector()
        
        sum.i = self.i + other.i
        sum.j = self.j + other.j
        sum.k = self.k + other.k
        
        return sum
    
    def __sub__(self, other):

        subs = Vector()
        
        subs.i = self.i - other.i
        subs.j = self.j - other.j
        subs.k = self.k - other.k
        
        return subs
    
    def __abs__(self):

        return math.sqrt(self.i**2 + self.j**2 + self.k**2)

    def scalar_mul(self, scalar: float):

        response = Vector()

        response.i = self.i * scalar
        response.j = self.j * scalar
        response.k = self.k * scalar

        return response

    def unit(self):

        return self.scalar_mul(1/abs(self))

    def dot(self, no):

      response = self.i * no.i + self.j * no.j + self.k * no.k

      return response

    def cross(self, no):

      response = Vector(self.j * no.k - self.k * no.j, 
                        self.k * no.i - self.i * no.k, 
                        self.i * no.j - self.j * no.i)

      return response

class RotationAxis:
    """!
    The rotation axis is just a line in R3.
    """

    def __init__(self, Ae: Vector, Ve: Vector):
        """!
        @param Ae Vector that points to a point on the line
        @param Ve Vector pointing in the line's direction
        """
        self.Ae = Ae
        self.Ve = Ve.unit()

class Cable:
    """!
    Here you save the head and tai of the vectors that point to the
    cable in R3, also the magnitude of the current which is pointing
    in the head - tail vector direction, if negative, points backwards.
    """
    
    def __init__(self, head: Vector, tail: Vector, current: float):

        self.head = head
        self.tail = tail
        self.current = current

    def set_current(self, current: float):
        """!
        change the the magnitude of the current which is pointing
        in the head - tail vector direction, if negative, points backwards.
        """

        self.current = current

    def move(self, move: Vector):
        """!
        Adds the move position to the actual cable position

        @param move Vector that has the moving direction
        """

        self.head += move
        self.tail += move

    def abs_move(self, coords: Vector):
        """!
        Changes the actual head of the cable position for the new 
        coords mantaining the head - tail vector (thus moving the
        tail)

        @param coords Vector that has the new coordinates of the 
               head
        """

        save = Vector()
        save = self.head - self.tail

        self.head = coords
        self.tail = self.head - save

    def rotate(self, angle: float, axis: RotationAxis):
        """!
        Adds the move position to the actual cable position

        @param angle float of the rotation angle in radians
        @param axis RotationAxis
        """

        # p is the closest point of the axis to the cable centre
        p = axis.Ae + axis.Ve.scalar_mul(axis.Ve.dot(self.head - axis.Ae))
        d = self.head - p
        dir1 = p - self.head
        dir1 = dir1.unit()
        dir2 = axis.Ve.cross(dir1.scalar_mul(-1))
        dir2 = dir2.unit()
        self.head += dir1.scalar_mul(math.cos(math.pi/2 - angle/2) * math.sqrt(2 * abs(d)**2 * (1 - math.cos(angle)))) 
        self.head += dir2.scalar_mul(math.sin(math.pi/2 - angle/2) * math.sqrt(2 * abs(d)**2 * (1 - math.cos(angle))))

        p = axis.Ae + axis.Ve.scalar_mul(axis.Ve.dot(self.tail - axis.Ae))
        d = self.tail - p
        dir1 = p - self.tail
        dir1 = dir1.unit()
        dir2 = axis.Ve.cross(dir1.scalar_mul(-1))
        dir2 = dir2.unit()
        self.tail += dir1.scalar_mul(math.cos(math.pi/2 - angle/2) * math.sqrt(2 * abs(d)**2 * (1 - math.cos(angle))))
        self.tail += dir2.scalar_mul(math.sin(math.pi/2 - angle/2) * math.sqrt(2 * abs(d)**2 * (1 - math.cos(angle))))

class Coil:
    """!
    It saves a list of cables connected forming any shape
    """
    
    def __init__(self, cables: list):

        self.cables = cables

    def set_current(self, current: float):
        """!
        The same current is set for every Cable
        """

        for cable in self.cables:
            cable.set_current(current)

    def plot(self):

        x = []
        y = []
        z = []
        u = []
        v = []
        w = []

        for cable in self.cables:

            if(cable.current > 0):
                x.append(cable.tail.i)
                y.append(cable.tail.j)
                z.append(cable.tail.k)
                temp = cable.head - cable.tail
                temp = temp.unit()
                u.append(cable.head.i - cable.tail.i)
                v.append(cable.head.j - cable.tail.j)
                w.append(cable.head.k - cable.tail.k)
            
            else:
                u.append(cable.tail.i - cable.head.i)
                v.append(cable.tail.j - cable.head.j)
                w.append(cable.tail.k - cable.head.k)
                x.append(cable.head.i)
                y.append(cable.head.j)
                z.append(cable.head.k)

        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        ax.quiver(x, y, z, u, v, w)
        ax.set_zlim3d(-7, 7)                    # viewrange for z-axis should be [-4,4] 
        ax.set_ylim3d(-7, 7)                    # viewrange for y-axis should be [-2,2] 
        ax.set_xlim3d(-7, 7)                    # viewrange for x-axis should be [-2,2]

        plt.show()

    def rotate(self, angle: float, axis: RotationAxis):

        for cable in self.cables:
            cable.rotate(angle, axis)


