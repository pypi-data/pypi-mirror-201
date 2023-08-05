# -*- coding: utf-8 -*-

"""Text colorization.

This module implements features related to text colorization.

"""

from codecs import decode
from logging import getLogger

from stemplate import config


logger = getLogger(__name__)


def get_code(name):
    """Return the color code.

    Parameters
    ----------
    name : str
        Name of the color code in the configuration file.

    Returns
    -------
    str
        Color code.

    """
    logger.debug("retrieving '%s' color code", name)
    color = config.get(__name__, name)
    return decode(color, 'unicode_escape')


def colorize(string, color):
    """Return the colorized string.

    Parameters
    ----------
    string : str
        The text to colorize.
    color : str
        The name of the color.

    Returns
    -------
    str
        Colorized text.

    """
    logger.debug("colorizing text with color '%s'", color)
    start = get_code(color)
    end = get_code('end')
    return start + string + end
