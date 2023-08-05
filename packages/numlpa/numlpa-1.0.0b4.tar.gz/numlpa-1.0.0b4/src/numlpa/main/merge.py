# -*- coding: utf-8 -*-

"""Data fusion feature.

This module implements the functionality to merge data from several
similar files into a single file.

"""

from datetime import datetime, timezone
from logging import getLogger
from os.path import splitext

import numpy as np

from numlpa import config
from numlpa._version import version_tuple
from numlpa.core.parallelism import get_rank
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


def main(input_path, output_path, **kwargs):
    """Merge the files.

    Parameters
    ----------
    input_path : str
        Path of the input container.
    output_path : str
        Path of the output container.

    Keyword Arguments
    -----------------
    format : str
        Format of the output file.

    """
    containers = {}
    data = {}
    files = {}
    series = {}
    if get_rank() != 0:
        return

    logger.debug("retrieving parameters")
    kwargs.setdefault('format', config.get(__name__, 'format'))

    logger.debug("preparing containers")
    containers['input'] = Container(input_path)
    containers['output'] = Container(output_path, create=True)

    logger.debug("preparing file names")
    files['input'] = containers['input'].names()
    files['existing'] = containers['output'].names()
    files['stems'] = [splitext(files['input'][i])[0] for i in [0, -1]]
    files['output'] = f"{'-'.join(files['stems'])}.{kwargs['format']}"
    files['target'] = f"({containers['output']})[{files['output']}]"

    logger.debug("checking if %s already exists", files['output'])
    if files['output'] in files['existing']:
        logger.debug("skipping %s", files['output'])
        return

    logger.debug("loading data")
    data['input'] = []
    containers['iterator'] = containers['input'].iterator(files['input'])
    for i in range(len(files['input'])):
        logger.debug("loading %s", files['input'][i])
        series['input'] = next(containers['iterator'])
        data['input'].append(deserialize(series['input'], files['input'][i]))

    logger.debug("checking files")
    try:
        data['type'] = data['input'][0]['metadata']['type']
    except (KeyError, TypeError) as exc:
        raise RuntimeError("can not parse data from container") from exc
    if data['type'] == 'fourier-transform':
        process_transforms(containers, files, data)
    elif data['type'] == 'spatial-analysis':
        raise NotImplementedError()
    else:
        raise TypeError(f"can not merge data of type {data['type']}")


def process_transforms(containers, files, data):
    """Merge the Fourier transforms.

    Parameters
    ----------
    containers : dict of Container
        Input and output containers.
    files : dict of list
        Input and output files names.
    data : dict
        Input and output files data.

    """
    series = {}

    logger.debug("gathering coefficients")
    data['output'] = dict(data['input'][0])
    data['cos'] = []
    data['sin'] = []
    for i in range(len(data['input'])):
        if data['input'][i]['metadata']['type'] != 'fourier-transform':
            raise TypeError(f"{files['input'][i]} is not a Fourier transform")
        data['cos'].append(data['input'][i]['coefficients'].pop('cos_mean'))
        data['sin'].append(data['input'][i]['coefficients'].pop('sin_mean'))

    logger.debug("conputing mean and deviation")
    data['avg_cos'] = np.average(data['cos'], axis=0)
    data['avg_sin'] = np.average(data['sin'], axis=0)
    data['coefficient'] = 1/np.sqrt(len(files['input']))
    data['std_cos'] = np.std(data['cos'], axis=0) * data['coefficient']
    data['std_sin'] = np.std(data['sin'], axis=0) * data['coefficient']

    logger.info("generating %s", files['target'])
    data['output']['diffraction']['samples'] = len(files['input'])
    data['output']['coefficients']['cos_mean'] = data['avg_cos'].tolist()
    data['output']['coefficients']['sin_mean'] = data['avg_sin'].tolist()
    data['output']['coefficients']['cos_deviation'] = data['std_cos'].tolist()
    data['output']['coefficients']['sin_deviation'] = data['std_sin'].tolist()
    data['output']['metadata'] = {
        'type': 'fourier-transform',
        'date': datetime.now(timezone.utc).isoformat(timespec="seconds"),
        'version': version_tuple,
    }

    logger.debug("saving %s", files['output'])
    series['output'] = serialize(data['output'], files['output'])
    containers['output'].add(series['output'], files['output'])
