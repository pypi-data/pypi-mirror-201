import click
from vhcs.service import lcm


@click.command()
@click.argument("id", type=str, required=True)
def delete(id: str):
    """Delete provider by ID"""
    return lcm.provider.delete(id)
