# -*- coding: utf-8 -*-

"""Groma-Ungár-Wilkens (GUW) model.

In 1988, I. Groma, T. Ungár and M. Wilkens [1]_ proposed a model that
has been simplified here as follows:

.. math::

   \\ln\\left[ A(L) \\right] = - \\Lambda \\rho L^2 \\left[
   \\ln\\left( \\frac{R_{eff}}{L} \\right) - \\frac{\\delta}{2}
   \\Lambda \\rho L^2 \\ln^2\\left( \\frac{R_0}{L} \\right) \\right]

With:

.. math::

   \\Lambda = \\frac{\\pi}{2} g^2 b^2 C_g

* :math:`A` Fourier amplitude.

* :math:`L` Fourier variable (:math:`\\mathrm{m}`).

* :math:`\\vec{g}` diffraction vector (:math:`\\mathrm{m}^{-1}`).

* :math:`\\vec{b}` Burgers vector (:math:`\\mathrm{m}`).

* :math:`C_g` contrast factor.

* :math:`\\rho` dislocation density (:math:`\\mathrm{m}^{-2}`).

* :math:`R_{eff}` effective radius (:math:`\\mathrm{m}`).

* :math:`\\delta` fluctuation.

* :math:`R_0` radius (:math:`\\mathrm{m}`).

For this model, the parameters to be adjusted are :math:`\\rho`,
:math:`R_{eff}`, :math:`\\delta` and :math:`R_0`.

.. [1] I. Groma, T. Ungár and M. Wilkens.
   Asymmetric X-ray line broadening of plastically deformed crystals.
   I. Theory, Journal of Applied Crystallography 21 (1) (1988) 47-54.

"""

from logging import getLogger

import numpy as np


logger = getLogger(__name__)


def guide(transform):
    """Return a guide for the model parameters.

    Parameters
    ----------
    transform : dict
        Fourier transform data.

    Returns
    -------
    dict
        Parameter names, min, max and real values.

    """
    logger.debug("retrieving distribution parameters")
    density = transform['distribution']['density']
    distance = 1/np.sqrt(density)

    logger.debug("assembling parameter guide")
    data = {
        'names': ('density', 'radius_eff', 'fluctuation', 'radius_0'),
        'max': (density*100, distance/10, 3, distance/10),
        'min': (density/100, distance*1000, 0, distance*1000),
        'real': (density, None, None, None),
    }
    return data


def model(transform, harmonic, limit=None):
    """Return the Fourier amplitude function.

    Parameters
    ----------
    transform : dict
        Fourier transform data.
    harmonic : int
        Harmonic of the diffraction vector.
    limit : int
        Index of the last Fourier variable.

    Returns
    -------
    Callable
        Function that takes parameter values and returns amplitudes.

    """
    data = {}

    logger.debug("defining constant quantities")
    data['L'] = np.array(transform['coefficients']['variable'])
    if limit:
        data['L'] = data['L'][:limit]
    data['b_uvw'] = np.array(transform['diffraction']['b_uvw'])
    data['g_hkl'] = np.array(transform['diffraction']['g_hkl'])
    data['g_vec'] = harmonic * data['g_hkl']/transform['diffraction']['cell']
    data['b_vec'] = data['b_uvw'] * transform['diffraction']['cell']/2
    data['g_len'] = np.linalg.norm(data['g_vec'])
    data['b_len'] = np.linalg.norm(data['b_vec'])
    data['C'] = transform['diffraction']['contrast']
    data['Lambda'] = np.pi/2 * data['g_len']**2 * data['b_len']**2 * data['C']
    data['cst1'] = data['Lambda'] * data['L']**2

    def amplitude(density, radius_eff, fluctuation, radius_0):
        if density < 0 or radius_eff < 0 or radius_0 < 0:
            return np.inf
        term_1 = data['cst1'] * density
        term_2 = np.log(radius_eff / data['L'])
        term_3 = np.log(radius_0 / data['L'])
        return np.exp(-term_1*(term_2 - fluctuation/2*term_1*term_3**2))

    return amplitude
