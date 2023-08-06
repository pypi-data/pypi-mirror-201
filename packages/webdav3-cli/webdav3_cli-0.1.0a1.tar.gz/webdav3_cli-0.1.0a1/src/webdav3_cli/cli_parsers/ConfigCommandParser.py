from .. import Configuration
from . import DebugParser


def _print_config_items_and_values(args):
    config = Configuration.load()

    print("Saved Configuration Values:")
    if len(config) == 0:
        print("  None")
    else:
        for item in config.items():
            print(f"{item[0]} = {item[1]}")


def _print_config_item(args):
    config = Configuration.load()

    if args.item in config:
        value = config[args.item]
        print(f"{args.item} = {value}")

    else:
        print(f"Item {args.item} was not found in Configuration")


def _set_config_item(args):
    input_ = args.item
    tokens = input_.split("=")
    key = tokens[0]
    value = tokens[1]

    if input_ != f"{key}={value}":
        raise ValueError()

    if value == "None":
        value = None

    config = Configuration.load()
    config[key] = value
    Configuration.save(config)

    print(f"Item {args.item} was set")


def _remove_config_item(args):
    config = Configuration.load()

    key = args.item
    if key not in config:
        print(f"Item {key} was not found in Configuration.")
        return

    config.pop(key)
    Configuration.save(config)
    print(f"Item {key} was removed from Configuration")


def _setup_show_command(subparsers):
    parser = subparsers.add_parser("show", help="Show all the specified configuration items with their values")
    parser.set_defaults(command_func=lambda args: _print_config_items_and_values(args))


def _setup_get_command(subparsers):
    parser = subparsers.add_parser("get", help="Print the value of a specific configuration item")

    parser.add_argument("item", help="item to print")
    parser.set_defaults(command_func=lambda args: _print_config_item(args))


def _setup_set_command(subparsers):
    parser = subparsers.add_parser("set", help="Set a value for a configuration item")

    parser.add_argument("item", help="'item=value' to set")
    parser.set_defaults(command_func=lambda args: _set_config_item(args))


def _setup_remove_command(subparsers):
    parser = subparsers.add_parser("remove", help="Remove an existing configuration item")

    parser.add_argument("item", help="item to remove")
    parser.set_defaults(command_func=lambda args: _remove_config_item(args))


def setup_command(subparsers):
    parser = subparsers.add_parser("config", help='''
        Specify and save default values for hostname, root, user, pass, etc such that they don't have to be provided.''')

    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand")
    subparsers.required = True

    _setup_show_command(subparsers)
    _setup_get_command(subparsers)
    _setup_set_command(subparsers)
    _setup_remove_command(subparsers)

    DebugParser.setup(parser)
