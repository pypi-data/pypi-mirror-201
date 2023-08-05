# -*- coding: utf-8 -*-

"""Numerical diffractometers.

This package gathers the implementations of the X-ray diffraction
simulators. These return the amplitude of the Fourier transform of
the diffracted intensity. According to the kinematical theory of
X-ray scattering [1]_, the Fourier transform is calculated from
the displacement field of the defects:

.. math::

   A(L) = \\frac{1}{V} \\int_V \\exp\\left(2 \\pi i \\vec{g} \\cdot
   \\left[\\vec{u}(\\vec{r}+\\vec{L}) - \\vec{u}(\\vec{r})\\right]
   \\right) d\\vec{r}

With:

* :math:`A` Fourier transform amplitude.

* :math:`\\vec{L}` Fourier variable vector, perpendicular to the
  diffracting lattice planes (:math:`\\mathrm{m}`).

* :math:`V` volume of the region of interest (:math:`\\mathrm{m}^{3}`).

* :math:`\\vec{g}` diffraction vector (:math:`\\mathrm{m}^{-1}`).

* :math:`\\vec{u}` displacement field (:math:`\\mathrm{m}`).

The resulting displacement field at a point is obtained by summing
the contributions of each dislocation. The displacement field induced
by a single screw or edge dislocation is given respectively by: [2]_

.. math::

   \\vec{u}_{\\text{screw}} = \\left( \\begin{array}{c}
   0 \\\\
   0 \\\\
   \\frac{b}{2 \\pi} \\arctan\\left(\\frac{y}{x}\\right)
   \\end{array} \\right)

and

.. math::

   \\vec{u}_{\\text{edge}} = \\left( \\begin{array}{c}
   \\frac{b}{2 \\pi} \\left( \\arctan\\left(\\frac{y}{x}\\right) +
   \\frac{xy}{2(1-\\nu)(x^2+y^2)} \\right) \\\\
   - \\frac{b}{8 \\pi (1 - \\nu)} \\left( (1-2\\nu) \\ln\\left(
   \\frac{x^2 + y^2}{b^2} \\right) - \\frac{2 y^2}{x^2 + y^2}
   \\right) \\\\
   0
   \\end{array} \\right)

With:

* :math:`b` Burgers vector length (:math:`\\mathrm{m}`).

* :math:`x` dislocation x-coordinate with respect to the observation
  position (:math:`\\mathrm{m}`).

* :math:`y` dislocation y-coordinate with respect to the observation
  position (:math:`\\mathrm{m}`).

* :math:`\\nu` Poisson's number.

.. [1] B. E. Warren.
   X-Ray diffraction. Dover Publications, 1990. ISBN: 978-0-48-666317-3.

.. [2] F. R. N. Nabarro.
   Theory of crystal dislocations. Oxford Clarendon Press, 1967.

"""
