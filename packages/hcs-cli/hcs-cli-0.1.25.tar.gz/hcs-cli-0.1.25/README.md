# hcs-cli

The hcs-cli is a CLI for Horizon Cloud Service, with the following considerations:
* Provides user-task oriented CLI, not API-CLI.
* Support multiple profiles.
* Based on [Context Programming](https://github.com/nanw1103/context-programming)

Confluence: https://confluence.eng.vmware.com/display/HCS/HCS+CLI

## Getting started
```
pip3 install hcs-cli
```

or if you already have hcs-cli installed, use the follow command to upgrade it:
```
hcs upgrade
```

Create a default profile:
```
hcs profile init
```


## Choose profile
List existing profiles
```
hcs profile list
```
Get details of a profile
```
hcs profile get <name>
```

Switch to a profile
```
hcs profile use <name>
```

You may directly edit a profile. The following command shows the profile file path:
```
hcs profile file <name>
```
### Auth related commands

Get the auth token that can be used as the bearer token for REST API call.
```
hcs auth
```

Get details of the configured auth token, e.g. permissions & orgs
```
hcs auth --details
```

### Examples

Each service has its own sub-command. Take PKI service as example, to request a resource certificate:
```
./bin/hcs pki sign-resource-cert my-res1
```
