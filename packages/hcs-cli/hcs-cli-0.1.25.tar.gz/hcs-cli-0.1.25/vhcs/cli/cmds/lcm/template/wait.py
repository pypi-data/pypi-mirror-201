import sys
import click
from vhcs.service import lcm


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.File("r"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
def create(file: str, type: str, wait: str):
    """Create a template"""

    with file:
        payload = file.read()
    return lcm.template.create(payload, type)


@click.command()
@click.argument("id", type=str, required=True)
@click.option("--status", "-s", type=str, required=False, help="The target status to wait for.")
@click.option("--timeout", "-t", type=str, required=False, help="Timeout. Examples: '2m', '30s', '1h30m'")
@click.option(
    "--fail-on-other-termination-status",
    "-f",
    type=bool,
    default=True,
    required=False,
    help="Stop waiting if the template reached to non-expected terminal states, e.g. waiting for ERROR but template is READY, or waiting for READY and template is ERROR.",
)
def wait(id: str, status: str, timeout: str, fail_on_other_termination_status: bool):
    """Wait for a template to transit to specific status. If the template"""

    print("TODO")
