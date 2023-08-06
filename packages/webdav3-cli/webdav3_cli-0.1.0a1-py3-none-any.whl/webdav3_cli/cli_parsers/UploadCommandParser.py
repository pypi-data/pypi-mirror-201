from .. import webdav3client_wrapper
from . import DebugParser
import os


def _execute(args):
    webdav3client_wrapper.upload(args.local_path, args.hostname, args.root, args.remote_path, args.user, args.password)
    print("Upload complete")


def setup_command(subparsers):
    parser = subparsers.add_parser("upload", help='''
        Upload a resource to a remote path on WebDAV server. 
        In case resource is directory it will upload all nested files and directories.''')

    parser.set_defaults(command_func=lambda args: _execute(args))

    parser.add_argument("local_path",
                        type=os.path.abspath,
                        help="Path to the file or folder to be uploaded")
    parser.add_argument("remote_path",
                        help="Path to the upload location")
    parser.add_argument("--hostname")
    parser.add_argument("--root")
    parser.add_argument("--user")
    parser.add_argument("--pass", dest="password")

    DebugParser.setup(parser)
