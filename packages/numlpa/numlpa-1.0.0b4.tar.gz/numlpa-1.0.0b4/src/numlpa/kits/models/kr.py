# -*- coding: utf-8 -*-

"""Krivoglaz-Ryaboshapka (KR) model.

In 1963, M. Krivoglaz and K. Ryaboshapka [1]_ proposed the following
equation:

.. math::

   \\ln\\left[ A(L) \\right] = - \\Lambda \\rho L^2 \\ln\\left(
   \\frac{R}{|\\vec{g} \\cdot \\vec{b} \\sin(\\psi)| L} \\right)

With:

.. math::

   \\Lambda = \\frac{\\pi}{2} g^2 b^2 C_g

* :math:`A` Fourier amplitude.

* :math:`L` Fourier variable (:math:`\\mathrm{m}`).

* :math:`\\vec{g}` diffraction vector (:math:`\\mathrm{m}^{-1}`).

* :math:`\\vec{b}` Burgers vector (:math:`\\mathrm{m}`).

* :math:`C_g` contrast factor.

* :math:`\\rho` dislocation density (:math:`\\mathrm{m}^{-2}`).

* :math:`R` radius (:math:`\\mathrm{m}`).

* :math:`\\psi` angle between :math:`\\vec{g}` and the dislocation line vector.

For this model, the parameters to be adjusted are :math:`\\rho` and :math:`R`.

.. [1] M. Krivoglaz, and K. Ryaboshapka.
   Theory of x-ray scattering by crystals containing dislocations,
   screw and edge dislocations randomly distributed throughout the
   crystal. Fiz. Metallov. Metalloved 15 (1963) 18-31.

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
        'names': ('density', 'radius'),
        'max': (density*100, distance/10),
        'min': (density/100, distance*1000),
        'real': (density, None),
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
    data['z_uvw'] = np.array(transform['diffraction']['z_uvw'])
    data['z_uni'] = data['z_uvw'] / np.linalg.norm(data['z_uvw'])
    data['g_uni'] = data['g_hkl'] / np.linalg.norm(data['g_hkl'])
    data['psi'] = np.abs(np.arccos(data['g_uni'].dot(data['z_uni'])))
    data['g_dot_b'] = data['g_vec'].dot(data['b_vec'])
    data['cst1'] = data['Lambda'] * data['L']**2
    data['cst2'] = data['L'] * np.abs(data['g_dot_b'] * np.sin(data['psi']))

    def amplitude(density, radius):
        if density < 0 or radius < 0:
            return np.inf
        return np.exp(-data['cst1']*density*np.log(radius/data['cst2']))

    return amplitude
