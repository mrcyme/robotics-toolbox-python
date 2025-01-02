#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.Robot import Robot
from spatialmath import SE3


class Mycobot280(Robot):
    """
    Class that imports a Panda URDF model

    ``Panda()`` is a class which imports a Franka-Emika Panda robot definition
    from a URDF file.  The model describes its kinematic and graphical
    characteristics.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.URDF.Lite6()
        >>> print(robot)

    Defined joint configurations are:

    - qz, zero joint angle configuration, 'L' shaped configuration
    - qr, vertical 'READY' configuration
    - qs, arm is stretched out in the x-direction
    - qn, arm is at a nominal non-singular configuration

    .. codeauthor:: Jesse Haviland
    .. sectionauthor:: Peter Corke
    """

    def __init__(self):

        links, name, urdf_string, urdf_filepath = self.URDF_read(
            "elephantrobotics_description/mycobot_280_pi/urdf/mycobot_280_pi.urdf"
        )

        super().__init__(
            links,
            name=name,
            manufacturer="elephant_robotics",
            #gripper_links=links[7],
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        #self.grippers[0].tool = SE3(0, 0, 0)

        self.qdlim = np.array(
            [2*np.pi, 2.61799, 5.235988, 2*np.pi, 2.1642, 2.0*np.pi]
        )

        self.qr = np.array([0, -0.3, 0, -2.2, 0, 2.0])
        self.qz = np.zeros(6)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

"""
if __name__ == "__main__":  # pragma nocover

    r = Mycobot280()
    r.qz
    T = r.fkine(r.qz)
    r.plot(r.qr, backend="swift")
"""

