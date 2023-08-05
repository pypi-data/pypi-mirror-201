# -*- coding: utf-8 -*-

"""Data extraction feature.

This module implements the functionality that allows you to easily and
quickly extract specific data from files saved in a container.

"""

from json import dumps
from logging import getLogger

import numpy as np

from numlpa import config
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
        '-e',
        '--entry',
        type=str,
        help="path to the field to be extracted (e.g. 'metadata.version')",
        metavar='key1.key2...',
    )
    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        help="path to the output file",
        metavar='path',
    )
    parser.add_argument(
        '-f',
        '--format',
        type=str,
        choices=('json', 'pyc'),
        help="format of the output file",
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        '--first',
        type=int,
        help="select value from the first 'n' files (in alphabetical order)",
        metavar='int',
    )
    selection.add_argument(
        '--last',
        type=int,
        help="select value from the last 'n' files (in alphabetical order)",
        metavar='int',
    )
    treatment = parser.add_mutually_exclusive_group()
    treatment.add_argument(
        '--mean',
        action='store_true',
        help="compute the average of the selected values",
    )
    treatment.add_argument(
        '--deviation',
        action='store_true',
        help="compute the standard deviation of the selected values",
    )


def main(input_path, **kwargs):
    """Extract data from the container.

    Parameters
    ----------
    input_path : str
        Path of the input container.

    Keyword Arguments
    -----------------
    entry : str
        Path to the field to be extracted (e.g. 'metadata.version').
    output : str
        Path to the output file.
    format : str
        Format of the output file.
    first : int
        Select value from the first 'n' files (in alphabetical order).
    last : int
        Select value from the last 'n' files (in alphabetical order).
    mean : bool
        Compute the average of the selected values.
    deviation : bool
        Compute the standard deviation of the selected values.

    """
    containers = {}
    data = {}
    if get_rank() != 0:
        return

    logger.debug("retrieving parameters")
    kwargs.setdefault('format', config.get(__name__, 'format'))
    kwargs.setdefault('first', 0)
    kwargs.setdefault('last', 0)
    kwargs.setdefault('mean', False)
    kwargs.setdefault('deviation', False)

    logger.debug("preparing containers")
    containers['input'] = Container(input_path)
    if 'output_path' in kwargs:
        containers['output'] = Container(kwargs['output_path'], create=True)
    else:
        containers['output'] = None

    logger.debug("checking entry parameter")
    if 'entry' not in kwargs:
        retrieve_entries(containers, data)
        print("available entries:")
        for data_entry, data_type in data['entries']:
            print(f"- {data_entry} ({data_type.__name__})")
        return

    logger.debug("retrieving data")
    retrieve_values(containers, data, kwargs)
    if not containers['output']:
        print(dumps(data['output'], indent=4))


def retrieve_values(containers, data, kwargs):
    """Retrieve data.

    Parameters
    ----------
    containers : dict of Container
        Input and output containers.
    data : dict
        Dictionary in which to place the extracted data.
    kwargs : dict
        Keyword arguments passed to the main function.

    """
    files = {}
    series = {}

    logger.debug("extracting file data")
    data['output'] = []
    files['input'] = containers['input'].names()
    if kwargs['first']:
        files['input'] = files['input'][:kwargs['first']]
    elif kwargs['last']:
        files['input'] = files['input'][-kwargs['last']:]
    series['iterator'] = containers['input'].iterator(files['input'])
    for i in range(len(files['input'])):
        series['input'] = next(series['iterator'])
        data['input'] = deserialize(series['input'], files['input'][i])
        for node in kwargs['entry'].split('.'):
            if isinstance(data['input'], list):
                node = int(node)
            data['input'] = data['input'][node]
        data['output'].append(data.pop('input'))

    logger.debug("processing data")
    if kwargs['mean']:
        data['output'] = np.array(data['output'], dtype=np.float64)
        data['output'] = np.mean(data['output'], axis=0)
    elif kwargs['deviation']:
        data['output'] = np.array(data['output'], dtype=np.float64)
        data['output'] = np.std(data['output'], axis=0)
    if isinstance(data['output'], np.ndarray):
        data['output'] = np.where(
            np.isnan(data['output']),
            None,
            data['output'],
        ).tolist()

    logger.debug("saving data")
    if not containers['output']:
        return
    files['output'] = f"extracted.{kwargs['format']}"
    files['target'] = f"({containers['output']})[{files['output']}]"
    files['existing'] = containers['output'].names()
    if files['output'] in files['existing']:
        logger.debug("skipping %s", files['output'])
        return
    logger.info("generating %s", files['target'])
    series['output'] = serialize(data['output'], files['output'])
    containers['output'].add(series['output'], files['output'])


def retrieve_entries(containers, data):
    """Get available entries from the container.

    Parameters
    ----------
    containers : dict of Container
        Input and output containers.
    data : dict
        Dictionary in which to place the extracted data.

    """
    series = {}
    files = {}

    logger.debug("extracting first file")
    files['input'] = containers['input'].names()
    series['input'] = containers['input'].get(files['input'][0])
    data['input'] = deserialize(series['input'], files['input'][0])

    def rec(node, parents):
        if isinstance(node, dict):
            entries = []
            for child in node:
                entries += rec(node[child], parents+[child])
            return entries
        return [('.'.join(parents), type(node))]

    logger.debug("retrieving values")
    data['entries'] = rec(data['input'], [])
