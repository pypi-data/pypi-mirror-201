import click
from vhcs.service import lcm


@click.command(hidden=True)
def test():
    return lcm.test()
