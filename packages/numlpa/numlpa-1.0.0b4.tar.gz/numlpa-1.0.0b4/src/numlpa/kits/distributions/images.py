# -*- coding: utf-8 -*-

"""Image screw dislocation probability distribution.

This distribution allows to generate uniformly distributed screw
dislocations in a circular region of interest. The image dislocations
allowing the mechanical equilibrium at the surface of the cylinder are
also added outside the region of interest.

Below is an example of a set of parameter values for the distribution
and an illustration of a resulting dislocation sample.

* ``number`` = ``200`` (The region of interest contains 200
  dislocations.)

* ``radius`` = ``1000e-9`` (The region of interest is a disk of 1000 nm
  radius.)

.. image:: ../figures/distributions/images/0.svg
   :width: 600

"""

from logging import getLogger
from math import pi, sqrt, cos, sin
from random import choice, seed as set_seed, uniform

from numlpa import config


logger = getLogger(__name__)


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.add_argument(
        '--number',
        type=int,
        help="number of dislocations in the region of interest",
        metavar='int',
    )
    parser.add_argument(
        '--radius',
        type=float,
        help="radius of the region of interest (m)",
        metavar='float',
    )


def draw(seed, **kwargs):
    """Return a sample drawn from the images distribution.

    Parameters
    ----------
    seed : int
        Random seed.

    Keyword Arguments
    -----------------
    number : int
        Number of dislocations in the region of interest.
    radius : float
        Radius of the region of interest (m).

    Returns
    -------
    dict
        Dislocation sample data.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('number', config.getint(__name__, 'number'))
    kwargs.setdefault('radius', config.getfloat(__name__, 'radius'))
    density = kwargs['number']/(pi*kwargs['radius']**2)

    logger.debug("drawing dislocations")
    set_seed(seed)
    x_list, y_list, s_list = [], [], []
    for _ in range(kwargs['number']):
        angle = uniform(0, 2*pi)
        sense = choice((-1, 1))
        radius_dilocation = kwargs['radius'] * sqrt(uniform(0, 1))
        x_list.append(radius_dilocation*cos(angle))
        y_list.append(radius_dilocation*sin(angle))
        s_list.append(sense)
        radius_image = kwargs['radius']**2 / radius_dilocation
        x_list.append(radius_image*cos(angle))
        y_list.append(radius_image*sin(angle))
        s_list.append(-sense)

    logger.debug("assembling data")
    data = {
        'distribution': {
            'module': __name__,
            'seed': seed,
            'density': density,
            'number': kwargs['number'],
            'radius': kwargs['radius'],
        },
        'region': {
            'type': 'disk',
            'radius': kwargs['radius'],
        },
        'dislocations': {
            'senses': s_list,
            'positions': [x_list, y_list],
        },
    }
    return data
