# -*- coding: utf-8 -*-

"""Wilkens model.

In 1970, M. Wilkens [1]_ proposed a model that has been simplified here
as follows:

.. math::

   \\ln\\left[ A(L) \\right] = - \\Lambda \\rho L^2 f\\left(
   \\frac{L}{R_e} \\right)

With:

.. math::

   \\Lambda = \\frac{\\pi}{2} g^2 b^2 C_g

.. math::

    f(\\eta) =
    \\begin{cases}
    - \\ln(\\eta) + \\frac{7}{4} - \\ln(2) + \\frac{512}{90 \\pi}
    \\eta^{-1} \\\\
    + \\frac{2}{\\pi} \\left( 1 - \\frac{1}{4}\\eta^{-2} \\right)
    \\int_0^\\eta \\frac{\\arcsin(V)}{V} dV \\\\
    - \\left( \\frac{769}{180} \\eta^{-1} + \\frac{41}{90} \\eta +
    \\frac{2}{90}\\eta^3 \\right) \\frac{\\sqrt{ 1 - \\eta^2 }}{\\pi}
    & \\forall \\eta \\leq 1 \\\\[3mm]
    \\frac{512}{90 \\pi} \\eta^{-1} - \\left( \\frac{11}{24} +
    \\frac{1}{4} \\ln(2) \\eta \\right) \\eta^{-2}
    & \\forall \\eta > 1
    \\end{cases}

* :math:`A` Fourier amplitude.

* :math:`L` Fourier variable (:math:`\\mathrm{m}`).

* :math:`\\vec{g}` diffraction vector (:math:`\\mathrm{m}^{-1}`).

* :math:`\\vec{b}` Burgers vector (:math:`\\mathrm{m}`).

* :math:`C_g` contrast factor.

* :math:`\\rho` dislocation density (:math:`\\mathrm{m}^{-2}`).

* :math:`R_e` radius (:math:`\\mathrm{m}`).

For this model, the parameters to be adjusted are :math:`\\rho` and
:math:`R_e`.

.. [1] M. Wilkens.
   Fundamental aspects of dislocation theory. Ed. by J. A. Simmons,
   R. de Wit, and R. Bullough. Vol. 2. U.S. National Bureau of
   Standards, 1970, pp. 1195-1221.

"""

from logging import getLogger

import numpy as np
import scipy.integrate


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
    data['cst1'] = data['Lambda'] * data['L']**2

    def amplitude(density, radius_e):
        if density < 0 or radius_e < 0:
            return np.inf
        return np.exp(-data['cst1']*density*vectorized_f(data['L']/radius_e))

    return amplitude


def wilkens_f(eta):
    """Return the result of the Wilkens intermediate function f.

    Parameters
    ----------
    eta : float
        Parameter of the Wilkens intermediate function f.

    Returns
    -------
    float
        Result of the Wilkens intermediate function f.

    """
    eta2 = eta**2

    def aux(val):
        if val == 0:
            return 1
        return np.arcsin(val)/val

    if eta < 1:
        result = (
            7/4 - np.log(eta) - np.log(2) + 512/90/np.pi/eta
            + 2/np.pi*(1-1/4/eta2)*scipy.integrate.quad(aux, 0, eta)[0]
            - 1/np.pi*(769/180/eta+41*eta/90+2*eta2*eta/90)*(1-eta2)**(1/2)
            - 1/np.pi*(11/12/eta2+7/2+eta2/3)*np.arcsin(eta) + eta2/6
        )
    else:
        result = 512/90/np.pi/eta - (11/24+np.log(2)*eta/4)/eta2
    return result


vectorized_f = np.vectorize(wilkens_f)
