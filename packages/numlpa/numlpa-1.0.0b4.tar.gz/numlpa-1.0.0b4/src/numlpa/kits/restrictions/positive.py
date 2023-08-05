# -*- coding: utf-8 -*-

"""Positive restriction.

This module allows to restrict the interval of the Fourier variable to
the part where the amplitude is strictly positive. An example of the
application of this restriction is given below:

.. image:: ../figures/restrictions/positive.svg
   :width: 600

"""


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
    n_positive = 0
    while n_positive < len(variable) and amplitude[n_positive] > 0:
        n_positive += 1
    return n_positive
