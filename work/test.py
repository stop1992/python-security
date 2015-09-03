# encoding:utf-8

import re
import requests
import os
import sys
import xlrd
import xlwt
import time
import Queue
import xlsxwriter

def test1():
    fp = open('data.txt', 'r')
    data = fp.readlines()
    pattern = re.compile(r'mRNA: NM_000927:  (\d+)~(\d+)')
    result = pattern.findall(str(data))
    print len(data)
    for item in result:
            print type(item)
            print item[0], item[1]
            raw_input('press any key')
    print len(result)

def test2():
    fp = open('mRNA.txt', 'r')
    line = fp.readline()
    print len(line)
    print line
    for i in xrange(len(line) - 1):
            if line[i]:
                    print '\n---------'
                    print i, line[i]
                    print '---------'
            else:
                    print 'this is null'
                    raw_input('press any key')

def test3():

    arra = ['A', 'U', 'C', 'G']
    arrb = ['A', 'U', 'C', 'G']
    arrc = ['AU', 'GC', 'GU', 'UA', 'CG', 'UG']
    arrd = ['AA', 'AC', 'AG', 'CA', 'CC', 'CU', 'GA', 'GG', 'UC', 'UU']
    resa = {}
    resb = {}

    for i in xrange(4):
            for j in xrange(4):
                    tmp = arra[i] + arrb[j]
                    if tmp in arrc:
                            resa[tmp] = ord(arra[i]) + ord(arrb[j])
                    else:
                            resb[tmp] = ord(arra[i]) + ord(arrb[j])
    print resa
    print resb

def test4():
    start = time.time()
    tmp = []
    fp = open('testt.txt', 'w')
    for i in xrange(1000000000):
            fp.write('test')
    fp.close()
    end = time.time()
    print 'time: ', end-start

def test5():

    fp = open('1.txt', 'w')
    for i in xrange(100):
        for j in xrange(100):
            # if j != 99:
            fp.write('a ')
            # else:
                # fp.write('a' + '\n')
        fp.write('\n')
    fp.close()

    for line in open('1.txt', 'r'):
        pass
        # print line,
        # raw_input('please enter')

    for line in open('1.txt', 'r'):
        line = line.strip()
        arr = line.split(' ')
        print arr
        print '-----------------------------------------------------'

def test6():
    l = [False] * 600000000

def test7():
    queue = Queue.Queue()
    a = [2, 3]
    c = [2, 3]
    d = [1, 2]
    e = [1, 2]
    queue.put(a)
    queue.put(c)
    queue.put(d)
    queue.put(e)

    print queue.qsize()
    for i in xrange(queue.qsize()):
        print queue.get()

def test7():
    a = [2, 3, 4, 5, 6]
    for i in xrange(len(a)):
        print a[i], ' ',


TEST = 1

class testclass(object):

    def one(self):
        global TEST
        TEST += 1
        print TEST

def test8():
    a = [[2, 3], [3, 4]]
    fp = open('test.txt', 'a')
    b = str(a)
    fp.write(b)
    fp.write('\n')
    fp.close()

def test9():

    for line in open('path.txt', 'r'):
        print line
        raw_input('please')

def test10():
    for i in xrange(100):
        if i == 50:
            sys.exit()
        else:
            print i, 'test.......'

def test11():

    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet('test')

    line = 0
    for i in xrange(1000, 100000):
        worksheet.write(line, 0, i)
        line += 1

    workbook.close()

if __name__ == '__main__':
    os.system('printf "\033c"')

    test11()
