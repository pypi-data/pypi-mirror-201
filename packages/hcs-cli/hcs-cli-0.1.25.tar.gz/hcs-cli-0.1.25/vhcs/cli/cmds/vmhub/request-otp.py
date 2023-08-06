import click
from vhcs.common.sglib.util import option_org_id, get_org_id
from vhcs.service import vmhub


@click.command()
@option_org_id
@click.option(
    "--region",
    type=str,
    default=None,
    required=False,
    help="Specify region name",
)
@click.argument("resource-name", type=str, required=True)
def request_otp(org: str, region: str, resource_name: str):
    """Request an one-time password for a specific resource"""
    org_id = get_org_id(org)
    vmhub.use_region(region)
    return vmhub.request_otp(org_id, resource_name)
