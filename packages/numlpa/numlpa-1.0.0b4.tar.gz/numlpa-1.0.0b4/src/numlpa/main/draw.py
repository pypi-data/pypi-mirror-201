# -*- coding: utf-8 -*-

"""Random dislocation drawing feature.

This module implements the functionality to randomly draw and save a
group of dislocation samples from the same probability distribution.

"""

from datetime import datetime, timezone
from logging import getLogger

from numlpa import config, kits
from numlpa._version import version_tuple
from numlpa.core.parallelism import get_rank, get_size
from numlpa.core.storage import Container, serialize


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
        'output_path',
        type=str,
        help="path of the output container",
    )
    parser.add_argument(
        '-n',
        '--size',
        type=int,
        help="number of samples to draw",
        metavar='int',
    )
    parser.add_argument(
        '-s',
        '--seed',
        type=int,
        help="random seed",
        metavar='int',
    )
    parser.add_argument(
        '-f',
        '--format',
        type=str,
        choices=('json', 'pyc'),
        help="format of the output files",
    )

    logger.debug("defining command-line subparsers")
    subparsers = parser.add_subparsers(
        dest='distribution',
        help="name of the module used for the random draw",
    )
    for name in kits.names('distributions'):
        subparser = subparsers.add_parser(
            name=name,
            help=f"draw from {name} distribution",
        )
        module = kits.get('distributions', name)
        module.setup(subparser)


def main(output_path, **kwargs):
    """Generate and save dislocation samples.

    Parameters
    ----------
    output_path : str
        Path of the output container.

    Keyword Arguments
    -----------------
    distribution : str
        Name of the module used for the random draw.
    size : int
        Number of samples to draw.
    seed : int
        Random seed.
    format : str
        Format of the output files.

    """
    containers = {}
    files = {}
    modules = {}

    logger.debug("retrieving parameters")
    kwargs.setdefault('distribution', config.get(__name__, 'distribution'))
    kwargs.setdefault('size', config.getint(__name__, 'size'))
    kwargs.setdefault('seed', config.getint(__name__, 'seed'))
    kwargs.setdefault('format', config.get(__name__, 'format'))

    logger.debug("preparing containers")
    containers['output'] = Container(output_path, create=True)

    logger.debug("preparing file names")
    stem_width = len(str(kwargs['size']-1))
    files['stems'] = [str(i).zfill(stem_width) for i in range(kwargs['size'])]
    files['output'] = [f"{stem}.{kwargs['format']}" for stem in files['stems']]
    files['existing'] = containers['output'].names()

    logger.debug("preparing submodules")
    modules['dist'] = kits.get('distributions', kwargs['distribution'])

    logger.debug("generating files")
    static = {
        'containers': containers,
        'files': files,
        'kwargs': kwargs,
        'modules': modules,
    }
    for i in range(get_rank(), kwargs['size'], get_size()):
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
    data = {}
    file = {}
    passed = {}
    series = {}

    logger.debug("defining local variables for file index %d", i)
    file['output'] = static['files']['output'][i]
    file['target'] = f"({static['containers']['output']})[{file['output']}]"
    passed.update(static['kwargs'])
    passed['seed'] += i

    logger.debug("checking if %s already exists", file['output'])
    if file['output'] in static['files']['existing']:
        logger.debug("skipping %s", file['output'])
        return

    logger.info("generating %s", file['target'])
    data['output'] = {
        'metadata': {
            'type': 'dislocation-sample',
            'date': datetime.now(timezone.utc).isoformat(timespec="seconds"),
            'version': version_tuple,
        },
        **static['modules']['dist'].draw(**passed),
    }

    logger.debug("saving %s", file['output'])
    series['output'] = serialize(data['output'], file['output'])
    static['containers']['output'].add(series['output'], file['output'])
