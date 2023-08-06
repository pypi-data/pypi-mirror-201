import sys
import click
from vhcs.service import lcm


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
def create(file: str, type: str):
    """Create a template"""

    with file:
        payload = file.read()
    return lcm.template.create(payload, type)
