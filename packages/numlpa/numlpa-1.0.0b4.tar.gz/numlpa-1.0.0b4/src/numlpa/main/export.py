# -*- coding: utf-8 -*-

"""Illustration feature.

This module implements the functionality to generate and save the
figures corresponding to the data stored in a container.

"""

from io import BytesIO
from logging import getLogger
from os.path import splitext

from matplotlib import font_manager
from matplotlib.pyplot import close, rcParams

from numlpa import config, kits
from numlpa.kits import fonts
from numlpa._version import version
from numlpa.core.parallelism import get_rank, get_size
from numlpa.core.storage import Container, deserialize


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
        choices=('pdf', 'svg', 'png'),
        help="output data files format",
    )
    parser.add_argument(
        '--font',
        type=str,
        choices=fonts.names(),
        help="text font used in the figures",
    )
    parser.add_argument(
        '--math',
        type=str,
        help="math font used in the figures",
        metavar='str',
    )
    parser.add_argument(
        '--size',
        type=int,
        help="font size used in the figures (pt)",
        metavar='int',
    )
    parser.add_argument(
        '--dpi',
        type=int,
        help="dots per inch",
        metavar='int',
    )

    logger.debug("defining command-line subparsers")
    subparsers = parser.add_subparsers(
        dest='representation',
        help="name of module used for illustration",
    )
    for name in kits.names('representations'):
        subparser = subparsers.add_parser(
            name=name,
            help=f"illustrate with {name} representation",
        )
        module = kits.get('representations', name)
        module.setup(subparser)


def main(input_path, output_path, **kwargs):
    """Generate figures.

    Parameters
    ----------
    input_path : str
        Path of the input container.
    output_path : str
        Path of the output container.

    Keyword Arguments
    -----------------
    representation : str
        Name of module used for illustration.
    format : str
        Output data files format.
    font : str
        Text font used in the figures.
    math : str
        Math font used in the figures.
    size : int
        Font size used in the figures (pt).
    dpi : int
        Dots per inch.

    """
    containers = {}
    files = {}
    modules = {}

    logger.debug("retrieving parameters")
    kwargs.setdefault('representation', config.get(__name__, 'representation'))
    kwargs.setdefault('format', config.get(__name__, 'format'))
    kwargs.setdefault('font', config.get(__name__, 'font'))
    kwargs.setdefault('math', config.get(__name__, 'math'))
    kwargs.setdefault('size', config.getint(__name__, 'size'))
    kwargs.setdefault('dpi', config.getint(__name__, 'dpi'))

    logger.debug("loading fonts")
    prop = font_manager.FontProperties(fname=fonts.path(kwargs['font']))
    font_manager.fontManager.addfont(fonts.path(kwargs['font']))
    rcParams["font.family"] = prop.get_name()
    rcParams["mathtext.fontset"] = kwargs['math']
    rcParams["font.size"] = kwargs['size']
    rcParams["legend.fontsize"] = kwargs['size']
    rcParams["axes.titlesize"] = kwargs['size']
    rcParams["figure.titlesize"] = kwargs['size']

    logger.debug("preparing containers")
    containers['input'] = Container(input_path)
    containers['output'] = Container(output_path, create=True)

    logger.debug("preparing file names")
    files['input'] = containers['input'].names()
    files['stems'] = [splitext(name)[0] for name in files['input']]
    files['output'] = [f"{stem}.{kwargs['format']}" for stem in files['stems']]
    files['existing'] = containers['output'].names()

    logger.debug("preparing submodules")
    modules['repr'] = kits.get('representations', kwargs['representation'])

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

    Raises
    ------
    TypeError
        If the input data format is not recognized.

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
    if data['type'] == 'dislocation-sample':
        data['function'] = 'sample'
        data['title'] = "Dislocation map"
    elif data['type'] == 'fourier-transform':
        data['function'] = 'transform'
        data['title'] = "Diffraction profile"
    elif data['type'] == 'model-adjustment':
        data['function'] = 'adjustment'
        data['title'] = "Model adjustment"
    else:
        raise TypeError(f"can not represent data type {data['type']}")
    if hasattr(static['modules']['repr'], data['function']):
        generator = getattr(static['modules']['repr'], data['function'])
    else:
        logger.warning(
            "module '%s' can not be used to represent '%s' data, "
            "switched to 'basic' representation module",
            static['modules']['repr'].__name__,
            data['type'],
        )
        static['modules']['repr'] = kits.get('representations', 'basic')
        generator = getattr(static['modules']['repr'], data['function'])

    logger.info("generating %s", file['target'])
    data['output'] = {}
    data['output']['fig'] = generator(data['input'], **passed)
    data['output']['metadata'] = {
        'Title': data['title'],
        'Creator': f'NumLPA {version}',
    }
    series['buffer'] = BytesIO()
    data['output']['fig'].savefig(
        series['buffer'],
        format=passed['format'],
        dpi=passed['dpi'],
        metadata=data['output']['metadata'],
    )
    close(data['output']['fig'])
    series['buffer'].seek(0)

    logger.debug("saving %s", file['output'])
    series['output'] = bytes(series['buffer'].read())
    static['containers']['output'].add(series['output'], file['output'])
