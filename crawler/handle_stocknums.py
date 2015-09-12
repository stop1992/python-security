#!/usr/bin/env python
# encoding: utf-8

import os
import xlrd


class Intersection:

    def get_data(self, file_name):
        excel = xlrd.open_workbook(file_name)
        sheet = excel.sheets()[0]
        stocknums = set()
        for row_num in xrange(sheet.nrows):
            # print type(sheet.row_values(row_num))
            for stocknum in sheet.row_values(row_num):
                if stocknum:
                    stocknums.add(stocknum.split('.')[0])
        return stocknums


    def handle(self):
        big_stocknums = self.get_data('big.xls')
        small_stocknums = self.get_data('small.xls')
        print 'big:', len(big_stocknums)
        print 'small:', len(small_stocknums)
        for stocknum in big_stocknums:
            small_stocknums.add(stocknum)
        print 'small:', len(small_stocknums)
        fp = open('stocknums.txt', 'w')
        for stocknum in small_stocknums:
            fp.write(stocknum + '\n')
        fp.close()

def get_file_name_ext(pre_name, num):
    if len(num) == 1:
       num = '0' + num
    return  pre_name + '_' + num + '.txt'

def get_file_name(num):
    if len(num) == 1:
        num = '0' + num
    return  'stocknum_' + num + '.txt'


def cut_stock_num():
    os.system('rm -rf stocknums')
    os.system('mkdir stocknums')
    # print 'initial successfully....'

    i = 0
    file_nums = 1
    file_name = get_file_name(str(file_nums))
    fp = open(file_name, 'w')
    for stock_num in open('stocknums.txt', 'r'):
        i += 1
        fp.write(stock_num.strip() + '\n')
        if i % 100 == 0:
            fp.close()
            # print 'handle ', fp.name
            # raw_input('pleasee ....')
            os.system('mv ' + file_name + ' ./stocknums/')
            file_nums += 1
            file_name = get_file_name(str(file_nums))
            fp = open(file_name, 'w')
    os.system('mv ' + file_name + ' ./stocknums/')
    fp.close()

def cut_stock_num_ext():

    os.system('rm -rf stocknum')
    os.system('mkdir stocknum')
    directory = './stocknums/'
    for name in os.listdir(directory):
        # print 'handling ', name
        pre_name = name.split('.')[0]
        # print pre_name
        os.system('rm -rf ' + pre_name)
        os.system('mkdir ' + pre_name)
        i = 0
        file_nums = 1
        file_name = get_file_name_ext(pre_name, str(file_nums))
        # print file_name
        each_file_line = 5
        file_count = 100 / each_file_line + 1
        fp = open(file_name, 'w')
        for stock_num in open(directory + name, 'r'):
            i += 1
            fp.write(stock_num.strip() + '\n')
            if i % each_file_line == 0:
                fp.close()
                os.system('mv ' + file_name + ' ./' + pre_name + '/')
                file_nums += 1
                file_name = get_file_name_ext(pre_name, str(file_nums))
                if file_nums == file_count:
                    break
                fp = open(file_name, 'w')
        fp.close()
        tmp = os.listdir(pre_name)
        print 'file nums:', len(tmp), ' dir_name:', pre_name
        os.system('mv ' + pre_name + ' stocknum')


if __name__ == '__main__':
    os.system('printf "\033c"')
    # inter = Intersection()
    # inter.handle()
    cut_stock_num()
    cut_stock_num_ext()
