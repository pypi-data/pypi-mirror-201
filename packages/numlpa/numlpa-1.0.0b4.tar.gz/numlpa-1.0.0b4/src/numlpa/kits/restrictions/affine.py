# -*- coding: utf-8 -*-

"""Affine restriction.

This module restricts the interval of the Fourier variable to the part
where the transformed amplitude :math:`\\log[A(L)]/L^2` follows an
affine behavior when viewed with the Fourier variable axis in
logarithmic scale. An example of the application of this restriction is
given below:

.. image:: ../figures/restrictions/affine.svg
   :width: 600

"""

import numpy as np


def limit(variable, amplitude):
    """Return the number of points to keep.

    Parameters
    ----------
    variable : list of float
        Fourier variable values.
    amplitudes : list of float
        Amplitude values.

    Returns
    -------
    int
        Number of points to keep.

    """
    n_positive = 1
    while n_positive < len(variable) and amplitude[n_positive] > 0:
        n_positive += 1
    variable = variable[:n_positive]
    amplitude = amplitude[:n_positive]
    x_list = np.log(variable)
    y_list = np.log(amplitude) / np.array(variable)**2
    n_p = n_affine(x_list, y_list)
    return n_p


def n_affine(x_list, y_list, tol=0.005):
    """Return the number of points to keep.

    Parameters
    ----------
    x_list : list of float
        Fourier variable values after transformation.
    y_list : list of float
        Amplitude values after transformation.

    Returns
    -------
    int
        Number of points to keep.

    """
    n_p = 3
    stop = False
    while n_p < len(x_list) and not stop:
        n_p += 1
        weights = np.ones(n_p)
        weighted = np.stack((x_list[:n_p], weights)).T
        error = np.linalg.lstsq(weighted, y_list[:n_p], rcond=None)[1][0]
        deviation = np.sqrt(error/(n_p-1))
        if deviation/np.ptp(y_list[:n_p]) > tol:
            stop = True
    return n_p - 1
