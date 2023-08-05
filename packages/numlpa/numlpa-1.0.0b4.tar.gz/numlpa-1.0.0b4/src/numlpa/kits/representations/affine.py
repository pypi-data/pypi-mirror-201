# -*- coding: utf-8 -*-

"""Affine data representations.

This module implements the figure generators allowing to show the
asymptotic affine behavior of the Fourier transform amplitude after
the following transformation:

.. math::

   A(L) \\mapsto \\frac{ln(A(L))}{L^2}

"""

from json import loads
from logging import getLogger

import matplotlib.pyplot as plt
import numpy as np

from numlpa import config


logger = getLogger(__package__)

TEX_G = r"\vec{g}"
TEX_U = r"\vec{u}"
TEX_R = r"\vec{r}"
TEX_L = r"\vec{L}"

CONVERSION = ['']


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.add_argument(
        '--figsize',
        help="width and heigth of the figure (inches)",
        type=float,
        nargs=2,
        metavar='float',
    )
    parser.add_argument(
        '--title',
        help="title of the figure",
        type=str,
        metavar='str',
    )
    legend = parser.add_mutually_exclusive_group()
    legend.add_argument(
        '--legend',
        action='store_const',
        const=True,
        help="display legends",
        dest='legend'
    )
    legend.add_argument(
        '--no-legend',
        action='store_const',
        const=False,
        help="hide legends",
        dest='legend'
    )
    parser.add_argument(
        '--length',
        help="length unit",
        type=str,
        choices=('m', 'nm'),
    )


def retrieve_parameters(kwargs):
    """Load the default value of the missing parameters.

    Parameters
    ----------
    kwargs : dict
        Parameters passed to a function of the module.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('figsize', loads(config.get(__name__, 'figsize')))
    kwargs.setdefault('title', config.get(__name__, 'title'))
    kwargs.setdefault('legend', config.getboolean(__name__, 'legend'))
    kwargs.setdefault('length', config.get(__name__, 'length'))


def log_x2(amplitude, variable):
    """Return the transformed amplitude.

    Parameters
    ----------
    amplitude : list or np.array
        Fourier amplitude values.
    variable : list or np.array
        Fourier variable values.

    Returns
    -------
    np.array
        Value of 'ln(amplitude)/variable**2'.

    """
    amplitude = np.array(amplitude)
    variable = np.array(variable)
    amplitude = np.where(amplitude > 0, amplitude, np.nan)
    return np.log(amplitude)/variable**2


def transform(data, **kwargs):
    """Return a matplotlib figure illustrating a Fourier transform.

    Parameters
    ----------
    data : dict
        Fourier transform data.

    Keyword Arguments
    -----------------
    figsize : tuple
        Width and heigth of the figure (inches).
    title : str
        Title of the figure.
    legend : bool
        Display legends.
    length : str
        Length unit ('m' or 'nm').

    Returns
    -------
    Figure
        Matplotlib figure.

    """
    figure = {}
    retrieve_parameters(kwargs)

    logger.debug("initializing figure")
    figure['fig'], figure['ax'] = plt.subplots(figsize=kwargs['figsize'])
    figure['ax'].grid()
    figure['ax'].set_xscale('log')

    logger.debug("setting scale coefficient for unit conversion")
    figure['scale'] = 1
    if kwargs['length'] == 'nm':
        figure['scale'] = 1e9

    logger.debug("plotting profiles")
    figure['variable'] = np.array(data['coefficients']['variable'])
    figure['cos'] = {
        'avg': np.array(data['coefficients']['cos_mean']),
        'std': np.array(data['coefficients']['cos_deviation']),
    }
    figure['fill'] = {
        'min': figure['cos']['avg'] - figure['cos']['std'],
        'max': figure['cos']['avg'] + figure['cos']['std'],
    }
    for i, j in enumerate(data['coefficients']['harmonic']):
        figure['ax'].plot(
            figure['scale']*figure['variable'],
            log_x2(figure['cos']['avg'][i], figure['variable']),
            label=(
                fr"$\ln \left("
                fr"\left\langle \cos \left( 2 \pi {TEX_G}_{j} \cdot "
                fr"\left[ {TEX_U} \left( {TEX_R} + {TEX_L} \right) "
                fr"- {TEX_U} \left( {TEX_R} \right) \right] \right) "
                fr"\right\rangle"
                fr"\right) / L^2$"
            )
        )
        figure['ax'].fill_between(
            figure['scale']*figure['variable'],
            log_x2(figure['fill']['min'][i], figure['variable']),
            log_x2(figure['fill']['max'][i], figure['variable']),
            alpha=0.3,
        )

    logger.debug("displaying text")
    if kwargs['legend']:
        figure['ax'].legend()
    if kwargs['title'] != "":
        figure['ax'].set_title(kwargs['title'])
    figure['ax'].set_xlabel(f"$L$ ({kwargs['length']})")

    return figure['fig']


def adjustment(data, **kwargs):
    """Return a matplotlib figure illustrating a Fourier transform.

    Parameters
    ----------
    data : dict
        Model adjustment data.

    Keyword Arguments
    -----------------
    figsize : tuple
        Width and heigth of the figure (inches).
    title : str
        Title of the figure.
    legend : bool
        Display legends.
    length : str
        Length unit ('m' or 'nm').

    Returns
    -------
    Figure
        Matplotlib figure.

    """
    figure = {}
    retrieve_parameters(kwargs)

    logger.debug("initializing figure")
    figure['fig'], figure['ax'] = plt.subplots(figsize=kwargs['figsize'])
    figure['ax'].grid()
    figure['ax'].set_xscale('log')

    logger.debug("setting scale coefficient for unit conversion")
    figure['scale'] = 1
    if kwargs['length'] == 'nm':
        figure['scale'] = 1e9

    logger.debug("plotting model and simulated profile")
    figure['ax'].plot(
        np.array(data['profile']['variable'])*figure['scale'],
        log_x2(data['profile']['amplitude'], data['profile']['variable']),
        label='profile',
    )
    figure['ax'].plot(
        np.array(data['model']['variable'])*figure['scale'],
        log_x2(data['model']['amplitude'], data['model']['variable']),
        label='model',
    )

    logger.debug("displaying text")
    if kwargs['legend']:
        figure['ax'].legend()
    if kwargs['title'] != "":
        figure['ax'].set_title(kwargs['title'])
    figure['ax'].set_xlabel(f"$L$ ({kwargs['length']})")

    return figure['fig']
