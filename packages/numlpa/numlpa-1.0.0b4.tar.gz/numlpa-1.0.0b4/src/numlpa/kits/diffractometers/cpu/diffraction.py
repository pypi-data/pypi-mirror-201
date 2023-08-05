# -*- coding: utf-8 -*-

"""CPU diffractometer implementation.

"""

from json import loads
from logging import getLogger
from math import sqrt, isclose
from multiprocessing import Pool, RawArray
from os import cpu_count
from time import time

import matplotlib.pyplot as plt
import numpy as np

from numlpa import config
from . import displacement


logger = getLogger(__package__)

shared = {}


def diffract(sample, **kwargs):
    """Return the Fourier transform.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.

    Keyword Arguments
    -----------------
    z_uvw : tuple of int
        Direction of the line vector (uvw).
    x_uvw : tuple of int
        Direction of the Fourier variable (uvw).
    b_uvw : tuple of int
        Direction of the Burgers vector (uvw).
    g_hkl : tuple of int
        Direction of the diffraction vector (hkl).
    cell : float
        Lattice constant (m).
    step : float
        Step size of the Fourier variable (m).
    range : float
        Absolute or relative limit of the Fourier variable (1|m).
    absolute : bool
        If true, the range parameter becomes an absolute value.
    poisson : float
        Poisson number.
    harmonics : list of int
        List of harmonics to be calculated.
    replicate : int
        Number of replication of the region of interest.
    points : int
        Number of random points.
    processes : int
        Number of parallel processes.
    check : bool
        Display random points and replicated dislocations.

    Returns
    -------
    dict
        Fourier transform data.

    """
    settings = {}
    share = {}
    times = {}
    result = {}

    check_parameters(kwargs)
    prepare_settings(sample, kwargs, settings)
    prepare_shared_data(sample, settings, share)
    user_check(settings, share, kwargs)
    run_monte_carlo(settings, share, result, times)
    return assemble_data(sample, settings, kwargs, result, times)


def check_parameters(kwargs):
    """Set the default configuration value to missing parameters.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments passed to the main function.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('z_uvw', loads(config.get(__package__, 'z_uvw')))
    kwargs.setdefault('x_uvw', loads(config.get(__package__, 'x_uvw')))
    kwargs.setdefault('b_uvw', loads(config.get(__package__, 'b_uvw')))
    kwargs.setdefault('g_hkl', loads(config.get(__package__, 'g_hkl')))
    kwargs.setdefault('cell', config.getfloat(__package__, 'cell'))
    kwargs.setdefault('step', config.getfloat(__package__, 'step'))
    kwargs.setdefault('range', config.getfloat(__package__, 'range'))
    kwargs.setdefault('absolute', config.getboolean(__package__, 'absolute'))
    kwargs.setdefault('points', config.getint(__package__, 'points'))
    kwargs.setdefault('poisson', config.getfloat(__package__, 'poisson'))
    kwargs.setdefault('harmonics', loads(config.get(__package__, 'harmonics')))
    kwargs.setdefault('processes', config.getint(__package__, 'processes'))
    kwargs.setdefault('replicate', config.getint(__package__, 'replicate'))
    kwargs.setdefault('check', config.getboolean(__package__, 'check'))
    if kwargs['processes'] < 1:
        kwargs['processes'] = cpu_count()


def unit_vector(vector):
    """Return the normalized vector.

    Parameters
    ----------
    vector : np.ndarray or list or tuple
        Vector to be normalized.

    Returns
    -------
    np.ndarray
        Normalized vector.

    """
    return np.array(vector) / np.linalg.norm(vector)


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
    logger.debug("calculating the maximum value of the Fourier variable")
    settings['maximum'] = kwargs['range']
    if not kwargs['absolute']:
        settings['maximum'] /= sqrt(sample['distribution']['density'])
    settings['steps'] = int(settings['maximum']/kwargs['step'])

    logger.debug("preparing the change of reference frame")
    settings['z_uni_rf2'] = unit_vector(kwargs['z_uvw'])
    settings['x_uni_rf2'] = unit_vector(kwargs['x_uvw'])
    settings['y_uni_rf2'] = np.cross(
        settings['z_uni_rf2'],
        settings['x_uni_rf2'],
    )
    settings['transition'] = np.array((
        settings['x_uni_rf2'],
        settings['y_uni_rf2'],
        settings['z_uni_rf2'],
    ))

    logger.debug("defining vectors")
    settings['b_uni_rf2'] = unit_vector(kwargs['b_uvw'])
    settings['g_uni_rf2'] = unit_vector(kwargs['g_hkl'])
    settings['b_vec_rf2'] = np.array(kwargs['b_uvw']) * kwargs['cell']/2
    settings['g_vec_rf2'] = np.array(kwargs['g_hkl']) / kwargs['cell']
    settings['g_vec_rf1'] = settings['transition'].dot(settings['g_vec_rf2'])
    settings['g_uni_rf1'] = settings['transition'].dot(settings['g_uni_rf2'])
    settings['s_vec_rf1'] = kwargs['step'] * settings['g_uni_rf1']
    settings['b_len'] = np.linalg.norm(settings['b_vec_rf2'])

    logger.debug("calculating angles")
    settings['abs_ang_z_b'] = np.abs(np.arccos(np.dot(
        settings['z_uni_rf2'],
        settings['b_uni_rf2'],
    )))
    settings['abs_ang_z_g'] = np.abs(np.arccos(np.dot(
        settings['z_uni_rf2'],
        settings['g_uni_rf2'],
    )))

    logger.debug("defining the number of dislocations")
    settings['n_roi'] = len(sample['dislocations']['senses'])
    settings['n_all'] = settings['n_roi'] * (2*kwargs['replicate'] + 1)**2

    logger.debug("drawing random points")
    settings['points'] = random_points(sample, kwargs['points'])

    logger.debug("adding some of the parameters passed to the main function")
    settings['replicate'] = kwargs['replicate']
    settings['poisson'] = kwargs['poisson']
    settings['harmonics'] = kwargs['harmonics']
    settings['step'] = kwargs['step']
    settings['processes'] = kwargs['processes']

    logger.debug("identifying dislocation type")
    if isclose(settings['abs_ang_z_b'], np.pi/2, abs_tol=1e-4):
        settings['type'] = 'edge'
        settings['function'] = phases_edge
        settings['contrast'] = contrast_factor_edge(settings)
    elif isclose(settings['abs_ang_z_b'], 0, abs_tol=1e-4):
        settings['type'] = 'screw'
        settings['function'] = phases_screw
        settings['contrast'] = contrast_factor_screw(settings)
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
    share['step'] = settings['s_vec_rf1'][0:2]
    share['steps'] = settings['steps']
    share['poisson'] = settings['poisson']
    share['constant'] = RawArray('d', 3)

    logger.debug("wrapping shared data")
    wrap['x'] = np.frombuffer(share['x'], dtype=np.float64)
    wrap['y'] = np.frombuffer(share['y'], dtype=np.float64)
    wrap['s'] = np.frombuffer(share['s'], dtype=np.int8)
    wrap['constant'] = np.frombuffer(share['constant'], dtype=np.float64)

    logger.debug("defining shared data")
    wrap['x'][0:settings['n_roi']] = sample['dislocations']['positions'][0]
    wrap['y'][0:settings['n_roi']] = sample['dislocations']['positions'][1]
    wrap['s'][0:settings['n_roi']] = sample['dislocations']['senses']
    wrap['constant'][:] = settings['g_vec_rf1'] * settings['b_len']
    wrap['constant'][1] *= - 1/(4*(1-settings['poisson']))
    if settings['replicate'] > 0:
        if sample['region']['type'] != 'square':
            raise TypeError("can only apply replication on a square region")
        for i, (k_x, k_y) in enumerate(shift_indexes(settings['replicate'])):
            j = (i+1) * settings['n_roi']
            k = (i+2) * settings['n_roi']
            wrap['x'][j:k] = k_x * sample['region']['side']
            wrap['y'][j:k] = k_y * sample['region']['side']
            wrap['x'][j:k] += wrap['x'][0:settings['n_roi']]
            wrap['y'][j:k] += wrap['y'][0:settings['n_roi']]
            wrap['s'][j:k] = wrap['s'][0:settings['n_roi']]


def user_check(settings, share, kwargs):
    """Display random points and replications if requested by the user.

    Parameters
    ----------
    settings : dict
        Diffraction variables.
    share : dict
        Shared data.
    kwargs : dict
        Keyword arguments passed to the main function.

    """
    logger.debug("checking random points and replicated dislocations")
    if kwargs['check']:
        fig, axes = plt.subplots()
        axes.scatter(share['x'], share['y'], label='dislocations')
        axes.scatter(*settings['points'].T, label='random points')
        axes.set_aspect(1)
        axes.set_xlabel("$x$ (m)")
        axes.set_ylabel("$y$ (m)")
        axes.legend()
        plt.show()
        plt.close(fig)


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
        'diffraction': {
            'module': __package__,
            'z_uvw': kwargs['z_uvw'],
            'x_uvw': kwargs['x_uvw'],
            'b_uvw': kwargs['b_uvw'],
            'g_hkl': kwargs['g_hkl'],
            'type': settings['type'],
            'cell': kwargs['cell'],
            'step': kwargs['step'],
            'poisson': kwargs['poisson'],
            'contrast': settings['contrast'],
            'samples': 1,
            'replicate': kwargs['replicate'],
            'duration': times['1'] - times['0'],
            'points': kwargs['points'],
            'processes': kwargs['processes'],
        },
        'coefficients': {
            'harmonic': kwargs['harmonics'],
            'variable': result['variables'].tolist(),
            'cos_mean': result['avg_cos'].tolist(),
            'sin_mean': result['avg_sin'].tolist(),
            'cos_deviation': result['std_cos'].tolist(),
            'sin_deviation': result['std_sin'].tolist(),
        },
    }
    return data


def run_monte_carlo(settings, share, result, times):
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
    logger.debug("computing displacements")
    times['0'] = time()
    with Pool(
        settings['processes'],
        initializer=initializer,
        initargs=(share,),
    ) as pool:
        result['phases'] = pool.map(settings['function'], settings['points'])
    times['1'] = time()

    logger.debug("processing output")
    result['phases'] = np.einsum(
        'ij,k->ikj',
        result['phases'],
        settings['harmonics'],
    )
    result['cos'] = np.cos(result['phases'])
    result['sin'] = np.sin(result['phases'])
    result['avg_cos'] = np.average(result['cos'], axis=0)
    result['avg_sin'] = np.average(result['sin'], axis=0)
    result['coef'] = 1/np.sqrt(result['phases'].shape[0])
    result['std_cos'] = np.std(result['cos'], axis=0) * result['coef']
    result['std_sin'] = np.std(result['sin'], axis=0) * result['coef']
    result['variables'] = (np.arange(settings['steps'])+1) * settings['step']


def initializer(share):
    """Initialize a worker.

    Parameters
    ----------
    share : dict
        Shared data to be passed to the worker.

    """
    shared.update(share)


def shift_indexes(replications):
    """Return the indexes for the replications of the roi.

    Parameters
    ----------
    replications : int
        Number of replications around the region of interest.

    Returns
    -------
    list of tuple
        Replications indexes.

    """
    indexes = []
    for i in range(1, replications+1):
        for j in range(2*i):
            for k in (1, -1):
                indexes.append((-i*k, (i-j)*k))
                indexes.append(((i-j)*k,  i*k))
    return indexes


def random_points(sample, number):
    """Return the position of the random points.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    number : int
        Number of random points in the region of interest.

    Returns
    -------
    np.array
        Position of the random points.

    """
    rng = np.random.default_rng(sample['distribution']['seed'])
    if sample['region']['type'] == 'square':
        side = sample['region']['side']
        positions = rng.random((number, 2), np.float64) * side
    elif sample['region']['type'] == 'disk':
        phi = 2 * np.pi * rng.random(number)
        rad = sample['region']['radius'] * np.sqrt(rng.random(number))
        return np.stack((rad*np.cos(phi), rad*np.sin(phi)), axis=1)
    else:
        raise NotImplementedError("unknown region type")
    return positions


def contrast_factor_edge(settings):
    """Return the contrast factor for edge dislocations.

    Parameters
    ----------
    settings : dict
        Diffraction settings.

    Returns
    -------
    float
        Contrast factor.

    """
    angle_z_g = settings['abs_ang_z_g']
    g_uni = settings['g_uni_rf2']
    b_uni = settings['b_uni_rf2']
    z_uni = settings['z_uni_rf2']
    poisson = settings['poisson']
    cos_projections = np.dot(
        unit_vector(g_uni - np.dot(g_uni, z_uni)*z_uni),
        unit_vector(b_uni - np.dot(b_uni, z_uni)*z_uni),
    )
    contrast = (
        np.sin(angle_z_g)**4 / (8*(1-poisson)**2)
        * (1-4*poisson+8*poisson**2+4*(1-2*poisson)*cos_projections**2)
    )
    return contrast


def contrast_factor_screw(settings):
    """Return the contrast factor for screw dislocations.

    Parameters
    ----------
    settings : dict
        Diffraction settings.

    Returns
    -------
    float
        Contrast factor.

    """
    angle = settings['abs_ang_z_g']
    return np.sin(angle)**2 * np.cos(angle)**2


def phases_screw(position):
    """Return the first harmonic phases at the position.

    This function applies only to screw dislocations. It returns
    'phase(L)' for each value 'L' of the Fourier variable. The
    Fourier coefficients for the harmonic 'h', and the variable 'L'
    can then be expressed by 'cos(h*phase(L))' and 'sin(h*phase(L))'.

    Parameters
    ----------
    position : np.array
        Position of the random point.

    Returns
    -------
    np.array
        Raw values.

    """
    step = shared['step']
    nsteps = shared['steps']
    constant = shared['constant']
    x_dislocations = shared['x']
    y_dislocations = shared['y']
    senses = shared['s']
    displacements = np.empty(nsteps+1, dtype=np.float64)
    for i in range(nsteps+1):
        x_measure, y_measure = position + i*step
        displacements[i] = displacement.screw(
            x_measure,
            y_measure,
            x_dislocations,
            y_dislocations,
            senses,
        )
    differences = displacements[1:] - displacements[0]
    phases = constant[2] * differences
    return phases


def phases_edge(position):
    """Return the first harmonic phases at the position.

    This function applies only to edge dislocations. It returns
    'phase(L)' for each value 'L' of the Fourier variable. The
    Fourier coefficients for the harmonic 'h', and the variable 'L'
    can then be expressed by 'cos(h*phase(L))' and 'sin(h*phase(L))'.

    Parameters
    ----------
    position : np.array
        Position of the random point.

    Returns
    -------
    np.array
        Raw values.

    """
    step = shared['step']
    nsteps = shared['steps']
    constant = shared['constant']
    x_dislocations = shared['x']
    y_dislocations = shared['y']
    senses = shared['s']
    poisson = shared['poisson']
    displacements = np.empty((nsteps+1, 2), dtype=np.float64)
    for i in range(nsteps+1):
        x_measure, y_measure = position + i*step
        displacements[i] = displacement.edge(
            x_measure,
            y_measure,
            x_dislocations,
            y_dislocations,
            senses,
            poisson,
        )
    differences = displacements[1:] - displacements[0]
    phases = np.inner(differences, constant[:2])
    return phases
