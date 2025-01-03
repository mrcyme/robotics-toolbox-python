#!/usr/bin/env python

import numpy as np
from spatialmath import SE3, base
import math
from typing import Union
from roboticstoolbox.fknm import Angle_Axis

ArrayLike = Union[list, np.ndarray, tuple, set]


def angle_axis(T, Td):

    try:
        e = Angle_Axis(T, Td)
    except BaseException:
        e = angle_axis_python(T, Td)

    return e


def angle_axis_python(T, Td):
    e = np.empty(6)
    e[:3] = Td[:3, -1] - T[:3, -1]
    R = Td[:3, :3] @ T[:3, :3].T
    li = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])

    if base.iszerovec(li):
        # diagonal matrix case
        if np.trace(R) > 0:
            # (1,1,1) case
            a = np.zeros((3,))
        else:
            a = np.pi / 2 * (np.diag(R) + 1)
    else:
        # non-diagonal matrix case
        ln = base.norm(li)
        a = math.atan2(ln, np.trace(R) - 1) * li / ln

    e[3:] = a

    return e


def cp_servo(
    wTe, wTep, gain: Union[float, ArrayLike] = 1.0, threshold=0.1, method="rpy"
):
    """
    Cartesian position-based servoing.

    Returns the end-effector velocity which will cause the robot to approach
    the desired pose.

    :param wTe: The current pose of the end-effecor in the base frame.
    :type wTe: SE3 or ndarray
    :param wTep: The desired pose of the end-effecor in the base frame.
    :type wTep: SE3 or ndarray
    :param gain: The gain for the controller. Can be vector corresponding to each
        axis, or scalar corresponding to all axes.
    :type gain: float, or array-like
    :param threshold: The threshold or tolerance of the final error between
        the robot's pose and desired pose
    :type threshold: float
    :param method: The method used to calculate the error. Default is 'rpy' -
        error in the end-effector frame. 'angle-axis' - error in the base frame
        using angle-axis method.
    :type method: string: 'rpy' or 'angle-axis'

    :returns v: The velocity of the end-effecotr which will casue the robot
        to approach wTep
    :rtype v: ndarray(6)
    :returns arrived: True if the robot is within the threshold of the final
        pose
    :rtype arrived: bool

    """

    if isinstance(wTe, SE3):
        wTe = wTe.A

    if isinstance(wTep, SE3):
        wTep = wTep.A

    if method == "rpy":
        # Pose difference
        eTep = np.linalg.inv(wTe) @ wTep
        e = np.empty(6)

        # Translational error
        e[:3] = eTep[:3, -1]

        # Angular error
        e[3:] = base.tr2rpy(eTep, unit="rad", order="zyx", check=False)
    else:
        e = angle_axis(wTe, wTep)

    if base.isscalar(gain):
        k = gain * np.eye(6)
    else:
        k = np.diag(gain)

    v = k @ e
    arrived = True if np.sum(np.abs(e)) < threshold else False

    return v, arrived

def jp_servo(q, q_dest, gain: Union[float, ArrayLike] = 1.0, threshold=0.1):
    """
    joint space position-based servoing.

    Returns the joint velocities which will cause the robot to approach the desired joint positions.
    
    :param q: The current joint positions of the robot.
    :type q: ndarray
    :param qd: The desired joint positions of the robot.
    :type qd: ndarray
    :param gain: The gain for the controller. Can be a scalar or a vector corresponding to each joint.
    :type gain: float, or array-like
    :param threshold: The threshold or tolerance of the final error between the robot's joint positions and desired joint positions.
    :type threshold: float
    :returns qdd: The joint velocities which will cause the robot to approach qd.
    :rtype qdd: ndarray(n)
    :returns arrived: True if the robot is within the threshold of the final joint positions.
    :rtype arrived: bool
    """
    # Joint position error
    e = q_dest - q
    
    if base.isscalar(gain):
        k = gain * np.eye(len(q))
    else:
        k = np.diag(gain)
    
    # Joint velocities
    qdd = k @ e
    
    arrived = True if np.sum(np.abs(e)) < threshold else False
    
    return qdd, arrived

def pid_servo(wTe, wTep, prev_error, integral_error, dt, gains, threshold=0.1, method="rpy"):
    """
    Position-based servoing with PID control.

    :param wTe: Current pose of the end-effector in the base frame.
    :type wTe: SE3 or ndarray
    :param wTep: Desired pose of the end-effector in the base frame.
    :type wTep: SE3 or ndarray
    :param prev_error: Previous error in pose from last control step.
    :type prev_error: ndarray
    :param integral_error: Accumulated integral error.
    :type integral_error: ndarray
    :param dt: Time interval between the current and the previous control step.
    :type dt: float
    :param gains: Tuple of gains for PID controller (Kp, Ki, Kd).
    :type gains: tuple
    :param threshold: Tolerance of the final error between robot's pose and desired pose.
    :type threshold: float
    :param method: Method used to calculate the error (default 'rpy' uses roll-pitch-yaw).
    :type method: str

    :returns: Tuple containing the calculated velocity and a boolean indicating if the target has been reached.
    :rtype: (ndarray, bool)
    """

    if isinstance(wTe, SE3):
        wTe = wTe.A

    if isinstance(wTep, SE3):
        wTep = wTep.A

    if method == "rpy":
        eTep = np.linalg.inv(wTe) @ wTep
        error = np.empty(6)
        error[:3] = eTep[:3, -1]
        error[3:] = base.tr2rpy(eTep, unit="rad", order="zyx", check=False)
    else:
        error = angle_axis(wTe, wTep)

    Kp, Ki, Kd = gains
    if np.isscalar(Kp):
        Kp = Kp * np.eye(6)
        Ki = Ki * np.eye(6)
        Kd = Kd * np.eye(6)

    # Update integral and derivative errors
    integral_error += error * dt
    derivative_error = (error - prev_error) / dt

    # Calculate control command
    v = Kp @ error + Ki @ integral_error + Kd @ derivative_error

    # Check if arrived within threshold
    arrived = np.linalg.norm(error) < threshold

    return v, arrived, error, integral_error

