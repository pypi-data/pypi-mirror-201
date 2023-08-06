import click
from vhcs.service import lcm


@click.command()
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
@click.option("--name", "-n", type=str, required=False, help="Optionally, specify name pattern to find.")
def list(type: str, name: str):
    """List templates"""
    return lcm.template.list(type=type, name=name)
