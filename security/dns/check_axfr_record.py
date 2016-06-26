#!/usr/bin/env python
# encoding: utf-8

import os
import re
import subprocess


class Axfr(object):

    def __init__(self):
        pass

    def check_axfr_record(self):

        result_fp = open('axfr.txt', 'w')

        for site in open('top.txt', 'r'):
            # print 'handling %s', site.strip()
            nameservers = subprocess.Popen(['dig', 'ns', site.strip(), '+short'], stdout=subprocess.PIPE)

            for ns in nameservers.stdout.readlines():
                print ns.strip(), ' <=> ', site.strip()
                result_fp.write(ns.strip() + ' <=> ' + site.strip() + '\n')
                # raw_input('wait....')
                axfr_record = subprocess.Popen(['dig', '@'+ns.strip(), 'axfr', site.strip(), '+short'], stdout=subprocess.PIPE)
                for a in axfr_record.stdout.readlines():
                    print a
                    result_fp.write(a)

                result_fp.write('\n')

        result_fp.close()



def main():

    axfr = Axfr()
    axfr.check_axfr_record()


if __name__ == '__main__':
    os.system('clear')

    main()
