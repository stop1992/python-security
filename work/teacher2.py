# -*- encoding:utf-8 -*-

import os
import re
import xlrd
import xlwt
import types
import copy

CONTINUOUS_NUM = 15

class Handle(object):

    def get_mrna_data(self):
        mfile = open('NM_000927.txt', 'r')
        self.mrnafilename, self.fileext = os.path.splitext(mfile.name)
        mdata = mfile.readlines()
        self.mrna_seq = mdata[0].strip().upper().replace('T', 'U')
        self.mrna_len = len(self.mrna_seq)
        # self.mrna_structure = mdata[1].strip()
        # print self.mrna_seq
        mfile.close()


    def get_rnas_data(self):

        self.get_mrna_data()
        directory = './match_result'
        direct = os.listdir(directory)
        for name in direct:
            print '------------------------------------------------'
            print 'handling ', name, '.....'
            self.rna_name = name.split('_mrna')[0]
            data = xlrd.open_workbook(directory + '/' + name)
            self.data_sheets = data.sheets()
            self.handle_data()


    def handle_data(self):
        # handle every sheet
        sheet_nums = len(self.data_sheets)
        # count rna occur times
        self.mrna_count = [0] * self.mrna_len
        save_excel = xlwt.Workbook()
        for sheet in self.data_sheets:
            # get colums data, col = 1
            col_data = sheet.col_values(0)
            pattern = re.compile(r'mRNA: ' + self.rna_name + ': (\d+)~(\d+)')
            result = pattern.findall(str(col_data))
            for item in result:
                # if seq occurs, count plus 1
                for i in xrange(int(item[0]) - 1, int(item[1])):
                    self.mrna_count[i] += 1
            # store continuous sequence num
            self.continu_result = [0] * self.mrna_len
            start = 0
            end = 0
            # count every continuous sequence num
            continu_count = 0
            # count continus times
            continu_times = 0
            for i in xrange(self.mrna_len):
                if self.mrna_count[i] > CONTINUOUS_NUM:
                    continu_count += 1
                    if continu_count == 1:
                        start = i
                    if continu_count >= 7:
                        end = i
                else:
                    if continu_count >= 7:
                        # continu_times as continu_result
                        continu_times += 1
                        for j in xrange(start, end+1):
                            self.continu_result[j] = continu_times
                    continu_count = 0
                    start = 0
                    end = 0

            if continu_count >= 7:
                # continu_times as continu_result
                continu_times += 1
                for j in xrange(start, end+1):
                    self.continu_result[j] = continu_times
            continu_count = 0
            start = 0
            end = 0
            save_excel_sheet = save_excel.add_sheet(sheet.name, cell_overwrite_ok=True)
            max_count = -1
            min_count = 10000000
            a = [0] * 200000
            max_len_a = -1

            for i in xrange(self.mrna_len):
                # write sequence num to excel
                save_excel_sheet.write(i, 0, i)
                # write sequence char to excel
                save_excel_sheet.write(i, 1, self.mrna_seq[i])
                # write count to excel
                save_excel_sheet.write(i, 2, self.mrna_count[i])
                # get min and max
                if min_count > self.mrna_count[i]:
                    min_count = self.mrna_count[i]
                if max_count < self.mrna_count[i]:
                    max_count = self.mrna_count[i]
                a[self.mrna_count[i] / 100] += 1
                if self.mrna_count[i] / 100 > max_len_a:
                    max_len_a = self.mrna_count[i] / 100

                # write continuous times result
                save_excel_sheet.write(i, 3, self.continu_result[i])

            # print test result
            print 'min_count:', min_count
            print 'max_count:' , max_count
            start = 0
            end = 99
            for i in xrange(max_len_a + 1):
                print start, '-', end, ':', a[i]
                start += 100
                end += 100

            # write total continus times
            save_excel_sheet.write(self.mrna_len, 0, 'pieces:'+str(continu_times))
            tmp_count = 2
            # write total min and max
            save_excel_sheet.write(self.mrna_len + tmp_count, 0, 'min')
            save_excel_sheet.write(self.mrna_len + tmp_count, 1, min_count)
            tmp_count += 1
            save_excel_sheet.write(self.mrna_len + tmp_count, 0, 'max')
            save_excel_sheet.write(self.mrna_len + tmp_count, 1, max_count)
            tmp_count += 2

            start = 0
            end = 99
            for i in xrange(max_len_a + 1):
                save_excel_sheet.write(self.mrna_len + tmp_count, 0, str(start) + '-' + str(end))
                save_excel_sheet.write(self.mrna_len + tmp_count, 1, a[i])
                tmp_count += 1
                start += 100
                end += 100

        file_name = self.rna_name  + '_count.xls'
        save_excel.save(file_name)
        os.system('mv ' + file_name + ' ./count_result/')
        print 'handle', self.rna_name, 'successfullly....'

if __name__ == '__main__':
    os.system('printf "\033c"')
    os.system('rm -rf count_result')
    os.system('mkdir count_result')
    raw_input('initial successfullly...')

    handle = Handle()
    handle.get_rnas_data()
