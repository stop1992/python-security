# encoding:utf-8

import os
import time
import Queue
import sys
import copy

sys.setrecursionlimit(50000)

COUNT_PATH = 0
LAST_POS_PATH = []
COUNT_TIMES = 1

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

    def first_seven_match(self, i, j):
        first_seven_match_len = 0
        sign = False
        match_len = 0
        for k in xrange(6):
            if self.matrix_match[i][j] == True:
                self.pos_path[match_len] = [i, j]
                self.matrix_match[i][j] = False
                match_len += 1
                i += 1
                j += 1
            else:
                sign = True
                break
        if not sign:
            self.next_match(i, j, match_len)

    def next_match(self, i, j, match_len):
        if self.matrix_match[i][j] == True:
            self.matrix_match[i][j] = False
            self.pos_path[match_len] = [i, j]
            match_len += 1
            self.matrix_match[i][j] = False
            # count jump postions
            jump_count = 0
            tmp_i = i + 1
            tmp_j = j + 1
            # print 'before while: i, j: ', tmp_i, tmp_j
            while tmp_i < self.mrna_len and tmp_j < self.lncrna_len:
                if self.matrix_match[tmp_i][tmp_j] == True:
                    self.pos_path[match_len] = [tmp_i, tmp_j]
                    self.matrix_match[tmp_i][tmp_j] == False
                    match_len += 1
                    tmp_i += 1
                    tmp_j += 1
                else:
                    break
            # print 'after while: i, j: ', tmp_i, tmp_j
            self.handle(self.pos_path, match_len, jump_count, tmp_i, tmp_j)

    def get_result(self):
        # use this list to record match path
        fp = open('path.txt', 'w')
        fp.close()
        # first_seven = 0
        self.pos_path = [[]] * (self.mrna_len + self.lncrna_len + 10)
        for i in xrange(self.mrna_len-6):
            for j in xrange(self.lncrna_len-6):
                match_len = 0
                jump_count = 0
                if self.matrix_match[i][j] == True:
                    self.first_seven_match(i, j)
                    # pos_path[match_len] = [i, j]
                    # if first_seven >= 7:

    def handle(self, pos_path, match_len_in, jump_count, row, column):
        # need to handle 4*4 grid
        for i in xrange(row, row+4):
            for j in xrange(column, column+4):
                if i >= self.mrna_len or j >= self.lncrna_len:
                    break
                if i < self.mrna_len and j < self.lncrna_len and self.matrix_match[i][j] == True:
                    match_len = match_len_in
                    pos_path[match_len] = [i, j]
                    # print 'row, column: ', i, j
                    match_len += 1
                    self.matrix_match[i][j] = False

                    tmp_i = i + 1
                    tmp_j = j + 1
                    while tmp_i < self.mrna_len and tmp_j < self.lncrna_len:
                        if self.matrix_match[tmp_i][tmp_j] == True:
                            pos_path[match_len] = [tmp_i, tmp_j]
                            self.matrix_match[tmp_i][tmp_j] == False
                            match_len += 1
                            tmp_i += 1
                            tmp_j += 1
                        else:
                            break
                    self.handle(pos_path, match_len, jump_count, tmp_i, tmp_j)

                    # if match, then jump count is 0
                    if jump_count <= 3:
                        # if COUNT_TIMES == 1
                            # LAST_POS_PATH = copy.deepcopy(pos_path)
                        # else:
                            # if (len(LAST_POS_PATH) + 1) == len(pos_path):

                        global COUNT_PATH
                        COUNT_PATH += 1
                        # print 'i: ', i, 'j: ', j
                        # print 'row: ', row, 'column: ', column
                        fp = open('path.txt', 'a')
                        # print 'PATH: ',  COUNT_PATH
                        fp.write('PATH:' + str(COUNT_PATH) + '\n')
                        for k in xrange(match_len):
                            fp.write(str(pos_path[k]) + ' ')
                            # print pos_path[k], ' ',
                        fp.write('\n')
                        fp.close()
                        if COUNT_PATH == 100:
                            sys.exit()
                        # print '\n'
                        # raw_input('please enter')
                        jump_count = 0
                else:
                    jmp_count = max(i - row, j - column) + 1


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
