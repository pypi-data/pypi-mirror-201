import click
from vhcs.service import pki


@click.command(hidden=True)
def test():
    return pki.test()
