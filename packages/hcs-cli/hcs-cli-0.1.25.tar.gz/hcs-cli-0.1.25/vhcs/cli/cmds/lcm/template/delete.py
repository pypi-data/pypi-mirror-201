import click
from vhcs.service import lcm


@click.command()
@click.argument("id", type=str, required=True)
@click.option(
    "--force/--safe", default=False, help="In 'force' mode, the template deletion will continue and ignore any error."
)
def delete(id: str, force: bool):
    """Delete template by ID"""
    return lcm.template.delete(id, force)
