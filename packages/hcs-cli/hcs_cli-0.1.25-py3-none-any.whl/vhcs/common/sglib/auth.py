import time
import logging
import hashlib
from vhcs.common.ctxp import profile, context, jsondot, panic
from .csp import CspClient

log = logging.getLogger(__name__)


def _validate_profile_readiness():
    csp_data = profile.current().csp
    if not csp_data:
        panic(f"Profile property missing: profile.csp. Current profile: {profile.name()}")
    if csp_data.apiToken:
        return
    if csp_data.clientId and csp_data.clientKey:
        return
    panic(
        f"Profile property missing. profile.csp requires either apiToken, or clientId/clientKey configured. Current profile: {profile.name()}"
    )


def _get_profile_user_hash():
    csp = profile.current().csp
    text = f"{csp.url}{csp.clientId}{csp.clientKey}{csp.apiToken}"
    return hashlib.md5(text.encode("ascii")).hexdigest()


def _is_auth_expired(data):
    return data.token == None or time.time() + 5 * 60 > data.token_expires_at


def data():
    profile_auth, all_auth = _data()
    return profile_auth


def _data():
    all_auth = context.get(".auth", default=dict())
    profile_user = _get_profile_user_hash()
    profile_auth = all_auth.get(profile_user)
    if profile_auth is None:
        profile_auth = jsondot.dotdict()
        all_auth[profile_user] = profile_auth
    return profile_auth, all_auth


def login(force_refresh: bool = False):
    _validate_profile_readiness()

    profile_auth, all_auth = _data()

    if force_refresh or _is_auth_expired(profile_auth):
        csp_data = profile.current().csp
        csp_client = CspClient(
            url=csp_data.url,
            client_id=csp_data.clientId,
            client_key=csp_data.clientKey,
            api_token=csp_data.apiToken,
        )
        profile_auth.token = csp_client.get_access_token()
        profile_auth.org = csp_client.get_org_details()
        profile_auth.token_expires_at = csp_client._token_expires_at
        profile_auth.jwt = csp_client._decoded_jwt
        expires_in_minutes = int((profile_auth.token_expires_at - time.time()) / 60)
        log.debug(
            f"Acquired new token [{profile_auth.org.displayName}/{profile_auth.org.id}], expires in {expires_in_minutes} minutes"
        )
        context.set(".auth", all_auth)
    else:
        expires_in_minutes = int((profile_auth.token_expires_at - time.time()) / 60)
        log.debug(
            f"Reusing existing token [{profile_auth.org.displayName}/{profile_auth.org.id}], expires in {expires_in_minutes} minutes"
        )
    return profile_auth
