from vhcs.common.ctxp import context, profile
from .ez_client import EzClient
from . import auth as auth


def _get_auth(client: EzClient, force: bool):
    auth_data = auth.login()
    return "authorization", f"Bearer {auth_data.token}"


def hcs_client(url: str, login: bool = False) -> EzClient:
    if not url:
        url = profile.current().hcs.url
    if url.endswith("/"):
        url = url[:-1]
    _client = EzClient(url, _get_auth)
    if login:
        _client.login()
        context.set("orgId", auth.data().org.id)
    return _client
