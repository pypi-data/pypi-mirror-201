# -*- coding: utf-8 -*-

"""CPU diffractometer.

This implementation uses the Monte Carlo method to simulate X-ray
diffraction and is parallelized on the different cores of the CPU.

"""

from . import diffraction, parser


setup = parser.setup
diffract = diffraction.diffract
