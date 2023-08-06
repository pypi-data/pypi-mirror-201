import httpx
import jwt
import time
import logging
from vhcs.common.ctxp import jsondot

log = logging.getLogger(__name__)


def _raise_on_4xx_5xx(response):
    response.raise_for_status()


def _log_request(request):
    log.debug(f"--> {request.method} {request.url} {request.headers}")


def _log_response(response):
    request = response.request
    log.debug(f"<-- {request.method} {request.url} - {response.status_code}")


class CspClient:
    def __init__(self, url: str, client_id: str, client_key: str, api_token: str = None) -> None:
        self._base_url = url
        self._client_id = client_id
        self._client_key = client_key
        self._api_token = api_token
        self._access_token = None
        self._org_id = None
        self._org = None
        self._token_expires_at = 0

        self._client = httpx.Client(
            base_url=url,
            timeout=20,
            event_hooks={
                "request": [_log_request],
                "response": [_log_response, _raise_on_4xx_5xx],
            },
        )

    def get_access_token(self, force=False):
        if self._access_token and not force:
            return self._access_token

        if self._api_token:
            resp = self._login_by_api_token()
        else:
            resp = self._login_by_client_id()

        try:
            data = resp.json()
        except:
            log.error(resp.content)
            raise
        token = data["access_token"]
        self._client.headers["authorization"] = "Bearer " + token

        token_ttl_seconds = int(data["expires_in"])
        self._token_expires_at = int(time.time() + token_ttl_seconds)

        decoded = jwt.decode(token, options={"verify_signature": False})
        log.debug(decoded)

        self._org_id = decoded["context_name"]
        self._decoded_jwt = decoded
        self._access_token = token
        return token

    def _login_by_client_id(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        params = {
            "grant_type": "client_credentials",
        }
        return self._client.post(
            "/csp/gateway/am/api/auth/authorize",
            auth=(self._client_id, self._client_key),
            headers=headers,
            params=params,
        )

    def _login_by_api_token(self):
        # curl -X 'POST' \\n  'https://console-stg.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize' \\n  -H 'accept: application/json' \\n  -H 'Content-Type: application/x-www-form-urlencoded' \\n  -d 'api_token=vA24tXLuWUlDmu-84ar5nl2zItvctRBKPOUyuBnxxPfOiRjEef1jJmDSW_IxRDMP'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        params = {
            "grant_type": "client_credentials",
        }
        return self._client.post(
            "/csp/gateway/am/api/auth/api-tokens/authorize",
            headers=headers,
            params=params,
            data=f"api_token={self._api_token}",
        )

    def get_org_details(self, force=False):
        if not self._org or force:
            try:
                resp = self._client.get(f"/csp/gateway/am/api/orgs/{self._org_id}")
                self._org = jsondot.dotify(resp.json())
            except Exception as e:
                if self._org is None:
                    self._org = jsondot.dotdict()
                self._org.error = f"Fail retrieving org details: {e}"
            self._org.id = self._org_id
        return self._org
