import click
from vhcs.service import lcm


@click.command()
@click.argument("id", type=str, required=True)
def get(id: str):
    """Get provider by ID"""
    return lcm.provider.get(id)
