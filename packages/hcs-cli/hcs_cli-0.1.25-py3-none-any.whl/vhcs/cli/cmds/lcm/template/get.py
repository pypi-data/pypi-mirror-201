import click
from vhcs.service import lcm


@click.command()
@click.argument("id", type=str, required=True)
def get(id: str):
    """Get template by ID"""
    return lcm.template.get(id)
