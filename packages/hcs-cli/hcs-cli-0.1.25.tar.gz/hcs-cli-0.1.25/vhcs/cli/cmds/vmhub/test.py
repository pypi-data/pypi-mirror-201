import click
from vhcs.service import vmhub


@click.command(hidden=True)
def test():
    return vmhub.test()
