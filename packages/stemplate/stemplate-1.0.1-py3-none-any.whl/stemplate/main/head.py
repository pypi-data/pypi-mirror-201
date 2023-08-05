# -*- coding: utf-8 -*-

"""Head feature.

This module implements the functionality that allows to display
the first lines of a file.

"""

from logging import getLogger

from stemplate import config
from stemplate.core.colors import colorize
from stemplate.core.files import get_beginning, get_size


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
        'file',
        help="path to the file",
        type=str,
    )
    parser.add_argument(
        '--color',
        help="name of the color",
        type=str,
    )
    parser.add_argument(
        '--lines',
        help="number of lines to display",
        type=int,
    )


def main(file, **kwargs):
    """Display the first lines of the file.

    Parameters
    ----------
    file : str
        Path to the file.

    Keyword Arguments
    -----------------
    lines : int
        Number of lines to display.
    color : str
        Name of the color.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('lines', config.get(__name__, 'lines'))
    kwargs.setdefault('color', config.get(__name__, 'color'))

    logger.debug("retrieving data")
    content = get_beginning(file, kwargs['lines'])
    size = get_size(file)

    logger.debug("colorizing text")
    colored = colorize(content, kwargs['color'])
    print(f"{colored}...\n(file size: {size} bytes)")
