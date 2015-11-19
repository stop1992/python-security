#!/bin/env/python

# Retrieve TOR exit node IPs

import mechanize
from datetime import datetime

currentdate = str(datetime.now().isoformat())
fname = currentdate +"TORnodes.txt"

br = mechanize.Browser()
br.addheaders=[('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36')]
br.set_handle_robots(False)
br.set_debug_http(True)
f= br.retrieve('http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv', fname)
print f," successfully retrieved."
