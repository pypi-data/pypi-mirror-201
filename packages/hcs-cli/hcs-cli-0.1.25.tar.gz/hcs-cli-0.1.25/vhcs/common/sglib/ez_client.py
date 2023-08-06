from http.client import HTTPResponse
import httpx
import logging
import json
from vhcs.common.ctxp import jsondot

log = logging.getLogger(__name__)

log_http_details = False


def _raise_on_4xx_5xx(response: httpx.Response):
    response.read()  # read the content so the response can be dumped later
    response.raise_for_status()


def _try_formatting_json(text: str):
    try:
        return json.dumps(json.loads(text), indent=4)
    except:
        return text


def _log_request(request):
    if not log.isEnabledFor(logging.DEBUG):
        return
    log.debug("\n")
    log.debug(f"--> {request.method} {request.url}")
    log.debug(f"--> {request.headers}")

    if len(request.content) > 0:
        text = _try_formatting_json(request.content)
        log.debug(text)


def _log_response(response: httpx.Response):
    if not log.isEnabledFor(logging.DEBUG):
        return
    request = response.request
    log.debug(f"<-- {request.method} {request.url} - {response.status_code}")
    log.debug(f"<-- {request.headers}")
    response.read()
    if len(response.text) > 0:
        text = _try_formatting_json(response.text)
        log.debug(text)
    log.debug("\n")


def _parse_resp(resp: httpx.Response):
    if not resp.content:
        return None
    content_type = resp.headers["Content-Type"]
    if content_type.startswith("text"):
        return resp.text
    if len(resp.content) > 3:
        try:
            data = resp.json()
            return jsondot.dotify(data)
        except:
            log.info("--- Fail parsing json. Dump content ---")
            log.info(resp.content)
            raise
    else:
        return None


def on404ReturnNone(func):
    try:
        resp = func()
        return _parse_resp(resp)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise


class EzClient:
    def __init__(self, base_url: str, get_auth: callable = None) -> None:
        event_hooks = {"response": [_raise_on_4xx_5xx]}
        event_hooks["request"] = [_log_request]
        event_hooks["response"].insert(0, _log_response)

        self._client = httpx.Client(base_url=base_url, timeout=30, event_hooks=event_hooks)
        self._get_auth = get_auth

    def login(self, force: bool = False):
        header_name, header_value = self._get_auth(self, force)
        self._client.headers[header_name] = header_value

    def post(self, url: str, json: dict = None, text: str = None, headers: dict = None):
        self.login()
        if text:
            resp = self._client.post(url, content=text, headers=headers)
        else:
            resp = self._client.post(url, json=json)
        return _parse_resp(resp)

    def get(self, url: str, raise_on_404: bool = False):
        self.login()
        try:
            resp = self._client.get(url)
            return _parse_resp(resp)
        except httpx.HTTPStatusError as e:
            print(e)
            if not raise_on_404 and e.response.status_code == 404:
                return None
            raise e

    def patch(self, url: str, json: dict):
        self.login()
        resp = self._client.patch(url, json=json)
        return _parse_resp(resp)

    def delete(self, url: str, raise_on_404: bool = False):
        self.login()
        try:
            return self._client.delete(url)
        except httpx.HTTPStatusError as e:
            if not raise_on_404 and e.response.status_code == 404:
                return None
            raise e

    def put(self, url: str, json: dict):
        self.login()
        resp = self._client.put(url, json=json)
        return _parse_resp(resp)

    def close(self):
        self._client.close()

    def dump_response(self, response: HTTPResponse):
        log.info("response text: " + response.text())
