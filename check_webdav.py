import os
import requests
import nmap


class Webdav(object):

    def __init__(self):
        windows_hosts = []


    def check_webdav(self):

        headers = {
                'Host': 'www.beihua.edu.cn'
                }

        response = requests.options('http://www.beihua.edu.cn', headers=headers)
        print response.headers



    def nmap_scan(self):

        self.nm = nmap.PortScanner()
        print 'scaning...'
        self.nm.scan(hosts='192.168.1.105-107', arguments='-sS -O')

        for host in self.nm.all_hosts():
            if self.nm[host]['osmatch']:
                print host, self.nm[host]['osmatch'][0]['osclass'][0]['osfamily']



def main():

    webdav = Webdav()
    # webdav.nmap_scan()
    webdav.check_webdav()


if __name__ == '__main__':
    os.system('clear')

    main()
