import click
import json
from vhcs.common.ctxp import config, profile, jsondot

_hcs_envs = config.get("hcs-deployments.yaml")


def _is_production_env(hdc_url: str) -> bool:
    for env in _hcs_envs["prod"]:
        if env.hdc.url == hdc_url:
            return True


def _get_csp_url(hdc_url: str) -> str:
    if _is_production_env(hdc_url):
        return "https://console.cloud.vmware.com"
    return "https://console-stg.cloud.vmware.com"


def _create_default_profiles(recreate_defaults: bool):
    _hcs_envs = config.get("hcs-deployments.yaml")

    items = []
    items += _hcs_envs["prod"]
    items += _hcs_envs["staging"]
    items += _hcs_envs["dev"]

    for i in items:
        name = i.alias or i.env

        if not recreate_defaults and profile.exists(name):
            continue

        doc = {
            "hcs": {"url": i.hdc.url, "regions": i.regions},
            "csp": {"url": _get_csp_url(i.hdc.url), "apiToken": "", "clientId": "", "clientKey": ""},
        }
        print("Creating default profile placeholder: " + name)
        profile.create(name, doc)


def _create_nightly_profile(recreate: bool):
    name = "nightly"
    if not recreate and profile.exists(name):
        return

    print("Creating default profile: " + name)
    data = profile.get("integration")
    copy = jsondot.parse(json.dumps(data))
    copy.csp.apiToken = ""
    copy.csp.clientId = ""
    copy.csp.clientKey = ""
    profile.create(name, copy)


def _copy_profile(name: str):
    data = profile.get(name)
    return jsondot.parse(json.dumps(data))


@click.command()
@click.argument("name", type=str, default="default", required=False)
@click.option("--recreate-defaults/--no-recreate-defaults", "-r", default=False)
@click.option(
    "--property",
    "-p",
    type=str,
    multiple=True,
    help="Specify additional properties, as key-value pair, e.g. 'o1.k1=v1'. Can be specified multiple times.",
)
def init(name: str, recreate_defaults: bool, property: list):
    """Init profile interactively"""

    _create_default_profiles(recreate_defaults)
    _create_nightly_profile(recreate_defaults)

    print()
    print("Preparing profile: " + name)
    doc = _copy_profile("nightly")

    hcs_url = doc.hcs.url
    doc.hcs.url = click.prompt("HCS URL", type=str, show_default=True, default=hcs_url)
    region_url = doc.hcs.regions[0].url
    region_url = click.prompt("HCS region URL", type=str, show_default=True, default=region_url)
    doc.hcs.regions[0].url = region_url
    doc.csp.url = _get_csp_url(doc.hcs.url)

    while True:
        default_val = doc.csp.apiToken or ""
        csp_api_token = click.prompt("CSP API Token", type=str, default=default_val, show_default=True)
        if csp_api_token:
            doc.csp.apiToken = csp_api_token
            break
        else:
            doc.csp.apiToken = ""

        default_val = doc.csp.clientId or ""
        csp_client_id = click.prompt("CSP client ID", type=str, default=default_val, show_default=True)
        if not csp_client_id:
            click.echo("To auth with CSP, either API token or client id/secret should be specified.")
            continue
        while True:
            default_val = doc.csp.clientKey or ""
            csp_client_key = click.prompt("CSP client key", type=str, default=default_val)
            if csp_client_key:
                doc.csp.clientId = csp_client_id
                doc.csp.clientKey = csp_client_key
                break
        break

    profile.create(name, doc)
    return profile.current()
