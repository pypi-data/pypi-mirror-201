# -*- coding: utf-8 -*-

"""Stemplate command-line interface.

This module allows the user to launch the main features of the package
from a command-line interface.

"""

from argparse import ArgumentParser
from logging import getLogger
from sys import exit as sys_exit

from stemplate import config
from stemplate._version import version
from stemplate.main import date, head


logger = getLogger(__name__)


def main():
    """Run the command-line interpreter.

    """
    logger.debug("defining command-line arguments")
    parser = ArgumentParser(
        prog=__package__,
        description=__doc__,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'%(prog)s {version}',
    )
    parser.add_argument(
        '-c',
        '--config',
        help="custom configuration file path",
        metavar='path',
    )
    parser.add_argument(
        '-l',
        '--log',
        help="logging level",
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
    )

    logger.debug("defining subparsers")
    subparsers = parser.add_subparsers(
        required=True,
        help="name of the command to run",
    )
    for module in (head, date):
        subparser = subparsers.add_parser(
            name=module.__name__.rsplit('.', maxsplit=1)[-1],
            help=f"run {module.__name__} module",
        )
        module.setup(subparser)

    logger.debug("parsing command-line arguments")
    args = parser.parse_args()
    kwargs = {key: val for key, val in vars(args).items() if val is not None}
    kwargs.pop('func')
    logger.debug("parsed arguments: %s", kwargs)

    logger.debug("running command")
    try:
        if args.log:
            getLogger().setLevel(args.log)
        if args.config:
            logger.info("loading custom configuration file")
            with open(args.config, encoding='utf-8') as file:
                config.read_file(file)
        logger.debug("executing command function")
        args.func(**kwargs)
    except SystemExit:
        logger.info("program exited")
        sys_exit(0)
    except KeyboardInterrupt:
        logger.info("program interrupted by Control-C")
        sys_exit(130)
    except FileNotFoundError as exception:
        logger.error(exception)
        sys_exit(1)


if __name__ == '__main__':
    main()
