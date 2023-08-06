from webdav3_cli.cli_parsers import ArgumentParser
from webdav3_cli.cli_parsers import UploadCommandParser, ListCommandParser, ConfigCommandParser

import logging
import sys


__version = "1.0.0"


def _setup_logging():
    logging.basicConfig(level=logging.DEBUG)


def _setup_parser():
    command = __package__.split('_')[0]
    parser = ArgumentParser(prog=command)
    parser.add_argument("-v", "--version", action="version", version=__version)

    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand")
    subparsers.required = True

    UploadCommandParser.setup_command(subparsers)
    ListCommandParser.setup_command(subparsers)
    ConfigCommandParser.setup_command(subparsers)

    return parser


def main(args=None):
    parser = _setup_parser()
    if not args:
        args = sys.argv[1:]

    parsed = parser.parse_args(args)
    if parsed.debug:
        _setup_logging()

    parsed.command_func(parsed)


if __name__ == '__main__':
    main()
