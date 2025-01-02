#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.Robot import Robot
from spatialmath import SE3
import roboticstoolbox as rtb

class Lite6(Robot):
    """
    Class that imports a Panda URDF model

    ``Panda()`` is a class which imports a Franka-Emika Panda robot definition
    from a URDF file.  The model describes its kinematic and graphical
    characteristics.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.URDF.Panda()
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
        filepath = "ufactory_description/lite6/urdf/lite6_with_gripper.urdf.xacro"
        #filepath = "ufactory_description/lite6/urdf/lite6.urdf.xacro"
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            filepath
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Ufactory",
            urdf_string=urdf_string,
            gripper_links=links[8],
            urdf_filepath=urdf_filepath,
        )
        self.grippers[0].tool = SE3(0, 0, 0.8)
        self.qdlim = np.array(
            [2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100, 3.0, 3.0]
        )

        self.qr = np.array([0, -0.6, 1, 0, 1, -1])
        self.qz = np.zeros(6)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)


if __name__ == "__main__":  # pragma nocover

    r = Lite6()
    r.qz
    T = r.fkine(r.qz)
    r.plot(r.qr, backend="swift")


