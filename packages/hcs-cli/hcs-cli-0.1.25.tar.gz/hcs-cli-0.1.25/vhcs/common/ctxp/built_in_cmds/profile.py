import click
import sys
import json
import vhcs.common.ctxp as ctxp


@click.group(cls=ctxp.cli_processor.LazyGroup)
def profile():
    """Commands for profile."""


@profile.command()
def list():
    """List all profile names."""
    return ctxp.profile.list()


@profile.command()
@click.argument("name")
def use(name: str):
    """Switch to a specific profile."""
    success = ctxp.profile.use(name) != None

    if not success:
        ctxp.panic("No such profile: " + name)


@profile.command()
@click.argument("name", required=False)
def get(name: str):
    """Get content of a specific profile."""
    if name:
        data = ctxp.profile.get(name)
    else:
        data = ctxp.profile.current()

    if data == None:
        ctxp.panic(
            "Profile not set. Use 'hcs profile use <profile-name>' to choose one, or 'hcs profile init' to crate"
        )
    return data


@profile.command()
@click.argument("name")
def delete(name: str):
    """Delete a profile by name."""
    ctxp.profile.delete(name)


@profile.command()
@click.argument("name", required=False)
def file(name: str):
    """Show file location of a profile by name."""
    if not name:
        name = ctxp.profile.name()
    return ctxp.profile.file(name)


@profile.command()
@click.argument("name", type=str)
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
def create(name: str, file):
    """Create a profile from file or STDIN."""
    with file:
        text = file.read()
    try:
        data = json.loads(text)
    except Exception as e:
        ctxp.panic(f"Invalid json {e}")

    return ctxp.profile.create(name, data)
