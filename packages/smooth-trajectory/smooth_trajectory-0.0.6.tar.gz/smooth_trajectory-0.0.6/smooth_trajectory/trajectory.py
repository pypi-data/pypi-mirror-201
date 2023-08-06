"""Smooth trajectory generation

Create a trajectory using polynomial smoothing. There are three polynomial
smoothing methods implemented: linear (1st order), cubic (3rd order), and
quintic (5th order).

Functions
---------
linear_polynomial()
cubic_polynomial()
quintic_polynomial()
time_scaling()
straight_trajectory()

"""

import numpy as np
import numpy.linalg as la
import scipy.linalg as sla


def _time_scaling(t: float, poly: np.polynomial.Polynomial):
    """Time scaling for the trajectory

    Map a given time value in [t_initial, t_final] to [0, 1] interval

    Parameters
    ----------
    t (float): Time value to be evaluated
    polynomial (np.polynomial.Polynomial): Smoothing polynomial

    Returns
    -------
    float: Time value mapped to [0, 1] interval

    """

    return poly(t), poly.deriv()(t)


def polynomial(
    t_initial: float, t_final: float, order: int = 3
) -> np.polynomial.Polynomial:
    """Fit a smooting polynomial

    Fit a linear, cubib or quintic polynomial between the initial and final
    time values

    (order = 1) a0 + a1 * t
    (order = 3) a0 + a1 * t + a2 * t**2 + a3 * t**3
    (order = 5) a0 + a1 * t + a2 * t**2 + a3 * t**3 + a4 * t**4 + a5 * t**5

    Parameters
    ----------
    t_initial (float): Initial time value
    t_final (float): Final time value
    order (int)

    Returns
    -------
    (np.polynomial.Polynomial): Numpy polynomial constructed from the
                                coefficients calculated using the input

    """

    if order == 1:
        coef_matrix = np.array([[1.0, t_initial], [1.0, t_final]])

        val = np.array([0.0, 1.0])
    elif order == 3:
        coef_matrix = np.array(
            [
                [1.0, t_initial, t_initial**2, t_initial**3],
                [0.0, 1.0, 2.0 * t_initial, 3.0 * t_initial**2],
                [1.0, t_final, t_final**2, t_final**3],
                [0.0, 1.0, 2.0 * t_final, 3.0 * t_final**2],
            ]
        )

        val = np.array([0.0, 0.0, 1.0, 0.0])
    elif order == 5:
        coef_matrix = np.array(
            [
                [
                    1.0,
                    t_initial,
                    t_initial**2,
                    t_initial**3,
                    t_initial**4,
                    t_initial**5,
                ],
                [
                    0.0,
                    1.0,
                    2.0 * t_initial,
                    3.0 * t_initial**2,
                    4 * t_initial**3,
                    5 * t_initial**4,
                ],
                [
                    0.0,
                    0.0,
                    2.0,
                    6.0 * t_initial,
                    12.0 * t_initial**2,
                    20.0 * t_initial**3,
                ],
                [1.0, t_final, t_final**2, t_final**3, t_final**4, t_final**5],
                [
                    0.0,
                    1.0,
                    2.0 * t_final,
                    3.0 * t_final**2,
                    4.0 * t_final**3,
                    5.0 * t_final**4,
                ],
                [
                    0.0,
                    0.0,
                    2.0,
                    6.0 * t_final,
                    12.0 * t_final**2,
                    20.0 * t_final**3,
                ],
            ]
        )

        val = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    else:
        raise ValueError("The order should be 1, 3 or 5")

    # Calculate the coefficients of the smoothing polynomial using least squares
    coeffs = la.inv(coef_matrix) @ val

    return np.polynomial.Polynomial(coeffs)


def straight_trajectory(
    t: float,
    poly: np.polynomial.Polynomial,
    initial_conf: np.array,
    final_conf: np.array,
) -> np.array:
    """Straight trajectory in SE(3)

    Create a straight line trajectory in SE(3)

    Parameters
    ----------
    t (float): Time value
    poly (np.polynomial.Polynomial): The smoothing polynomial for the time scaling
    initial_conf (np.ndarray): Initial configuration in SE(3)
    final_conf (np.ndarray): Final configuration in SE(3)

    Returns
    -------
    (np.ndarray): Configuration represented in SE(3) at time t

    TODO check the second return value (twist) and add to the docstring

    """

    # Map the given time to [0, 1] interval
    scaled_time, d_scaled_time = _time_scaling(t, poly)

    return (
        initial_conf
        @ sla.expm(sla.logm(la.inv(initial_conf) @ final_conf) * scaled_time),
        initial_conf
        @ sla.logm(la.inv(initial_conf) @ final_conf)
        @ sla.expm(sla.logm(la.inv(initial_conf) @ final_conf) * scaled_time)
        * d_scaled_time,
    )

def joint_trajectory(t: float, poly: np.polynomial.Polynomial, initial_pos: float, final_pos: float) -> float:
    """Straight trajectory in joint space
    
    Create a smooth straight line trajectory in Eucledean space

    Parameters
    ----------
    t (float): Time value
    poly (np.polynomial.Polynomial): The smoothing polynomial for the time scaling
    initial_pos (float): Initial position in Euclidean space
    final_pos (float): Final position in Euclidean space

    Returns
    -------
    (float): Position on the straight trajectory
    (float): Velocity on the straight trajectory
    
    """

    # Map the given time to [0, 1] interval
    scaled_time, d_scaled_time = _time_scaling(t, poly)

    return (initial_pos + scaled_time * (final_pos - initial_pos),
            d_scaled_time * (final_pos - initial_pos))