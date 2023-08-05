# -*- coding: utf-8 -*-

"""Dipoles dislocation probability distribution.

This distribution allows to generates pairs of dislocations of opposite
sign and separated by a fixed distance. The region of interest is
divided into subareas of equal size in which a fixed number of dipoles
are generated.

Below is an example of a set of parameter values for the distribution
and an illustration of a resulting dislocation sample.

* ``length`` = ``0`` (The dipole length then becomes the average
  interdislocation distance.)

* ``nsub`` = ``5`` (A side of the region of interest is divided into 5
  subareas.)

* ``pairs`` = ``4`` (Each subarea contains 4 dipoles of dislocations.)

* ``side`` = ``2000e-9`` (The region of interest is a 2000 nm square.)

.. image:: ../figures/distributions/dipoles/0.svg
   :width: 600

"""

from logging import getLogger
from math import cos, sin, pi, sqrt
from random import seed as set_seed, uniform

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
        '--length',
        type=float,
        help="distance between two dislocations of a dipole (m)",
        metavar='float',
    )
    parser.add_argument(
        '--nsub',
        type=int,
        help="number of subareas on a side of the region of interest",
        metavar='int',
    )
    parser.add_argument(
        '--pairs',
        type=int,
        help="number of dipoles in each subarea",
        metavar='int',
    )
    parser.add_argument(
        '--side',
        type=float,
        help="size of the region of interest (m)",
        metavar='float',
    )


def draw(seed, **kwargs):
    """Return a sample drawn from the dipoles distribution.

    When the 'length' parameter is zero, the dipole distance becomes
    the average interdislocation distance.

    Parameters
    ----------
    seed : int
        Random seed.

    Keyword Arguments
    -----------------
    length : float
        Distance between two dislocations of a dipole (m).
    nsub : int
        Number of subareas on a side of the region of interest.
    pairs : int
        Number of dipoles in each subarea.
    side : float
        Size of the region of interest (m).

    Returns
    -------
    dict
        Dislocation sample data.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('length', config.getfloat(__name__, 'length'))
    kwargs.setdefault('nsub', config.getint(__name__, 'nsub'))
    kwargs.setdefault('pairs', config.getint(__name__, 'pairs'))
    kwargs.setdefault('side', config.getfloat(__name__, 'side'))
    density = 2*kwargs['pairs']*kwargs['nsub']**2/kwargs['side']**2
    subarea = kwargs['side']/kwargs['nsub']
    if kwargs['length'] == 0:
        kwargs['length'] = 1/sqrt(density)

    logger.debug("drawing dislocations")
    set_seed(seed)
    x_list, y_list, s_list = [], [], []
    for i in range(kwargs['nsub']):
        for j in range(kwargs['nsub']):
            for _ in range(kwargs['pairs']):
                x_center = uniform(i*subarea, (i+1)*subarea)
                y_center = uniform(j*subarea, (j+1)*subarea)
                angle = uniform(0, 2*pi)
                for sense in (-1, 1):
                    x_list.append(x_center+sense*cos(angle)*kwargs['length']/2)
                    y_list.append(y_center+sense*sin(angle)*kwargs['length']/2)
                    s_list.append(sense)

    logger.debug("assembling data")
    data = {
        'distribution': {
            'module': __name__,
            'seed': seed,
            'density': density,
            'length': kwargs['length'],
            'nsub': kwargs['nsub'],
            'pairs': kwargs['pairs'],
            'side': kwargs['side'],
        },
        'region': {
            'type': 'square',
            'side': kwargs['side'],
        },
        'dislocations': {
            'senses': s_list,
            'positions': [x_list, y_list],
        },
    }
    return data
