'''! spining simulator module
        Contains the physics of the project

Coded by Francisco Valbuena
GitHub: franyol
e-mail: f.valbuenao64@gmail.com
'''

# =============================================================================

# Standard library imports
import os
import sys

# Third party imports
import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Local imports
import modules.spining_electromagnets as sp

# =============================================================================

def calc_cable_torque(current_cable: sp.Cable, 
                      magnetic_field: sp.Vector,  
                      axis: sp.RotationAxis) -> sp.Vector:
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



def calc_torque(current_object, 
                magnetic_field: sp.Vector, 
                axis: sp.RotationAxis) -> sp.Vector:
        """! Calc the torque of every current section
        
        @param current_object has the Cables objects with the torque 
                              to be calculated
        @param axis RotationAxis
        @return Vector with the torque
        """

        if(isinstance(current_object, sp.Cable)):
                response = calc_cable_torque(current_object, 
                                             magnetic_field, 
                                             axis)

        elif(isinstance(current_object, sp.Coil)):
                response = sp.Vector()
                for cable in current_object.cables:
                        response += calc_cable_torque(cable, 
                                                      magnetic_field, 
                                                      axis)

        elif(isinstance(current_object, sp.Spinner)):
                response = sp.Vector()
                for coil in current_object.coils:
                        for cable in coil.cables:
                                response += calc_cable_torque(cable, 
                                                              magnetic_field, 
                                                              axis)

        return response


def plot_torque_vs_angle(current_object: sp.Coil, 
                         magnetic_field: sp.Vector, 
                         axis: sp.RotationAxis) -> None:

        torques = []
        angles = np.linspace(0, 6.283, 100)

        for _ in angles:

                current_object.rotate(6.283/100, axis)
                torques.append(abs(calc_torque(current_object, 
                                               magnetic_field, 
                                               axis)))

        fig = plt.figure()
        plt.xlabel("angle (rad)")
        plt.ylabel("torque (Nm)")

        torques = np.array(torques)
        plt.plot(angles, torques)

        plt.show()


def simulate_movement(spinners: list, 
                      magnetic_field: sp.Vector, 
                      sim_currents: list, 
                      delta_time: float) -> None:
        """! Generate video frames and graphs from a current list of values in time
        
        @param spiners list of the spinner objects in the simulation
        @param magnetic_field Vector with the magnetic field that 
                              generates rotation
        @param sim_currents list of floats with the currents of every coil at
                            every frame (ex: if the spinners list has 3 Spinner
                            elements, then the list dimentions must be
                            sim_currents dimentions = [3, NUMB_OF_COILS, NUMB_OF_FRAMES])
        @param delta_time float with the time between every sim frame
        @return None
        """


        # Check that the dimensions are ok
        for i in range(len(sim_currents)-1):
                if len(sim_currents[i][0]) != len(sim_currents[i+1][0]):
                        print("[ERROR] Dimensions error in sim_currents")
                        return
        if len(sim_currents) != len(spinners):
                print("[ERROR] spinners and sim_currents dimensions must match")
                return

        #Creates frames dir if it does not exist
        if not os.path.exists("frames"):
            os.mkdir('frames')

        #Remove old frames
        for f in os.listdir('frames'):
            os.remove(os.path.join('frames', f))

        friction = 0.148/(10**6)
        # Taken from a cilinder of 4cm radious and 10g mass
        inertia_moment = 500/(10**6)
        torque = 0
        a = 0
        w = 0
        delta_w = 0
        theta = 0
        delta_theta = 0

        percent = 0

        for i in range(len(sim_currents[0][0])):
                # In the frame i

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                
                for j in range(len(spinners)):
                        # In the spinner j
                        for k in range(len(spinners[j].coils)):
                                # In the coil k

                                # Set current
                                spinners[j].coils[k].set_current(sim_currents[j][k][i])
                        
                        # Calculate torque
                        temp = calc_torque(spinners[j], magnetic_field, spinners[j].axis)

                        # Get torque in the rotation axis
                        torque = temp.dot(spinners[j].axis.Ve)

                        # Calculate torque loss (water friction like)
                        loss = friction * w**2 * torque/abs(torque)

                        # Calculate acceleration
                        a = (torque - loss)/inertia_moment

                        # Calculate angular velocity
                        delta_w = a * delta_time
                        w += delta_w

                        # Calculate theta
                        delta_theta = w * delta_time
                        theta += delta_theta

                        # Rotate
                        spinners[j].rotate(delta_theta)

                        # Make frame plots
                        for coil in spinners[j].coils:
                                coil.plot(ax)

                
                # Save frame
                plt.savefig("frames/frame"+str(i))

                percent += 100/len(sim_currents[0][0])
                print("creating video: [ " + str(int(percent)) + "% ]")
                sys.stdout.write("\033[F")

                plt.close()
                # Make graphs

        print("creating video: [ 100% ]")

        # Save graphs
        # Save video
        first_frame = cv.imread("frames/frame0.png")
        height, width, _ = first_frame.shape

        fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv.VideoWriter('simulation.mp4', fourcc, int(1/delta_time), (width, height))
        for j in range(len(sim_currents[0][0])):
                img = cv.imread("frames/frame" + str(j) + ".png")
                video.write(img)

        video.release()

