import click
from vhcs.service import pki
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@option_org_id
def get_org_cert(org: str):
    """Get the signing certificate of a specific org"""
    org_id = get_org_id(org)
    return pki.get_org_cert(org_id)
