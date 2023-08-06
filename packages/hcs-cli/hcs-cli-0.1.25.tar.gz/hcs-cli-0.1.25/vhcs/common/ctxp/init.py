import click
from os import path
from pathlib import Path
from . import profile
from . import config
from . import cli_processor

user_home = str(Path.home())


def init(
    cli_name: str,
    main_cli: click.Group,
    commands_dir: str = "./cmds",
    store_path: str = user_home,
    config_path="./config",
):
    real_store_path = path.join(store_path, "." + cli_name)
    profile_path = path.join(real_store_path, "profile")
    profile.init(profile_path)
    config._init(config_path)

    return cli_processor.init(main_cli, commands_dir)
