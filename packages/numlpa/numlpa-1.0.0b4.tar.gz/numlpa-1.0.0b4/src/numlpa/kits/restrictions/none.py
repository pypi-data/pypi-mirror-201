# -*- coding: utf-8 -*-

"""No restriction.

This module does not apply any restriction on the Fourier variable
interval for model fitting. As shown below, the restricted interval is
equal to the original interval:

.. image:: ../figures/restrictions/none.svg
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
    _ = amplitude
    return len(variable)
