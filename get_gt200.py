# encoding:utf-8

import os
import re

class Dong(object):

    def __init__(self):
        pass

    def get_file(self):

        while True:

            file_name = raw_input('please enter the path of file: ')
            if os.path.isfile(file_name):
                self.fp = open(file_name, 'r')
                break


    def judge_brackets(self, line):

        if line[0] == '>':
            return True
        else:
            return False


    def handle_data(self):

        self.get_file()
        print self.fp.name

        # self.fp = open('ath.fas', 'r')
        all_data = self.fp.readlines()
        data_len = len(all_data)
        brackets_lines = []

        for i in xrange(data_len):
            if self.judge_brackets(all_data[i]):
                brackets_lines.append(i)

        brackets_lines_len = len(brackets_lines)
        brackets_lines.append(data_len)
        result_fp = open('result.fas', 'w')

        for i in xrange(brackets_lines_len):
            line_num = brackets_lines[i]

            try:
                title = all_data[line_num]
            except:
                print 'error line is ', line_num
            body = ''
            for j in xrange(line_num+1, brackets_lines[i+1]):
                try:
                    body += all_data[j]
                except:
                    print 'error line is ', j

            if len(body) > 200:
                result_fp.write(title)
                result_fp.write(body)
        result_fp.close()


def main():

    dong = Dong()
    dong.handle_data()

if __name__ == '__main__':
    os.system('clear')

    main()
