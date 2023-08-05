# -*- coding: utf-8 -*-

"""Default optimizer.

This module implements a parallelized optimizer with random restart.

"""

from logging import getLogger
from multiprocessing import Pool
from os import cpu_count
from random import seed as set_seed, uniform

import numpy as np
from scipy import optimize

from numlpa import config


logger = getLogger(__name__)

shared = {}


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.add_argument(
        '--maxiter',
        type=int,
        help="maximum number of iterations",
        metavar='int',
    )
    parser.add_argument(
        '--method',
        type=str,
        help="name of the solver",
    )
    parser.add_argument(
        '--points',
        type=int,
        help="number of random initializations tested",
    )
    parser.add_argument(
        '-s',
        '--seed',
        type=int,
        help="random seed",
        metavar='int',
    )
    parser.add_argument(
        '--processes',
        type=int,
        help="number of parallel processes",
    )


def minimize(objective, guide, **kwargs):
    """Return the parameters minimizing the objective function.

    Parameters
    ----------
    objective : Callable
        Function to be minimized.
    guide : dict of list
        Parameter guide.

    Keyword Arguments
    -----------------
    maxiter : int
        Maximum number of iterations.
    method : str
        Name of the solver.
    points : int
        Number of random initializations tested.
    seed : int
        Random seed.
    processes : int
        Number of parallel processes.

    Returns
    -------
    parameters : list
        Optimal parameters values.

    """
    data = {}

    logger.debug("retrieving parameters")
    kwargs.setdefault('maxiter', config.getint(__name__, 'maxiter'))
    kwargs.setdefault('method', config.get(__name__, 'method'))
    kwargs.setdefault('points', config.getint(__name__, 'points'))
    kwargs.setdefault('seed', config.getint(__name__, 'seed'))
    kwargs.setdefault('processes', config.getint(__name__, 'processes'))
    if kwargs['processes'] < 1:
        kwargs['processes'] = cpu_count()

    logger.debug("defining initializations")
    set_seed(kwargs['seed'])
    data['inits'] = []
    for _ in range(kwargs['points']):
        init = []
        for i in range(len(guide['names'])):
            if guide['real'][i] is not None:
                init.append(guide['real'][i])
            else:
                init.append(uniform(guide['min'][i], guide['max'][i]))
        data['inits'].append(init)

    logger.debug("optimizing")
    share = {
        'fun': objective,
        'method': kwargs['method'],
        'options': {
            'maxiter': kwargs['maxiter'],
        }
    }
    np.seterr(all="ignore")
    with Pool(
        kwargs['processes'],
        initargs=(share,),
        initializer=initializer,
    ) as pool:
        data['result'] = pool.map(result, data['inits'])

    logger.debug("retrieving best parameters")
    data['rss'] = [r.fun for r in data['result']]
    if not any(r.success for r in data['result']):
        logger.warning("no attempt to adjust the model was successful")
    return data['result'][np.argmin(data['rss'])].x


def initializer(share):
    """Initialize a worker.

    Parameters
    ----------
    share : dict
        Shared data to be passed to the worker.

    """
    shared.update(share)


def result(initialization):
    """Return the optimization result for the given initialization.

    Parameters
    ----------
    initialization : list
        Parameter initialization.

    Returns
    -------
    OptimizeResult
        Optimization result.

    """
    return optimize.minimize(x0=initialization, **shared)
