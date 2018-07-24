# py-tsclientip

## Requirements

Install pywinrm:

`pip install pywinrm`

Install netifaces:

`pip install netifaces`

Ensure that your Tanium Server has winrm enabled: https://docs.microsoft.com/en-us/windows-server/administration/server-manager/configure-remote-management-in-server-manager

This script will attempt to determine if you're connected to VPN, and will use either `en0` or `utun1` as appropriate.

In your terminal run:

`python py-tsclientip.py 'server_ip_addresss_or_fqdn' 'administrator' 'password'`
