import click
import vhcs.common.sglib as sglib


@click.command()
@click.option("--details/--no-details", default=False)
@click.option("--refresh/--no-refresh", default=False)
def auth(details: bool, refresh: bool):
    """Print the API auth token."""
    data = sglib.auth.login(force_refresh=refresh)
    if details:
        return data
    else:
        return data.token
