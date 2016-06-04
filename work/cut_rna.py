#!/usr/bin/env python
# encoding: utf-8

import os
import shutil


def cut_lncrna(f):

    fp = open(f, 'r')
    lnc_datas = fp.readlines()
    data_len = len(lnc_datas)

    dir_name = f.split('.')[0]

    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)

    for i in xrange(data_len):
        if '>' in lnc_datas[i]:
            lnc_name = lnc_datas[i].strip().split('>')[1]
            print lnc_name
            lnc_fp = open(dir_name + os.sep + lnc_name + '.fasta', 'w')
            lnc_fp.write(lnc_datas[i].strip()+'\n')
            lnc_fp.write(lnc_datas[i+1].strip()+'\n')



def main():

    files = ['ath_lncRNA.txt', 'zma_lncRNA.txt']
    for f in files:
        cut_lncrna(f)

if __name__ == '__main__':
    os.system('clear')

    main()

