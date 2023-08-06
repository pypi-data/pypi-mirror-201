import click
from vhcs.service import vmhub
from vhcs.util import pki_util


@click.command()
@click.option(
    "--region",
    type=str,
    default=None,
    required=False,
    help="Specify region name",
)
@click.argument("resource-name", type=str, required=True)
@click.argument("otp", type=str, required=True)
def redeem_otp(region: str, resource_name: str, otp: str):
    """Redeem OTP with CSR, receive resource cert."""

    vmhub.use_region(region)
    csr_pem, private_key_pem = pki_util.generate_CSR(resource_name)

    ret = vmhub.redeem_otp(resource_name, otp, csr_pem)
    ret.private_key = private_key_pem
    return ret
