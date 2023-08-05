# -*- coding: utf-8 -*-

"""Date feature.

This module implements the functionality that allows to display the
date in different time zones.

"""

from logging import getLogger

from datetime import datetime, timezone

from stemplate import config
from stemplate.core.colors import colorize


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
        '--color',
        help="name of the color",
        type=str,
    )


def main(**kwargs):
    """Display the date.

    Keyword Arguments
    -----------------
    color : str
        Name of the color.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('color', config.get(__name__, 'color'))

    logger.debug("retrieving date")
    date = datetime.now(timezone.utc)
    zone = date.astimezone().tzinfo
    str1 = date.isoformat(timespec="seconds")
    str2 = date.astimezone(zone).isoformat(timespec="seconds")
    text = f"{str1} (UTC)\n{str2} ({zone})"

    logger.debug("colorizing text")
    colorized = colorize(text, kwargs['color'])
    print(colorized)
