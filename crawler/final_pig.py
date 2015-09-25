#!/usr/bin/env python
# encoding: utf-8

import os
# import xlsxwriter
import xlrd
from pymongo import MongoClient
import Queue
import calendar
import xlsxwriter

class Final:

    def add_zero(self, num):
        if len(num) == 1:
            num = '0' + num
        return num

    def trans(self, year, month, day):
        return year + '-' + self.add_zero(month) + '-' + self.add_zero(day)

    def get_dates(self):
        dates = []
        years = [2013, 2014]
        for year in years:
            for month in xrange(1, 13):
                days = calendar.monthrange(year, month)[1]
                str_year = str(year)
                str_month = str(month)
                for day in xrange(1, days+1):
                    date = self.trans(str_year, str_month, str(day))
                    dates.append(date)
        return dates

    def prepare_file(self):
        line = 1
        for date in self.dates:
            self.post_sheet.write(line, 0, date)
            self.negative_sheet.write(line, 0, date)
            self.positive_sheet.write(line, 0, date)
            line += 1

    def prepare(self):
        host = '192.168.1.108'
        port = 27018
        client = MongoClient(host, port)
        self.db = client.guba
        lack_queue = Queue.Queue()

        self.post_workbook = xlsxwriter.Workbook('post.xlsx')
        self.post_sheet = self.post_workbook.add_worksheet('post')

        self.negative_workbook = xlsxwriter.Workbook('negative.xlsx')
        self.negative_sheet = self.negative_workbook.add_worksheet('negative')

        self.positive_workbook = xlsxwriter.Workbook('positive.xlsx')
        self.positive_sheet = self.positive_workbook.add_worksheet('positive')

        self.dates = self.get_dates()

        self.prepare_file()

    def write2file(self, line, row, data):
        self.post_sheet.write(line, row, data)
        self.positive_sheet.write(line, row, data)
        self.negative_sheet.write(line, row, data)

    def save_data(self):
        # self.post_workbook.save('post.xls')
        # self.negative_workbook.save('negative.xls')
        # self.positive_workbook.save('positive.xls')
        self.post_workbook.close()
        self.negative_workbook.close()
        self.positive_workbook.close()


    def handle(self):
        col_num = 1
        for stock_num in open('stocknums.txt', 'r'):
            stock_num = stock_num.strip()

            self.write2file(0, col_num, stock_num)

            stocknum = 'db' + stock_num
            collec = self.db[stocknum]
            # print '\n' + '#' * 90
            print '\nhandle', stock_num, col_num
            if collec.count() > 0:
                for day_data in collec.find():
                    ask_time = day_data['ask_time']
                    line_num = self.dates.index(ask_time)

                    post_times = day_data['post_times']
                    self.post_sheet.write(line_num+1, col_num, post_times)

                    key_words = day_data['key_words']
                    negative_value = 0
                    for i in xrange(1, 5710):
                        negative_value += key_words[i]
                    self.negative_sheet.write(line_num+1, col_num, str(negative_value))

                    positive_value = 0
                    for j in xrange(5710, len(key_words)):
                        positive_value += key_words[j]
                    self.positive_sheet.write(line_num+1, col_num, str(positive_value))
            col_num += 1
        self.save_data()
                # raw_input('please ....')


if __name__ == '__main__':
    os.system('printf "\033c"')
    os.system('rm -f post.xlsx')
    os.system('rm -f negative.xlsx')
    os.system('rm -f positive.xlsx')

    final = Final()
    final.prepare()
    final.handle()
