# encoding:utf-8

import os
import time
import Queue
import sys
import copy
import xlwt
import xlsxwriter


COUNT_PATH = 0
LAST_POS_PATH = []
COUNT_TIMES = 1
WRITE_ROW_NUM = 1

class LM_RNA(object):

    def pre_ready(self, file_name):
        # print file_name
        # raw_input('please .....')
        if os.path.isfile('/home/xinali/python/work/' + file_name + '_mrna_match.xlsx'):
            print 'exsit file, deleting....'
            os.remove('/home/xinali/python/work/' + file_name + '_mrna_match.xlsx')
            print 'delete successfully'
        fp = open('tmp.txt', 'w')
        fp.close()

    def handle(self):

        directory =  'lncrna'
        files = os.listdir(directory)
        for i in files:
            global COUNT_PATH
            COUNT_PATH = 0
            print '\n############################################'
            print 'handling ', i
            f = os.path.join(directory, i)
            self.pre_ready(i.split('.')[0])
            self.get_data(f)
            self.write_matrix_file()
            self.get_result()
            print COUNT_PATH
            print 'handled',  i
            # raw_input('please ......')


    def get_data(self, lnc_files):

        # lncfile = open('NR_026902.txt', 'r')
        lncfile = open(lnc_files, 'r')
        self.lncfilename, self.fileext = os.path.splitext(lncfile.name)
        self.lncfilename = self.lncfilename.split('/')[1]
        # print self.lncfilename, self.fileext
        # raw_input('please .......')
        lncdata = lncfile.readlines()
        lnclen = len(lncdata)
        self.lncrna = ''
        for i in xrange(1, lnclen):
                self.lncrna += lncdata[i].strip().upper().replace('T', 'U')
        # print len(lncrna)
        lncfile.close()
        # print lncrna

        mfile = open('NM_000927.txt', 'r')
        self.mrnafilename, self.fileext = os.path.splitext(mfile.name)
        mdata = mfile.readlines()
        self.mrna = mdata[0].strip().upper().replace('T', 'U')
        self.mrna_structure = mdata[1].strip()
        # print self.mrna
        mfile.close()

    def write_matrix_file(self):
        # positive sequence
        self.mrna_len = len(self.mrna)
        self.lncrna_len = len(self.lncrna)
        # matrix_match value is matching or not, if match, then is true, not is false
        self.matrix_match = [[False] * self.lncrna_len for i in xrange(self.mrna_len)]
        # matrix_match_value value is match value A:U, GU are 2, G:C is 3
        # self.matrix_match_value = [([0] * columns) for i in xrange(rows)]

        # match dictionarys
        match = {138, 150, 156} #GC=138 AU=150 GU=156

        # if match, write 1, or not write 0
        # fp_match = open('match.txt', 'w')
        # if mathc, value write 3(GC), or not write 2
        fp_match_value = open('match_value.txt', 'w')

        for i in xrange(self.mrna_len):
            for j in xrange(self.lncrna_len):
                tmp = ord(self.lncrna[j]) + ord(self.mrna[i])
                if tmp in match:
                    self.matrix_match[i][j] = True
                    # fp_match.write('1 ')
                    if tmp == 138:
                            fp_match_value.write('3 ')
                    else:
                            fp_match_value.write('2 ')
                else: # not match
                    # fp_match.write('0 ')
                    # self.matrix_match = False
                    fp_match_value.write('0 ')
            # fp_match.write('\n')
            fp_match_value.write('\n')
        # fp_match.close()
        fp_match_value.close()

    def write_result2excel(self):
        # excel = xlwt.Workbook()
        excel = xlsxwriter.Workbook(self.lncfilename + '_mrna_match.xlsx')
        table = excel.add_worksheet(self.lncfilename + '_mrna_match')
        # excel.save('lnc_mrna_match.xlsx')
        j = 1
        for line in open('tmp.txt', 'r'):
            mrna_start, mrna_end, lncrna_start, lncrna_end = [int(i) for i in line.split(',')]
            # print mrna_start, mrna_end, lncrna_start, lncrna_end
            global WRITE_ROW_NUM
            # print WRITE_ROW_NUM
            # raw_input('please......')
            table.write(WRITE_ROW_NUM    , 0, 'mRNA: ' + self.lncfilename + ': ' + str(mrna_start) + '~' + str(mrna_end))
            table.write(WRITE_ROW_NUM + 1, 0, self.mrna[mrna_start:mrna_end+1])
            table.write(WRITE_ROW_NUM + 2, 0, 'lncRNA: '+self.mrnafilename+': '+ str(lncrna_start) +'~' + str(lncrna_end))
            table.write(WRITE_ROW_NUM + 3, 0, self.lncrna[lncrna_start:lncrna_end+1])
            table.write(WRITE_ROW_NUM + 4, 0, 'length: ' + str(mrna_end - mrna_start + 1))
            WRITE_ROW_NUM += 7
        excel.close()

    def write_result2txt(self, match_len):
        fp = open('tmp.txt', 'a')
        mrna_start = str(self.pos_path[0][0])
        mrna_end = str(self.pos_path[match_len-1][0])
        lnc_start = str(self.pos_path[0][1])
        lnc_end = str(self.pos_path[match_len-1][1])
        fp.write(mrna_start + ',' + mrna_end + ',' + lnc_start + ',' + lnc_end + '\n')
        fp.close()

    def get_continus_match(self, i, j):
        match_len = 0
        self.matrix_match[i][j] = False
        self.pos_path[match_len] = [i, j]
        match_len += 1
        # count jump postions
        tmp_i = i + 1
        tmp_j = j + 1
        while tmp_i < self.mrna_len and tmp_j < self.lncrna_len:
            if self.matrix_match[tmp_i][tmp_j] == True:
                self.pos_path[match_len] = [tmp_i, tmp_j]
                self.matrix_match[tmp_i][tmp_j] == False
                match_len += 1
                tmp_i += 1
                tmp_j += 1
            else:
                break
        if match_len >= 7:
            global COUNT_PATH
            COUNT_PATH += 1
            self.write_result2txt(match_len)

    def get_result(self):
        self.pos_path = [[]] * (self.mrna_len + self.lncrna_len + 10)
        for i in xrange(self.mrna_len-6):
            for j in xrange(self.lncrna_len-6):
                if self.matrix_match[i][j] == True:
                    self.get_continus_match(i, j)
        self.write_result2excel()

def main():

    start = time.time()

    lmrna = LM_RNA()
    lmrna.handle()

    end = time.time()
    print 'used time: ', (end - start) / 60, 's'

if __name__ == '__main__':
    os.system('printf "\033c"')

    main()
