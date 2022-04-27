'''! spining simulator module
        Contains the physics of the project

Coded by Francisco Valbuena
GitHub: franyol
e-mail: f.valbuenao64@gmail.com
'''

# =============================================================================

# Standard library imports
import math
from re import U

# Third party imports
import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Local imports
import modules.spining_electromagnets as sp

# =============================================================================

def calc_cable_torque(current_cable: sp.Cable, magnetic_field: sp.Vector,  axis: sp.RotationAxis) -> sp.Vector:
        """! Calc the torque of every current section
        
        @param current_object has the Cables objects with the torque 
                              to be calculated
        @param magnetic_field Vector
        @param axis RotationAxis
        @return Vector with the torque
        """

        head_tail = current_cable.head - current_cable.tail
        crossfield = head_tail.cross(magnetic_field)
        force = crossfield.scalar_mul(current_cable.current)

        cable_centre = current_cable.head + current_cable.tail
        cable_centre = cable_centre.scalar_mul(1/2)

        # p is the closest point of the axis to the cable centre
        p = axis.Ae + axis.Ve.scalar_mul(axis.Ve.dot(cable_centre - axis.Ae))
        d = cable_centre - p

        return d.cross(force)



def calc_torque(current_object, magnetic_field: sp.Vector, axis: sp.RotationAxis) -> sp.Vector:
        """! Calc the torque of every current section
        
        @param current_object has the Cables objects with the torque 
                              to be calculated
        @param axis RotationAxis
        @return Vector with the torque
        """

        if(isinstance(current_object, sp.Cable)):
                response = calc_cable_torque(current_object, magnetic_field, axis)

        elif(isinstance(current_object, sp.Coil)):
                response = sp.Vector()
                for cable in current_object.cables:
                        response += calc_cable_torque(cable, magnetic_field, axis)

        return response


def plot_torque_vs_angle(current_object, magnetic_field: sp.Vector, axis: sp.RotationAxis) -> None:

        torques = []
        angles = np.linspace(0, 6.283, 100)

        for i in angles:

                current_object.rotate(6.283/100, axis)
                torques.append(abs(calc_torque(current_object, magnetic_field, axis)))

        fig = plt.figure()

        torques = np.array(torques)
        plt.plot(angles, torques)

        plt.show()

