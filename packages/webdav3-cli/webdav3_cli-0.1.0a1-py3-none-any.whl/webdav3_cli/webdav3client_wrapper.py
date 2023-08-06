from . import Configuration
import webdav3.client as webdav
import logging
import pathlib


_logger = logging.getLogger(__package__)


def _create_client(config):
    options = {
        "webdav_hostname": config["hostname"],
        "webdav_root": config["root"],
        "webdav_login": config["user"],
        "webdav_password": config["pass"],
    }

    return webdav.Client(options)


def _load_config(hostname, root_path, remote_path, user, password):
    config = Configuration.load()
    if hostname is not None:
        config["hostname"] = hostname

    if root_path is not None:
        config["root"] = root_path

    if user is not None:
        config["user"] = user

    if password is not None:
        config["pass"] = password

    if remote_path is not None:
        config["remote_path"] = remote_path

    return config


def list(hostname, root_path, remote_path, user, password):
    _logger.log(logging.DEBUG, "Executing list({hostname}, {root_path}, {remote_path}, {user}, {password})")

    config = _load_config(hostname, root_path, remote_path, user, password)
    client = _create_client(config)
    artifacts = client.list(config["remote_path"])
    return artifacts


def upload(local_path, hostname, root_path, remote_path, user, password):
    _logger.log(logging.DEBUG, f"Executing upload({local_path}, {hostname}, {root_path}, {remote_path}, {user}, {password})")

    config = _load_config(hostname, root_path, remote_path, user, password)

    local_path = pathlib.Path(local_path)
    remote_path = pathlib.Path(config["remote_path"])

    basename = local_path.name
    remote_path = remote_path.joinpath(basename)

    client = _create_client(config)
    client.upload_sync(remote_path.as_posix(), local_path)

