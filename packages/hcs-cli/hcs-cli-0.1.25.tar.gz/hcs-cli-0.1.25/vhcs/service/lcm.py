import time
from ._util import hdc_service_client

_client = hdc_service_client("lcm")


class template:
    @staticmethod
    def get(id: str):
        return _client.get(f"/v1/templates/{id}")

    @staticmethod
    def list(type: str = None, name: str = None):
        base = "/v1/templates?size=200"
        if type:
            base += "&type=" + type
        pageIndex = 0
        ret = []

        def filter_fn(t):
            if name:
                return t.name.find(name) >= 0
            return True

        while True:
            url = base + "&page=" + str(pageIndex)
            page = _client.get(url)
            if not page.content:
                break
            ret.append(list(filter(filter_fn, page.content)))
            pageIndex += 1
        return ret

    @staticmethod
    def delete(force: bool):
        return _client.delete(f"/v1/templates/{id}?force={force}")

    @staticmethod
    def create(payload: str, type: str):
        url = "/v1/templates"
        if type:
            url += "/" + type

        return _client.post(url, payload)

    @staticmethod
    def wait(
        id: str,
        expected_status: list,
        timeout_seconds: int,
        exclude_status: list = ["ERROR"],
        interval_seconds: int = 10,
    ):
        start = int(time.time())
        while True:
            t = template.get(id)
            if not t:
                msg = f"Error waiting for template {id}. Not found."
                raise Exception(msg)

            status = t.status

            if status in expected_status:
                return t

            if status in exclude_status:
                msg = f"Error waiting for template {id}. Current status is {status}, which is not expected."
                raise Exception(msg)

            now = int(time.time())
            elapsed = now - start

            if elapsed > timeout_seconds:
                msg = f"Timeout waiting for template {id}. Current: {status}, expect: {expected_status}"
                raise Exception(msg)

            delay = min(interval_seconds, timeout_seconds - elapsed)
            time.sleep(delay)

            print(f"Waiting for template {id}. Expected={exclude_status}, current={status}...")


class provider:
    @staticmethod
    def get(id: str):
        return _client.get(f"/v1/providers/{id}")

    @staticmethod
    def list():
        return _client.get("/v1/providers")

    @staticmethod
    def delete():
        return _client.delete(f"/v1/providers/{id}")


def test():
    print("test")
