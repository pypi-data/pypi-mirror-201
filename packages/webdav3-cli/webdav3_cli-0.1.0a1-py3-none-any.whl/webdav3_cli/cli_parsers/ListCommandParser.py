from .. import webdav3client_wrapper
from . import DebugParser


def _execute(args):
    results = webdav3client_wrapper.list(args.hostname, args.root, args.remote_path, args.user, args.password)
    results.sort()
    for result in results:
        print(result)


def setup_command(subparsers):
    parser = subparsers.add_parser("list", help='''
        Get the list of resources at a remote path on the WebDAV server.''')

    parser.set_defaults(command_func=lambda args: _execute(args))

    parser.add_argument("remote_path")
    parser.add_argument("--hostname")
    parser.add_argument("--root")
    parser.add_argument("--user")
    parser.add_argument("--pass", dest="password")

    DebugParser.setup(parser)
