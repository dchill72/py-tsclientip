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

    ip_address = getMyIp()

    script_text = "$ip_address = '" + ip_address + """'\n$path = @'C:\\Program Files\\Tanium\\Tanium Module Server\\
    plugins\\content\\integrity-monitor-scheduledtask\\invoker.js'@
$hostname = "hostname: '"
$port = "port: "

$text1 = Get-Content $path
$text1 -replace ("(?<=$hostname)" + "(.*?)(?=\')"), "$ip_address" | Set-Content $path
$text2 = Get-Content $path
$text2 -replace ("(?<=$port)" + "(.*?)(?=,)"), "17456" | Set-Content $path
Write-Host "Done"
Exit"""

    print(script_text)
    s = winrm.Session(ts_server, auth=(ts_admin, ts_pwd))
    print("Running script")
    r = s.run_ps(script_text)
    print("Script complete")

    print(r.status_code)
    print(r.std_out)


if __name__ == "__main__":
    main()
