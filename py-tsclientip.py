#!/usr/bin/python

import winrm
import netifaces
import sys


def getMyIp():
    if 'utun1' in netifaces.interfaces():
        return netifaces.ifaddresses('utun1')[netifaces.AF_INET][0]['addr']
    return netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']


def main():
    ts_server = sys.argv[1]
    ts_admin = sys.argv[2]
    ts_pwd = sys.argv[3]
    ts_plugin = sys.argv[4]

    ip_address = getMyIp()
#    plugins\\content\\""" + ts_plugin + """\\invoker.js'@
    script_text = "$ip_address = '" + ip_address + """'\n$path = 'C:\\Program Files\\Tanium\\Tanium Module Server\\plugins\\content\\""" + ts_plugin + """\\invoker.js'
$hostname = "hostname: '"
$port = "port: "

$text = Get-Content $path
$text -replace ("(?<=$hostname)" + "(.*?)(?=\')"), $ip_address | Set-Content $path
$text = Get-Content $path
$text -replace ("(?<=$port)" + "(.*?)(?=,)"), "17456" | Set-Content $path
Write-Host 'Done'"""

    print(script_text)
    s = winrm.Session(ts_server, auth=(ts_admin, ts_pwd))
    print("Running script")
    r = s.run_ps(script_text)
    print("Script complete")

    print 'Result: ' + r.std_out


if __name__ == "__main__":
    main()
