from ._util import hdc_service_client

_client = hdc_service_client("pki")


def test():
    print("TODO: test. Migrate that from pki-util here")


def get_org_cert(org_id: str):
    return _client.get(f"/certificate/v1/orgs/{org_id}")


def delete_org_cert(org_id: str):
    return _client.delete(f"/certificate/v1/orgs/{org_id}")


def sign_resource_cert(org_id: str, csr: str):
    headers = {"Content-Type": "text/plain"}
    return _client.post(f"/certificate/v1/orgs/{org_id}/resource?includeChain=true", text=csr, headers=headers)


def get_root_ca():
    return _client.get(f"/certificate/v1/root-ca")
