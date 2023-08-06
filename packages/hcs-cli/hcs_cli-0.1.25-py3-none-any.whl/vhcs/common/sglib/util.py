import click

option_org_id = click.option(
    "--org",
    type=str,
    default=None,
    required=False,
    help="Specify org ID. If not specified, org ID from the current auth token will be used.",
)


def get_org_id(org: str) -> str:
    if org:
        return org

    from vhcs.common.sglib import auth

    auth_info = auth.login()
    return auth_info.org.id
