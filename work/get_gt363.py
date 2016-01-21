# encoding:utf-8

import os
import re

class Dong(object):

    def __init__(self):
        pass

    def get_input_file(self):

        while True:

            file_name = raw_input('please enter the path of input file: ')
            if os.path.isfile(file_name):
                print '[*] get input file successfully...'
                self.fp = open(file_name, 'r')
                break
            else:
                print '[*] get input file fail...'

    def get_output_path(self):

        while True:

            self.output_path = raw_input('please enter output path:')
            if os.path.exists(self.output_path):
                print '[*] get output path successfully...'
                break
            else:
                print '[*] get output path fail....'


    def judge_brackets(self, line):

        if line[0] == '>':
            return True
        else:
            return False

    def judge_ORF_condition(self):

        all_ATG_index = []
        start = -1
        while True:
            try:
                ATG_index = self.body.index('ATG', start+1)
                all_ATG_index.append(ATG_index)
                start = ATG_index
            except ValueError:
                break

        for ATG_index in all_ATG_index:

            TAA_index = self.get_index('TAA', ATG_index)
            TAG_index = self.get_index('TAG', ATG_index)
            TGA_index = self.get_index('TGA', ATG_index)
            codon_length = max(TAA_index, TAA_index, TGA_index) - ATG_index + 1
            if codon_length >= 363 and (codon_length+1)%3!=0:
                return True
        return False

    def get_index(self, termination, start):

        try:
            tmp_index = 0
            tmp_index = self.body.index(termination, start)
        except ValueError:
            pass
        return tmp_index



    def handle_data(self):

        # self.get_input_file()
        # self.get_output_path()

        # output_file = self.output_path + 'result.fas'
        # result_fp = open(output_file, 'w')


        self.fp = open('result.fas', 'r')
        result_fp = open('final_result.fas', 'w')

        print '[*] handling all data of', self.fp.name

        all_data = self.fp.readlines()
        data_len = len(all_data)
        brackets_lines = []

        for i in xrange(data_len):
            if self.judge_brackets(all_data[i]):
                brackets_lines.append(i)

        brackets_lines_len = len(brackets_lines)
        brackets_lines.append(data_len)

        for i in xrange(brackets_lines_len):
            line_num = brackets_lines[i]

            try:
                title = all_data[line_num]
            except:
                print 'error line is ', line_num

            self.body = ''
            no_strip_body = ''

            for j in xrange(line_num+1, brackets_lines[i+1]):
                try:
                    self.body += all_data[j].strip()
                    no_strip_body += all_data[j]
                except:
                    print 'error line is ', j

            if len(self.body) >= 363 and 'ATG' in self.body:
                if self.judge_ORF_condition():
                    result_fp.write(title)
                    result_fp.write(no_strip_body)
        result_fp.close()
        print 'get successfully...'
        # print '[*] Save all result to %s successfully...' % (output_file)


def main():

    dong = Dong()
    dong.handle_data()

if __name__ == '__main__':
    os.system('color 02')

    main()
