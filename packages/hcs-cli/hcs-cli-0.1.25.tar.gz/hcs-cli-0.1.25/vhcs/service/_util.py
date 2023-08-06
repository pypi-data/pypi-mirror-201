from vhcs.common.ctxp import profile, panic
from vhcs.common.sglib import hcs_client


def hdc_service_client(service_name: str):
    url = profile.current().hcs.url
    if not url.endswith("/"):
        url += "/"
    url += service_name
    return hcs_client(url)


def _get_region_url(region_name: str):
    regions = profile.current().hcs.regions
    if not region_name:
        return regions[0].url
    for r in regions:
        if r.name.lower() == region_name.lower():
            return r.url
    names = []
    for r in regions:
        names.append(r.name)
    panic(f"Region not found: {region_name}. Available regions: {names}")


def regional_service_client(region_name: str, service_name: str):
    #'https://dev1b-westus2-cp103a.azcp.horizon.vmware.com/vmhub'
    url = _get_region_url(region_name)
    if not url:
        panic("Missing profile property: hcs.regions")
    if not url.endswith("/"):
        url += "/"
    url += service_name
    return hcs_client(url)
