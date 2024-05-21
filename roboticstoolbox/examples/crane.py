# %%
import swift
from math import pi
import roboticstoolbox as rtb
from spatialgeometry import Mesh, Axes
from spatialmath import SE3, Twist3
from spatialmath.base import *

import numpy as np

rails = Mesh(
    filename=str("/home/simeon/Documents/digitalFabrication/FabAcademy2024/final project/cnc/base.stl"),
    color=[34, 143, 201],
    scale=(0.001,) * 3,
)
z_carriage = Mesh(
    filename=str("/home/simeon/Documents/digitalFabrication/FabAcademy2024/final project/cnc/z_carriage.stl"),
    color=[31, 184, 72],
    scale=(0.001,) * 3,
    

)
rotating_end_effector = Mesh(
    filename=str("/home/simeon/Documents/digitalFabrication/FabAcademy2024/final project/cnc/rotating_end_effector.stl"),
    color=[240, 103, 103],
    scale=(0.001,) * 3,
)
fixed_end_effector = Mesh(
    filename=str("/home/simeon/Documents/digitalFabrication/FabAcademy2024/final project/cnc/fixed_end_effector.stl"),
    color=[240, 103, 50],
    scale=(0.001,) * 3,
)
env = swift.Swift()
env.launch()
axes = Axes(length=0.1, pose=SE3(0.12, 0.5, 0.0))
env.add(axes)
env.add(rails)
env.add(z_carriage)
env.add(rotating_end_effector)
env.add(fixed_end_effector)



# %%
import time
import numpy as np
rotating_end_effector.T = SE3(0.4, 0.0, 0.0)
fixed_end_effector.T = SE3(0.0, 0.0, 0.0)
z_carriage.T = SE3(0.0, 0.0, 0.0)

print(SE3(0.0, 0.0, 0.0).A[:, 2])
rotation_axis = np.array([0.13, 0.5, 0])
#rotation_axis = [0, 0, 0]
add_vector = np.array([0.001, 0.001, 0])

i = 1
while True:
    #rotating_end_effector.T =  rotating_end_effector.T *Twist3.UnitRevolute([0,0,1], rotation_axis ).SE3(np.radians(20))
    #rotating_end_effector.T = rotating_end_effector.T * SE3(0.001, 0.001, 0.0)
    Tep = T = SE3(-0.13, -0.5, 0.0) * SE3.RPY([0, 0, 0], order='xyz') * SE3.Rz(-i*10, unit='deg')
    rotating_end_effector.T = Tep
    #rotating_end_effector.T = rotating_end_effector.T*Twist3.UnitRevolute([0,0,1], rotation_axis).SE3(np.radians(180))
    axes.T = SE3(*rotation_axis)
    
    #print(rotation_axis)
    #fixed_end_effector.T = fixed_end_effector.T * SE3(0.001, 0.001, 0.0)
    #rotating_end_effector.T = rotating_end_effector.T * Twist3.UnitRevolute([0, 0, 1], rotation_axis).SE3(np.radians(10))
    #rotation_axis = add_vector
    #rotation_axis = np.add(rotation_axis, add_vector) 
    #rotation_axis = add_vector
    #z_carriage.T = z_carriage.T * SE3(0.001, 0.0, 0.0)
    env.step()
    time.sleep(0.1)
    i += 1

# %%
