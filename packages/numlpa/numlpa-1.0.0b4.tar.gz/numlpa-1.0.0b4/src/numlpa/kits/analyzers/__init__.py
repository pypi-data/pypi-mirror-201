# -*- coding: utf-8 -*-

"""Spatial analyzers.

This package gathers the implementations of the spatial analyzers.
These compute the strain energy contained in a dislocation sample and
the distribution of dislocations around a dislocation. The strain
energy contained in the region of interest is given by:

.. math::

   E_T = \\sum_{i=1}^n E_{S, i} + \\frac{1}{2} \\sum_{i=1}^n
   \\sum_{\\substack{j=1 \\\\ j \\neq i}}^n E_{I, i, j}

With:

* :math:`E_T` total energy per unit length (:math:`\\mathrm{J.m}^{-1}`).

* :math:`E_{S, i}` self energy per unit length of the dislocation
  :math:`i` (:math:`\\mathrm{J.m}^{-1}`).

* :math:`E_{I, i, j}` interaction energy per unit length of :math:`i`
  and :math:`j` (:math:`\\mathrm{J.m}^{-1}`).

* :math:`n` number of dislocations in the region of interest.

The self energy of a dislocation and the interaction energy between two
dislocations are expressed respectively by: [1]_ [2]_

.. math::

   E_{S,i} = \\begin{cases}
   \\frac{G b^2}{4 \\pi} \\ln\\left( \\frac{r_{\\text{ROI}}}{r_0}
   \\right) & \\text{for screw dislocations} \\\\
   \\frac{G b^2}{4 \\pi (1-\\nu)} \\ln\\left( \\frac{r_{
   \\text{ROI}}}{r_0} \\right) & \\text{for edge dislocations}
   \\end{cases}

and

.. math::

   E_{I, i, j} = \\begin{cases}
   \\vec{b}_i \\cdot \\vec{b}_j \\frac{G}{2 \\pi} \\ln\\left(
   \\frac{r_{\\text{ROI}}}{d_{i, j}} \\right) &
   \\text{for screw dislocations} \\\\
   \\vec{b}_i \\cdot \\vec{b}_j \\frac{G}{2 \\pi (1-\\nu)}
   \\ln\\left( \\frac{r_{ \\text{ROI}}}{d_{i, j}} \\right) &
   \\text{for edge dislocations}
   \\end{cases}

With:

* :math:`G` shear modulus (:math:`\\mathrm{Pa}`).

* :math:`\\vec{b}` Burgers vector (:math:`\\mathrm{m}`).

* :math:`r_{\\text{ROI}}` size of the region of interest
  (:math:`\\mathrm{m}`).

* :math:`r_0` dislocation core radius (:math:`\\mathrm{m}`).

* :math:`d_{i,j}` distance between dislocations :math:`i` and :math:`j`
  (:math:`\\mathrm{m}`).

Finally we introduce the outer cut-off radius with the following
expression:

.. math::

   E_T = \\begin{cases}
   \\frac{G b^2 n}{2 \\pi} \\ln\\left(
   \\frac{r_{\\text{cut}}}{r_0} \\right) &
   \\text{for screw dislocations} \\\\
   \\frac{G b^2 n}{2 \\pi (1-\\nu)}
   \\ln\\left( \\frac{r_{\\text{cut}}}{r_0} \\right) &
   \\text{for edge dislocations}
   \\end{cases}

With:

* :math:`r_{\\text{cut}}` outer cut-off radius (:math:`\\mathrm{m}`).

.. [1] D. Hull and D. J. Bacon.
   Introduction to dislocations. Elsevier, 2011. ISBN:
   978-0-08-096672-4. DOI: 10.1016/C2009-0-64358-0.

.. [2] F. R. N. Nabarro.
   Theory of crystal dislocations. Oxford Clarendon Press, 1967.

"""
