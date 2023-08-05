# -*- coding: utf-8 -*-

"""Spatial analysis feature.

This module implements the functionality to compute the strain energy
and the interdislocation statistics of a group of dislocation samples.

"""

from datetime import datetime, timezone
from logging import getLogger
from os.path import splitext

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

    logger.debug("defining command-line subparsers")
    subparsers = parser.add_subparsers(
        dest='analyzer',
        help="name of the module used for analysis",
    )
    for name in kits.names('analyzers'):
        subparser = subparsers.add_parser(
            name=name,
            help=f'analyze with {name} analyzer',
        )
        module = kits.get('analyzers', name)
        module.setup(subparser)


def main(input_path, output_path, **kwargs):
    """Analize.

    Parameters
    ----------
    input_path : str
        Path of the input container.
    output_path : str
        Path of the output container.

    Keyword Arguments
    -----------------
    analyzer : str
        Name of the module used for analizing.
    format : str
        Format of the output files.

    """
    containers = {}
    files = {}
    modules = {}

    logger.debug("retrieving parameters")
    kwargs.setdefault('analyzer', config.get(__name__, 'analyzer'))
    kwargs.setdefault('format', config.get(__name__, 'format'))

    logger.debug("preparing containers")
    containers['input'] = Container(input_path)
    containers['output'] = Container(output_path, create=True)

    logger.debug("preparing file names")
    files['input'] = containers['input'].names()
    files['stems'] = [splitext(name)[0] for name in files['input']]
    files['output'] = [f"{stem}.{kwargs['format']}" for stem in files['stems']]
    files['existing'] = containers['output'].names()

    logger.debug("preparing submodules")
    modules['analyze'] = kits.get('analyzers', kwargs['analyzer'])

    logger.debug("generating files")
    static = {
        'containers': containers,
        'files': files,
        'kwargs': kwargs,
        'modules': modules,
    }
    for i in range(get_rank(), len(files['input']), get_size()):
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
    file['input'] = static['files']['input'][i]
    file['output'] = static['files']['output'][i]
    file['target'] = f"({static['containers']['output']})[{file['output']}]"
    passed.update(static['kwargs'])

    logger.debug("checking if %s already exists", file['output'])
    if file['output'] in static['files']['existing']:
        logger.debug("skipping %s", file['output'])
        return

    logger.debug("loading %s", file['input'])
    series['input'] = static['containers']['input'].get(file['input'])
    data['input'] = deserialize(series['input'], file['input'])

    logger.debug("checking %s", file['input'])
    try:
        data['type'] = data['input']['metadata']['type']
    except (KeyError, TypeError) as exc:
        raise RuntimeError(f"can not parse data from {file['input']}") from exc
    if data['type'] != 'dislocation-sample':
        raise TypeError(f"invalid data type {data['type']}")

    logger.info("generating %s", file['target'])
    data['output'] = {
        'metadata': {
            'type': 'spatial-analysis',
            'date': datetime.now(timezone.utc).isoformat(timespec="seconds"),
            'version': version_tuple,
        },
        **static['modules']['analyze'].analyze(data['input'], **passed),
    }

    logger.debug("saving %s", file['output'])
    series['output'] = serialize(data['output'], file['output'])
    static['containers']['output'].add(series['output'], file['output'])
