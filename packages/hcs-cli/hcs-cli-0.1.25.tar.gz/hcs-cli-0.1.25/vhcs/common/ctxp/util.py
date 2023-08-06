import json
import sys
import click
import typing


class CtxpException(Exception):
    pass


def print_output(data: any, output: str = "json"):
    if type(data) is str:
        text = data
    elif output == "json-compact":
        text = json.dumps(data)
    elif output == "yaml":
        import yaml
        import vhcs.common.ctxp as ctxp

        text = yaml.dump(ctxp.jsondot.plain(data))
    elif output == "text":
        text = json.dumps(data, indent=4)
    else:
        text = json.dumps(data, indent=4)
    print(text, end="")


def panic(reason: any = None, code: int = 1):
    print(reason, file=sys.stderr)
    sys.exit(code)


F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])


def command(
    name: typing.Optional[str] = None,
    cls: typing.Optional[typing.Type[click.Command]] = None,
    **attrs: typing.Any,
) -> typing.Callable[[F], click.Command]:
    print("wrapping")
    return click.command(name, cls, **attrs)


option_verbose = click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="Print debug logs",
)

option_output = click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "json-compact", "yaml", "text"]),
    default="json",
    help="Specify output format",
)
