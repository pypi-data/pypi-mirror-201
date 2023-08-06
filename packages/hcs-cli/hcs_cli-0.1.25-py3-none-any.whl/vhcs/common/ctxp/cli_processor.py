import click
import sys
import yaml
from click.core import Group
import os.path as path
import os
import importlib
import importlib.util
from pathlib import Path
from . import util

_eager_loading = os.environ.get("_CTXP_EAGER_LOAD")
if _eager_loading:
    print("_CTXP_EAGER_LOAD:", _eager_loading, file=sys.stderr)


class LazyGroup(click.Group):
    def __init__(self, mod_path: Path = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mod_path = mod_path
        self._lazy_commands_loaded = False
        if _eager_loading:
            self._ensure_subcommands()

    def list_commands(self, ctx):
        self._ensure_subcommands()
        return super().list_commands(ctx)

    def get_command(self, ctx, cmd_name):
        self._ensure_subcommands()
        return super().get_command(ctx, cmd_name)

    def _ensure_subcommands(self):
        if not self._lazy_commands_loaded and self.mod_path:
            _add_subcommands(self.mod_path.absolute(), self)
            self._lazy_commands_loaded = True


def _add_built_in_commands(group: Group):
    script_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), "."))
    build_in_cmds_dir = path.join(script_dir, "built_in_cmds")
    _add_subcommands(build_in_cmds_dir, group)


def _ensure_sub_group(current: Group, mod_path: Path):
    name = mod_path.name
    help = _read_group_meta(mod_path).get("help")
    subgroup = current.commands.get(name)
    if subgroup and isinstance(subgroup, Group):
        if isinstance(subgroup, LazyGroup):
            subgroup.mod_path = mod_path
        return subgroup

    subgroup = LazyGroup(name=name, help=help, mod_path=mod_path)
    current.add_command(subgroup)
    return subgroup


def _read_group_meta(mod_path: Path) -> dict:
    meta_file = mod_path.absolute().joinpath("meta.yaml")
    if not meta_file.exists():
        return {}
    with open(meta_file, "r") as f:
        return yaml.safe_load(f)


_excluded_names = ["__pycache__", "__init__.py", ".DS_Store"]


def _add_subcommands(commands_dir: str, group: Group):
    for mod_path in Path(commands_dir).glob("*"):
        if mod_path.name in _excluded_names:
            continue
        if mod_path.is_dir():
            _ensure_sub_group(group, mod_path)
        elif mod_path.name.endswith(".py"):
            _import_cmd_file(mod_path, group)
        else:
            pass
            # print("Unrecognized sub cmd: " + mod_path.name)
    return


def _import_cmd_file(mod_path: Path, parent: click.core.Group):
    mod_name = f"ctxp#{mod_path}"
    # print("Loading ---> ", mod_name)

    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # mod = importlib.import_module(mod_name)
    # filter out any things that aren't a click Command
    cli_methods = []
    for attr in dir(mod):
        foo = getattr(mod, attr)
        if callable(foo):
            cli_methods.append(foo)

    for foo in cli_methods:
        if isinstance(foo, click.core.Group):
            parent.add_command(foo)
            return  # only the first one. This enables single-file group of commands.

    for foo in cli_methods:
        if isinstance(foo, click.core.Command):
            parent.add_command(foo)


def _process_result(result, **kwargs):
    if result is not None:
        if isinstance(result, tuple):
            data, return_code = result
            if data is not None:
                util.print_output(data, kwargs.get("output"))
            if isinstance(return_code, int):
                ctx = click.get_current_context()
                ctx.exit(return_code)
            else:
                raise Exception("Invalid command return code. Expect int, actual=" + str(type(return_code)))
        else:
            util.print_output(result, kwargs.get("output"))


def init(main_cli: click.Group, commands_dir: str):
    _add_built_in_commands(main_cli)
    _add_subcommands(commands_dir, main_cli)
    main_cli.result_callback()(_process_result)
    return main_cli(obj={})
