import click
from vhcs.service import lcm


@click.command()
def list():
    """List providers"""
    return lcm.provider.list()
