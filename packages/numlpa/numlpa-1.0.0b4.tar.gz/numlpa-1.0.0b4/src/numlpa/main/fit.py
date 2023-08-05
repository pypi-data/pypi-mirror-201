# -*- coding: utf-8 -*-

"""Model adjustment feature.

This module implements the functionality to determine the parameter
values predicted by the models by fitting the latter to the diffraction
simulation results.

"""

from datetime import datetime, timezone
from logging import getLogger

import numpy as np

from numlpa import config, kits
from numlpa._version import version_tuple
from numlpa.core.parallelism import get_rank, get_size
from numlpa.core.storage import Container, deserialize, serialize


logger = getLogger(__name__)


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.set_defaults(
        func=main,
    )
    parser.add_argument(
        'input_path',
        type=str,
        help="path of the input container",
    )
    parser.add_argument(
        'output_path',
        type=str,
        help="path of the output container",
    )
    parser.add_argument(
        '-f',
        '--format',
        type=str,
        choices=('json', 'pyc'),
        help="format of the output files",
    )
    parser.add_argument(
        '--model',
        type=str,
        choices=kits.names('models'),
        help="name of the model to be fitted",
    )
    parser.add_argument(
        '--restrict',
        type=str,
        choices=kits.names('restrictions'),
        help="name of the restriction for the variable interval",
    )
    parser.add_argument(
        '--part',
        type=str,
        choices=('real', 'module'),
        help="part of the Fourier transform to be fitted",
    )
    parser.add_argument(
        '--harmonic',
        type=int,
        metavar='int',
        help="harmonic of the Fourier transform to be fitted",
    )

    logger.debug("defining command-line subparsers")
    subparsers = parser.add_subparsers(
        dest='optimizer',
        help="name of the module used for error minimization",
    )
    for name in kits.names('optimizers'):
        subparser = subparsers.add_parser(
            name=name,
            help=f'minimize with {name} optimizer',
        )
        module = kits.get('optimizers', name)
        module.setup(subparser)


def main(input_path, output_path, **kwargs):
    """Adjust a model.

    Parameters
    ----------
    input_path : str
        Path of the input container.
    output_path : str
        Path of the output container.

    Keyword Arguments
    -----------------
    input_path : str
        Path of the input container.
    output_path : str
        Path of the output container.
    format : str
        Format of the output files.
    model : str
        Name of the model to be fitted.
    restrict : str
        Name of the restriction for the variable interval.
    part : str
        Part of the Fourier transform to be fitted ('real', 'module').
    harmonic : int
        Harmonic of the Fourier transform to be fitted.
    optimizer : str
        Name of the module used for error minimization.

    """
    containers = {}
    data = {}
    files = {}
    modules = {}
    series = {}

    logger.debug("retrieving arguments")
    kwargs.setdefault('format', config.get(__name__, 'format'))
    kwargs.setdefault('model', config.get(__name__, 'model'))
    kwargs.setdefault('restrict', config.get(__name__, 'restrict'))
    kwargs.setdefault('part', config.get(__name__, 'part'))
    kwargs.setdefault('harmonic', config.getint(__name__, 'harmonic'))
    kwargs.setdefault('optimizer', config.get(__name__, 'optimizer'))

    logger.debug("preparing containers")
    containers['input'] = Container(input_path)
    containers['output'] = Container(output_path, create=True)

    logger.debug("preparing submodules")
    modules['opti'] = kits.get('optimizers', kwargs['optimizer'])
    modules['model'] = kits.get('models', kwargs['model'])

    logger.debug("loading data")
    files['input'] = containers['input'].names()
    if len(files['input']) > 1:
        raise RuntimeError("multiple files in input container, merge them")
    series['input'] = containers['input'].get(files['input'][0])
    data['input'] = deserialize(series['input'], files['input'][0])
    data['harmonics'] = data['input']['coefficients']['harmonic']
    data['i_harmonic'] = data['harmonics'].index(kwargs['harmonic'])
    data['profile'] = {
        'var': data['input']['coefficients']['variable'],
        'cos': data['input']['coefficients']['cos_mean'][data['i_harmonic']],
        'sin': data['input']['coefficients']['sin_mean'][data['i_harmonic']],
    }
    data['guide'] = modules['model'].guide(data['input'])

    logger.debug("pre-processing profile")
    if kwargs['part'] == 'real':
        data['profile']['amp'] = data['profile']['cos']
    elif kwargs['part'] == 'module':
        data['profile']['amp'] = np.sqrt(
            data['profile']['cos']**2 + data['profile']['sin']**2
        )
    else:
        raise ValueError(f"unknown part '{kwargs['part']}'")
    data['limits'] = {}
    for name in kits.names('restrictions'):
        modules['restrict'] = kits.get('restrictions', name)
        data['limits'][name] = modules['restrict'].limit(
            data['profile']['var'],
            data['profile']['amp'],
        )
    data['imaxmax'] = data['limits'][kwargs['restrict']]
    data['imax'] = list(range(2, data['imaxmax']+1))

    logger.debug("preparing file names")
    width = len(str(data['imaxmax']))
    files['stem'] = [f'0-{str(i).zfill(width)}' for i in data['imax']]
    files['output'] = [f"{stem}.{kwargs['format']}" for stem in files['stem']]
    files['existing'] = containers['output'].names()

    logger.debug("generating files")
    static = {
        'containers': containers,
        'files': files,
        'kwargs': kwargs,
        'modules': modules,
        'data': data,
    }
    for i in range(get_rank(), len(data['imax']), get_size()):
        process(static, i)


def process(static, i):
    """Process a file.

    Parameters
    ----------
    static: dict of dict
        The data that does not vary from one file to another.
    i : int
        Index of the file to be generated.

    """
    file = {}
    fit = {}
    passed = {}
    series = {}

    logger.debug("defining local variables for file index %d", i)
    file['output'] = static['files']['output'][i]
    file['target'] = f"({static['containers']['output']})[{file['output']}]"
    passed.update(static['kwargs'])

    logger.debug("checking if %s already exists", file['output'])
    if file['output'] in static['files']['existing']:
        logger.debug("skipping %s", file['output'])
        return

    logger.info("generating %s", file['target'])
    fit['imax'] = static['data']['imax'][i]
    fit['amplitude'] = np.array(static['data']['profile']['amp'][:fit['imax']])
    fit['variable'] = np.array(static['data']['profile']['var'][:fit['imax']])
    fit['function'] = static['modules']['model'].model(
        static['data']['input'],
        static['kwargs']['harmonic'],
        fit['imax'],
    )

    def objective(parameters):
        return rss(fit['amplitude'], fit['function'], parameters)

    logger.debug("fitting over range [0, %d]", fit['imax'])
    fit['parameters'] = static['modules']['opti'].minimize(
        objective,
        static['data']['guide'],
        **passed,
    )

    logger.debug("computing relative values")
    fit['relative'] = [None for _ in static['data']['guide']['names']]
    for j in range(len(static['data']['guide']['names'])):
        real = static['data']['guide']['real'][j]
        if real is not None:
            fit['relative'][j] = fit['parameters'][j] / real

    logger.debug("assembling data")
    fit['output'] = {
        'metadata': {
            'type': 'model-adjustment',
            'date': datetime.now(timezone.utc).isoformat(timespec="seconds"),
            'version': version_tuple,
        },
        'distribution': static['data']['input']['distribution'],
        'region': static['data']['input']['region'],
        'diffraction': static['data']['input']['diffraction'],
        'profile': {
            'harmonic': static['kwargs']['harmonic'],
            'part': static['kwargs']['part'],
            'variable': list(static['data']['profile']['var']),
            'amplitude': list(static['data']['profile']['amp']),
        },
        'limits': static['data']['limits'],
        'model': {
            'module': static['modules']['model'].__name__,
            'variable': list(fit['variable']),
            'amplitude': list(fit['function'](*fit['parameters'])),
        },
        'optimization': {
            'module': static['modules']['opti'].__name__,
            'restriction': static['kwargs']['restrict'],
            'rss': rss(fit['amplitude'], fit['function'], fit['parameters']),
        },
        'parameters': {
            'names': static['data']['guide']['names'],
            'values': list(fit['parameters']),
            'real': static['data']['guide']['real'],
            'relative': fit['relative'],
        },
    }
    series['output'] = serialize(fit['output'], file['output'])
    static['containers']['output'].add(series['output'], file['output'])


def rss(amplitude, function, parameters):
    """Return the residual sum of squares.

    Parameters
    ----------
    amplitude : np.array
        Value of the true amplitude.
    function : Callable
        Function returning the amplitude given by the model.
    parameters : np.array
        Value of the function parameters.

    Returns
    -------
    float
        Residual sum of squares
    """
    return np.sum((function(*parameters) - amplitude)**2)
