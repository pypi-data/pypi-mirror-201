import logging
import pathlib
import tomlkit


def filename() -> str:
    return "config.toml"


def home() -> str:
    return str(_home())


def _home() -> pathlib.Path:
    _path = pathlib.Path.home()
    return _path.joinpath(".webdav3-cli")


def filepath() -> str:
    return str(_filepath())


def _filepath() -> pathlib.Path:
    return _home().joinpath(filename())


def load():
    __filepath = _filepath()
    if not __filepath.exists():
        return {}

    with open(__filepath, "r") as config_file:
        toml_doc = tomlkit.load(config_file)

    return toml_doc


def save(toml_doc):
    __filepath = _filepath()
    with open(__filepath, "w") as config_file:
        tomlkit.dump(toml_doc, config_file)
