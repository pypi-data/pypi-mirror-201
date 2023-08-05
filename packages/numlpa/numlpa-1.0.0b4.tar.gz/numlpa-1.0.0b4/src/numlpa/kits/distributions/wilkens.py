# -*- coding: utf-8 -*-

"""Wilkens dislocation probability distribution.

The Wilkens distribution divides the region of interest into subareas
of equal size and randomly places in these subareas as many
dislocations with a positive Burger vector sense as negative.

Below is an example of a set of parameter values for the distribution
and an illustration of a resulting dislocation sample.

* ``nsub`` = ``5`` (A side of the region of interest is divided into 5
  subareas.)

* ``pairs`` = ``4`` (Each subarea contains 8 dislocations.)

* ``side`` = ``2000e-9`` (The region of interest is a 2000 nm square.)

.. image:: ../figures/distributions/wilkens/0.svg
   :width: 600

"""

from logging import getLogger
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
        '--nsub',
        type=int,
        help="number of subareas on a side of the region of interest",
        metavar='int',
    )
    parser.add_argument(
        '--pairs',
        type=int,
        help="number of pairs of dislocations in each subarea",
        metavar='int',
    )
    parser.add_argument(
        '--side',
        type=float,
        help="size of the region of interest (m)",
        metavar='float',
    )


def draw(seed, **kwargs):
    """Return a sample drawn from the Wilkens distribution.

    Parameters
    ----------
    seed : int
        Random seed.

    Keyword Arguments
    -----------------
    nsub : int
        Number of subareas on a side of the region of interest.
    pairs : int
        Number of pairs of dislocations in each subarea.
    side : float
        Size of the region of interest (m).

    Returns
    -------
    dict
        Dislocation sample data.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('nsub', config.getint(__name__, 'nsub'))
    kwargs.setdefault('pairs', config.getint(__name__, 'pairs'))
    kwargs.setdefault('side', config.getfloat(__name__, 'side'))
    density = 2*kwargs['pairs']*kwargs['nsub']**2/kwargs['side']**2
    subarea = kwargs['side']/kwargs['nsub']

    logger.debug("drawing dislocations")
    set_seed(seed)
    x_list, y_list, s_list = [], [], []
    for i in range(kwargs['nsub']):
        for j in range(kwargs['nsub']):
            for _ in range(kwargs['pairs']):
                for sense in (-1, 1):
                    x_list.append(uniform(i*subarea, (i+1)*subarea))
                    y_list.append(uniform(j*subarea, (j+1)*subarea))
                    s_list.append(sense)

    logger.debug("assembling data")
    data = {
        'distribution': {
            'module': __name__,
            'seed': seed,
            'density': density,
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
