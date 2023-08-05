# -*- coding: utf-8 -*-

"""CPU analyzer.

"""

from logging import getLogger
from multiprocessing import Pool, RawArray
from os import cpu_count
from time import time

import numpy as np

from numlpa import config
from . import interaction


logger = getLogger(__package__)

shared = {}


def analyze(sample, **kwargs):
    """Return the spatial analysis.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.

    Keyword Arguments
    -----------------
    type : str
        Dislocation type ('screw' or 'edge').
    r_0 : float
        Core radius (m).
    r_roi : float
        Size of the region of interest (m).
    r_max : float
        Maximum radius value (m).
    steps : int
        Number of subdivision on the absice axis.
    b_len : float
        Burgers vector length (m).
    poisson : float
        Poisson number.
    shear : float
        Shear modulus (Pa).
    processes : int
        Number of parallel processes.

    Returns
    -------
    dict
        Spatial analyzis data.

    """
    settings = {}
    share = {}
    times = {}
    result = {}

    check_parameters(kwargs)
    prepare_settings(sample, kwargs, settings)
    prepare_shared_data(sample, settings, share)
    run_analysis(settings, share, result, times)
    return assemble_data(sample, settings, kwargs, result, times)


def check_parameters(kwargs):
    """Set the default configuration value to missing parameters.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments passed to the main function.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('type', config.get(__package__, 'type'))
    kwargs.setdefault('r_0', config.getfloat(__package__, 'r_0'))
    kwargs.setdefault('r_roi', config.getfloat(__package__, 'r_roi'))
    kwargs.setdefault('r_max', config.getfloat(__package__, 'r_max'))
    kwargs.setdefault('steps', config.getint(__package__, 'steps'))
    kwargs.setdefault('b_len', config.getfloat(__package__, 'b_len'))
    kwargs.setdefault('poisson', config.getfloat(__package__, 'poisson'))
    kwargs.setdefault('shear', config.getfloat(__package__, 'shear'))
    kwargs.setdefault('processes', config.getint(__package__, 'processes'))
    if kwargs['processes'] < 1:
        kwargs['processes'] = cpu_count()


def prepare_settings(sample, kwargs, settings):
    """Prepare the diffraction variables.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    kwargs : dict
        Keyword arguments passed to the main function.
    settings : dict
        Diffraction variables.

    """
    logger.debug("adding some of the parameters passed to the main function")
    settings['r_0'] = kwargs['r_0']
    settings['r_roi'] = kwargs['r_roi']
    settings['steps'] = kwargs['steps']
    settings['b_len'] = kwargs['b_len']
    settings['poisson'] = kwargs['poisson']
    settings['shear'] = kwargs['shear']
    settings['processes'] = kwargs['processes']

    logger.debug("preparing energy parameters")
    settings['n_all'] = len(sample['dislocations']['senses'])
    settings['indexes'] = range(settings['n_all'])

    logger.debug("identifying region type")
    if sample['region']['type'] == 'square':
        settings['r_max'] = 2 * sample['region']['side']
        if settings['r_roi'] == 0:
            settings['r_roi'] = sample['region']['side']
    elif sample['region']['type'] == 'disk':
        settings['r_max'] = 2 * sample['region']['radius']
        if settings['r_roi'] == 0:
            settings['r_roi'] = sample['region']['radius']
    else:
        raise NotImplementedError("unknown region type")
    settings['step'] = settings['r_max'] / kwargs['steps']

    logger.debug("identifying dislocation type")
    if kwargs['type'] == 'edge':
        settings['factor'] = 1 / (1-settings['poisson'])
    elif kwargs['type'] == 'screw':
        settings['factor'] = 1
    else:
        raise NotImplementedError("mixed dislocations")


def prepare_shared_data(sample, settings, share):
    """Initialize and fill the shared containers.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    settings : dict
        Diffraction variables.
    share : dict
        Shared data.

    """
    wrap = {}

    logger.debug("declaring shared data")
    share['x'] = RawArray('d', settings['n_all'])
    share['y'] = RawArray('d', settings['n_all'])
    share['s'] = RawArray('b', settings['n_all'])
    share['steps'] = settings['steps']
    share['step'] = settings['step']

    logger.debug("wrapping shared data")
    wrap['x'] = np.frombuffer(share['x'], dtype=np.float64)
    wrap['y'] = np.frombuffer(share['y'], dtype=np.float64)
    wrap['s'] = np.frombuffer(share['s'], dtype=np.int8)

    logger.debug("defining shared data")
    wrap['x'][:] = sample['dislocations']['positions'][0]
    wrap['y'][:] = sample['dislocations']['positions'][1]
    wrap['s'][:] = sample['dislocations']['senses']


def run_analysis(settings, share, result, times):
    """Run the simulation with Monte Carlo method.

    Parameters
    ----------
    settings : dict
        Diffraction variables.
    share : dict
        Shared data.
    results : dict
        Diffraction results.
    times : dict
        Time measurements.

    """
    logger.debug("computing self energy")
    result['self_energy'] = (
        settings['n_all'] *
        settings['shear'] *
        settings['b_len']**2 /
        (4 * np.pi) *
        settings['factor'] *
        np.log(settings['r_roi']/settings['r_0'])
    )

    logger.debug("computing interactions")
    times['0'] = time()
    with Pool(
        settings['processes'],
        initializer=initializer,
        initargs=(share,),
    ) as pool:
        result['raw'] = pool.map(interaction_data, settings['indexes'])
    times['1'] = time()

    logger.debug("processing output")
    result['interaction_energy'] = 0
    result['count_mm'] = np.zeros(settings['steps'], dtype=np.int64)
    result['count_mp'] = np.zeros(settings['steps'], dtype=np.int64)
    result['count_pm'] = np.zeros(settings['steps'], dtype=np.int64)
    result['count_pp'] = np.zeros(settings['steps'], dtype=np.int64)
    for i in settings['indexes']:
        term, count_equal, count_opposed = result['raw'][i]
        result['interaction_energy'] += term
        if share['s'][i] > 0:
            result['count_pp'] += count_equal
            result['count_pm'] += count_opposed
        else:
            result['count_mm'] += count_equal
            result['count_mp'] += count_opposed
    result['interaction_energy'] += (
        settings['n_all'] *
        (settings['n_all']-1) *
        np.log(settings['r_roi'])
    )
    result['interaction_energy'] *= (
        1/2 *
        settings['shear'] *
        settings['b_len']**2 /
        (4 * np.pi) *
        settings['factor']
    )

    logger.debug("computing total energy")
    result['total_energy'] = result['self_energy']
    result['total_energy'] += result['interaction_energy']

    logger.debug("computing outer cut-off radius")
    result['r_cut'] = settings['r_0'] * np.exp(
        result['total_energy'] *
        (2 * np.pi) /
        settings['n_all'] /
        settings['shear'] /
        settings['b_len']**2 /
        settings['factor']
    )


def initializer(share):
    """Initialize a worker.

    Parameters
    ----------
    share : dict
        Shared data to be passed to the worker.

    """
    shared.update(share)


def assemble_data(sample, settings, kwargs, result, times):
    """Return the Fourier transform data.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    settings : dict
        Diffraction variables.
    kwargs : dict
        Keyword arguments passed to the main function.
    results : dict
        Diffraction results.
    times : dict
        Time measurements.

    Returns
    -------
    dict
        Fourier transform data.

    """
    logger.debug("assembling data")
    data = {
        'distribution': sample['distribution'],
        'region': sample['region'],
        'analysis': {
            'module': __package__,
            'type': kwargs['type'],
            'r_0': settings['r_0'],
            'r_roi': settings['r_roi'],
            'r_max': settings['r_max'],
            'steps': settings['steps'],
            'poisson': settings['poisson'],
            'shear': settings['shear'],
            'r_cut': result['r_cut'],
            'self_energy': result['self_energy'],
            'interaction_energy': result['interaction_energy'],
            'total_energy': result['total_energy'],
            'variable': [settings['step']*i for i in range(kwargs['steps'])],
            'count_mm': result['count_mm'].tolist(),
            'count_mp': result['count_mp'].tolist(),
            'count_pm': result['count_pm'].tolist(),
            'count_pp': result['count_pp'].tolist(),
            'samples': 1,
            'duration': times['1'] - times['0'],
            'processes': kwargs['processes'],
        }
    }
    return data


def interaction_data(index):
    """Return the interaction data for one dislocation.

    This function computes the interaction energy term and the
    dislocation distribution around a dislocation using the interaction
    extension module.

    Parameters
    ----------
    index : int
        Index of the dislocation.

    Returns
    -------
    tuple
        Interaction data for screw dislocations.

    """
    count_equal = RawArray('Q', shared['steps'])
    count_opposed = RawArray('Q', shared['steps'])
    np.frombuffer(count_equal, dtype=np.uint64)[:] = 0
    np.frombuffer(count_opposed, dtype=np.uint64)[:] = 0
    term = interaction.sum_term(
        index,
        shared['x'],
        shared['y'],
        shared['s'],
        shared['step'],
        count_equal,
        count_opposed,
    )
    raw = (
        term,
        np.array(count_equal, dtype=np.int64),
        np.array(count_opposed, dtype=np.int64),
    )
    return raw
