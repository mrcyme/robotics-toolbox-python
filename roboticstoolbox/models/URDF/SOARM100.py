#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.Robot import Robot
from spatialmath import SE3
import roboticstoolbox as rtb

class SOARM100(Robot):
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
        filepath = "huggingface_description/SO-ARM100/urdf/SO_5DOF_ARM100_8j_URDF.SLDASM.urdf"
        #filepath = "ufactory_description/lite6/urdf/lite6.urdf.xacro"
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            filepath
        )

        super().__init__(
            links,
            name=name,
            manufacturer="HuggingFace",
            urdf_string=urdf_string,
            gripper_links=links[6],
            urdf_filepath=urdf_filepath,
        )
        #self.grippers[0].tool = SE3(0, 0, 0.4)
        self.qdlim = np.array(
            [2.1750, 2.1750, 2.1750, 2.1750, 2.6100]
        )

        self.qr = np.array([0, -0.6, 1, 0, 1])
        self.qz = np.zeros(5)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)


if __name__ == "__main__":  # pragma nocover

    r = SOARM100()
    r.qz
    T = r.fkine(r.qz)
    r.plot(r.qr, backend="swift")


