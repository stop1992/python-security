#!/usr/bin
# encoding:utf-8

import os
import subprocess
import re

def export_db():
    mongo_path=r'C:\"Program Files\MongoDB 2.6 Standard\bin"'
    os.system('printf "\033c"')
    os.system('color 02')
    tasklist = os.popen('tasklist')
    pattern = re.compile('mongod.exe')
    for f in tasklist:
        line = f.split()
        if len(line) > 0:
            if pattern.search(line[0]):
                print 'mongod is running, start exporting data.....'
                for stocknum in open('stocknum_04.txt', 'r'):
                    export_num = 0
                    # print 'export ', stocknum, 'successfully....'
                    # stocknum = '601901'
                    stocknum = stocknum.strip()
                    try:
                        os.system(mongo_path + r'\mongoexport.exe -d guba_data -c db' + stocknum + ' -o .\\db_04\\' + stocknum + '.dat')
                        export_num += 1
                    except Exception, e:
                        print str(e)
                        raw_input('please enter....')

    print 'export_num:', export_num
if __name__ == '__main__':
    export_db()
