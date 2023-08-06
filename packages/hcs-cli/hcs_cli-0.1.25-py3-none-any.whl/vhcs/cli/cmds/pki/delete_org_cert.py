import click
from vhcs.common.ctxp import panic
from vhcs.service import pki
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command()
@option_org_id
@click.option("--confirm/--no-confirm", default=False)
def delete_org_cert(org: str, confirm: bool):
    """Delete the signing certificate of a specific org"""

    if not confirm:
        panic('Delete an org certificate will impact some service. Specify "--confirm" to perform the deletion.')
    org_id = get_org_id(org)
    return pki.delete_org_cert(org_id)
