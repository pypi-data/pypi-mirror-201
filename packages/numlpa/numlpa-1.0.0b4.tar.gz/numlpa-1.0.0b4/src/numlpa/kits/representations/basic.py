# -*- coding: utf-8 -*-

"""Basic data representations.

This module implements very simple figure generators for the different
types of data produced by the package.

"""

from json import loads
from logging import getLogger

from matplotlib import patches
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
    samples = parser.add_argument_group(
        title='sample',
        description="dislocation map options",
    )
    samples.add_argument(
        '--pairs',
        action='store_true',
        help="display a line between two consecutive dislocations",
    )
    samples.add_argument(
        '--subareas',
        help="name of the parameter giving the number of subareas",
        type=str,
    )
    profiles = parser.add_argument_group(
        title='profiles',
        description="diffraction profile options",
    )
    profiles.add_argument(
        '--ylog',
        action='store_true',
        help="display the ordinate axis in logarithmic scale",
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
    kwargs.setdefault('pairs', config.getboolean(__name__, 'pairs'))
    kwargs.setdefault('subareas', config.get(__name__, 'subareas'))
    kwargs.setdefault('ylog', config.getboolean(__name__, 'ylog'))


def sample(data, **kwargs):
    """Return a matplotlib figure illustrating a dislocation sample.

    Parameters
    ----------
    data : dict
        Dislocation sample data.

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
    pairs : bool
        Display a line between two consecutive dislocations.
    subareas : str
        Name of the parameter giving the number of subareas.

    Returns
    -------
    Figure
        Matplotlib figure.

    """
    figure = {}
    retrieve_parameters(kwargs)

    logger.debug("initializing figure")
    figure['fig'], figure['ax'] = plt.subplots(figsize=kwargs['figsize'])
    figure['ax'].set_aspect(1)

    logger.debug("retrieving dislocation positions")
    figure['x'] = np.array(data['dislocations']['positions'][0])
    figure['y'] = np.array(data['dislocations']['positions'][1])
    figure['s'] = np.array(data['dislocations']['senses'])

    logger.debug("setting scale coefficient for unit conversion")
    figure['scale'] = 1
    if kwargs['length'] == 'nm':
        figure['scale'] = 1e9

    logger.debug("plotting dislocation positions")
    partition = (
        (r"$ \bot $", "Burgers vector sense $+$", figure['s'] > 0),
        (r"$ \top $", "Burgers vector sense $-$", figure['s'] < 0),
    )
    for marker, label, mask in partition:
        figure['ax'].scatter(
            figure['scale']*figure['x'][mask],
            figure['scale']*figure['y'][mask],
            marker=marker,
            label=label,
            zorder=100,
        )

    logger.debug("drawing region border")
    if data['region']['type'] == 'square':
        figure['side'] = figure['scale'] * data['region']['side']
        figure['limits'] = [-figure['side']*0.1, figure['side']*1.1]
        figure['ax'].set_xlim(figure['limits'])
        figure['ax'].set_ylim(figure['limits'])
        figure['nsub'] = data['distribution'].get(kwargs['subareas'], 1)
        for i in range(figure['nsub']+1):
            plt.plot(
                (0, figure['side']),
                (i*figure['side']/figure['nsub'],)*2,
                color='black',
                alpha=0.3,
            )
            plt.plot(
                (i*figure['side']/figure['nsub'],)*2,
                (0, figure['side']),
                color='black',
                alpha=0.3,
            )
    elif data['region']['type'] == 'disk':
        figure['radius'] = figure['scale'] * data['region']['radius']
        figure['limits'] = [-figure['radius']*1.1, figure['radius']*1.1]
        figure['ax'].set_xlim(figure['limits'])
        figure['ax'].set_ylim(figure['limits'])
        figure['circle'] = patches.Circle(
            (0, 0),
            figure['radius'],
            edgecolor='k',
            alpha=0.5,
            facecolor='none',
        )
        figure['ax'].add_patch(figure['circle'])

    logger.debug("displaying pairs")
    if kwargs['pairs']:
        for i in range(len(figure['s'])//2):
            figure['ax'].plot(
                (
                    figure['scale'] * figure['x'][2*i],
                    figure['scale'] * figure['x'][2*i+1],
                ),
                (
                    figure['scale'] * figure['y'][2*i],
                    figure['scale'] * figure['y'][2*i+1],
                ),
                color='black',
                alpha=0.3,
            )

    logger.debug("displaying text")
    if kwargs['legend']:
        figure['ax'].legend()
    if kwargs['title'] != "":
        figure['ax'].set_title(kwargs['title'])
    figure['ax'].set_xlabel(f"$x$ ({kwargs['length']})")
    figure['ax'].set_ylabel(f"$y$ ({kwargs['length']})")

    return figure['fig']


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
    if kwargs['ylog']:
        figure['ax'].set_yscale('log')

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
    figure['sin'] = {
        'avg': np.array(data['coefficients']['sin_mean']),
        'std': np.array(data['coefficients']['sin_deviation']),
    }
    for func in ('cos', 'sin'):
        for i, j in enumerate(data['coefficients']['harmonic']):
            figure['ax'].plot(
                figure['scale']*figure['variable'],
                figure[func]['avg'][i],
                label=(
                    fr"$\left\langle \{func} \left( 2 \pi {TEX_G}_{j} \cdot "
                    fr"\left[ {TEX_U} \left( {TEX_R} + {TEX_L} \right) "
                    fr"- {TEX_U} \left( {TEX_R} \right) \right] \right) "
                    fr"\right\rangle$"
                )
            )
            figure['ax'].fill_between(
                figure['scale']*figure['variable'],
                figure[func]['avg'][i]-figure[func]['std'][i],
                figure[func]['avg'][i]+figure[func]['std'][i],
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
    if kwargs['ylog']:
        figure['ax'].set_yscale('log')

    logger.debug("setting scale coefficient for unit conversion")
    figure['scale'] = 1
    if kwargs['length'] == 'nm':
        figure['scale'] = 1e9

    logger.debug("plotting model and simulated profile")
    figure['ax'].plot(
        np.array(data['profile']['variable'])*figure['scale'],
        np.array(data['profile']['amplitude']),
        label='profile',
    )
    figure['ax'].plot(
        np.array(data['model']['variable'])*figure['scale'],
        np.array(data['model']['amplitude']),
        label='model',
    )

    logger.debug("displaying text")
    if kwargs['legend']:
        figure['ax'].legend()
    if kwargs['title'] != "":
        figure['ax'].set_title(kwargs['title'])
    figure['ax'].set_xlabel(f"$L$ ({kwargs['length']})")

    return figure['fig']
