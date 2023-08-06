import base64
from ._util import regional_service_client
from vhcs.common.ctxp import profile, panic
from vhcs.common.sglib import hcs_client

_region_name = None


def use_region(region_name: str):
    global _region_name
    _region_name = region_name


def _client():
    return regional_service_client(_region_name, "vmhub")


def request_otp(org_id: str, resource_name: str) -> str:
    mqtt_endpoint_request = {
        #'mqttEndpoint': '',
        "orgId": org_id,
        "vmId": resource_name,
    }
    ret = _client().post("/credentials/generate-otp", mqtt_endpoint_request)
    return ret


def redeem_otp(resource_name: str, otp: str, csr: str):
    base64_encoded_csr = base64.b64encode(csr.encode("ascii")).decode("ascii")

    credentials_request = {"vmId": resource_name, "otp": otp, "clientCsr": base64_encoded_csr}
    return _client().post("/credentials", credentials_request)


def test():
    print("TODO")
