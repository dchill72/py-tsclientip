import winrm
import netifaces
import sys


def get_ip():
    # making assumption that utun1 is the vpn interface
    # todo: validate this assumption?
    if 'utun1' in netifaces.interfaces():
        return netifaces.ifaddresses('utun1')[netifaces.AF_INET][0]['addr']

    # the primary gateway provides the default interface name for this machine
    primaryInteface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    ip_address = netifaces.ifaddresses(primaryInteface)[netifaces.AF_INET][0]['addr']
    print primaryInteface + ' IP: ' + ip_address
    return ip_address


def main():
    ts_server = sys.argv[1]
    ts_admin = sys.argv[2]
    ts_pwd = sys.argv[3]
    ts_plugin = sys.argv[4]

    ip_address = get_ip()

    # this string format is the most brittle part of the script, changing it
    # can easily break the remote call for no apparent reason
    script_text = "$ip_address = '" + ip_address + """'\n$path = 'C:\\Program Files\\Tanium\\Tanium Module Server\\plugins\\content\\""" + ts_plugin + """\\invoker.js'
$hostname = "hostname: '"
$port = "port: "

$text = Get-Content $path
$text -replace ("(?<=$hostname)" + "(.*?)(?=\')"), $ip_address | Set-Content $path
$text = Get-Content $path
$text -replace ("(?<=$port)" + "(.*?)(?=,)"), "17456" | Set-Content $path
Write-Host 'Done'"""

    print 'Remote Script:'
    print '--------------------------------------------------------------------------------------------'
    print script_text
    print '--------------------------------------------------------------------------------------------'
    s = winrm.Session(ts_server, auth=(ts_admin, ts_pwd))
    print 'Running script'
    r = s.run_ps(script_text)
    print 'Script complete'

    print 'StdOut From Remote: ' + r.std_out


if __name__ == "__main__":
    main()
