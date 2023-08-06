import click
from vhcs.service import pki


@click.command()
def get_root_ca():
    """Get the certificate of the root CA."""
    return pki.get_root_ca()
