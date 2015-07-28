# encoding:utf-8

import os
import time
import Queue

COUNT_PATH = 0

class LM_RNA(object):

    def get_data(self):
        lncfile = open('tmp_lncrna.txt', 'r')
        lncdata = lncfile.readlines()
        lnclen = len(lncdata)
        self.lncrna = ''
        for i in xrange(1, lnclen):
                self.lncrna += lncdata[i].strip().upper().replace('T', 'U')
        # print len(lncrna)
        lncfile.close()
        # print lncrna

        mfile = open('mrna.txt', 'r')
        mdata = mfile.readlines()
        self.mrna = mdata[0].strip().upper().replace('T', 'U')
        self.mrna_structure = mdata[1].strip()
        # print self.mrna
        mfile.close()

    def write_matrix_file(self):
        # positive sequence
        columns = len(self.lncrna)
        rows = len(self.mrna)
        # matrix_match value is matching or not, if match, then is true, not is false
        self.matrix_match = [[False] * columns for i in xrange(rows)]
        # matrix_match_value value is match value A:U, GU are 2, G:C is 3
        # self.matrix_match_value = [([0] * columns) for i in xrange(rows)]

        # match dictionarys
        match = {138, 150, 156} #GC=138 AU=150 GU=156

        # if match, write 1, or not write 0
        # fp_match = open('match.txt', 'w')
        # if mathc, value write 3(GC), or not write 2
        fp_match_value = open('match_value.txt', 'w')

        for i in xrange(rows):
            for j in xrange(columns):
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

    def get_result(self):

        mrna_len = len(self.mrna)
        lncrna_len = len(self.lncrna)
        # record last character match or not
        # last_match = False
        # record current character match or not
        # current_match = False
        # pos_queue = Queue.Queue()
        # use this list to record match path
        pos_path = [[]] * (mrna_len + lncrna_len + 10)
        match_len = 0
        jump_count = 0
        for i in xrange(mrna_len-6):
            for j in xrange(lncrna_len-6):
                if self.matrix_match[i][j] == True:
                    match_len += 1
                    pos_path[match_len] = [i, j]
                    # self.matrix_match[i][j] = False
                    # count jump postions
                    jump_count = 0
                    self.handle(pos_path, match_len, jump_count, i+1, j+1)
                else:
                    self.handle(pos_path, match_len, jump_count, i, j)

    # def handle(self, pos_path, match_len, jump_count, row, column):

    def handle(self, pos_path, match_len, jump_count, row, column):
        # need to handle 4*4 grid
        for i in xrange(0, 4):
            for j in xrange(0, 4):
                if self.matrix_match[row+i][column+j] == True:
                    match_len += 1
                    pos_path[match_len] = [row+i, column+j]
                    # self.matrix_match[row+i][column+j] = False
                    # if match, then jump count is 0
                    if jump_count > 3 and match_len >= 7:
                        # one path is over
                        global COUNT_PATH
                        COUNT_PATH += 1
                        # print 'i: ', i, 'j: ', j
                        # print 'row: ', row, 'column: ', column
                        print 'PATH: ',  COUNT_PATH
                        for k in xrange(1, match_len+1):
                            print pos_path[k], ' ',
                        print '\n'
                        raw_input('please enter')
                        jump_count = 0

                    self.handle(pos_path, match_len, jump_count, row+i+1, column+j+1)
                else:
                    jump_count += 1
                    self.handle(pos_path, match_len, jump_count, row+i, column+j)

#    def write_matrix2file(self):
#        # positive sequence
#        columns = len(self.lncrna)
#        rows = len(self.mrna)
#        # matrix_match value is matching or not, if match, then is true, not is false
#        # self.matrix_match = [([False] * columns) for i in xrange(rows)]
#        # matrix_match_value value is match value A:U, GU are 2, G:C is 3
#        # self.matrix_match_value = [([0] * columns) for i in xrange(rows)]
#
#        # match dictionarys
#        match = {138, 150, 156} #GC=138 AU=150 GU=156
#
#        # if match, write 1, or not write 0
#        fp_match = open('match.txt', 'w')
#        # if mathc, value write 3(GC), or not write 2
#        fp_match_value = open('match_value.txt', 'w')
#
#        for i in xrange(rows):
#            for j in xrange(columns):
#                tmp = ord(self.lncrna[j]) + ord(self.mrna[i])
#                if tmp in match:
#                    fp_match.write('1 ')
#                    if tmp == 138:
#                            fp_match_value.write('3 ')
#                    else:
#                            fp_match_value.write('2 ')
#                else: # not match
#                    fp_match.write('0 ')
#                    fp_match_value.write('0 ')
#            fp_match.write('\n')
#            fp_match_value.write('\n')
#        fp_match.close()
#        fp_match_value.close()
#
#    def get_result():
#
#        mrna_len = len(self.mrna)
#        for i in xrange(mrna_len):
#            # count match base length
#            match_len = 0
#            crack = 0
#            for line in open('match.txt', 'r'):
#                line = line.strip()
#                line_data = line.split()
#                line_len = len(line_data)
#
#                # 'first' line needs find which base is matching
#                if match_len = 0:
#                    line_lne -= 6 # last 6 is not enough long to 7
#                    for i in xrange(line_len)):
#                        if line_data[i] == '1':
#                            match_len = 1
#                            # record current column to next use
#                            column = i
#                else:
#                    if column+1 < line_len and line_data[column+1] == '1':
#                        match_len += 1
#                    else:
#                        crack += 1
#                        if crack
#

if __name__ == '__main__':
    os.system('printf "\033c"')

    start = time.time()
    lmrna = LM_RNA()
    lmrna.get_data()
    lmrna.write_matrix_file()
    lmrna.get_result()
    end = time.time()
    print '\n\n--------------------------------------------'
    print COUNT_PATH
    print 'used time: ', end-start
    print '----------------------------------------------'
