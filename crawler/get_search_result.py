# encoding:utf-8

import requests
import os
import re
from bs4 import BeautifulSoup


class Search(object):
    def __init__(self):
        self.fp = open('result.txt', 'w')

    def get_html(self):
        self.fp.close()
        init_url = 'http://bioinformatics.cau.edu.cn/cgi-bin/PMRD/further/result1.cgi?txtmiR_name=&speciesA=All+species&miRNA=all_stem_loop&page='
        for i in xrange(1, 110):
            url = init_url + str(i)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            result = soup.find_all("td", align="center")
            print 'handling ', i, ' pages'
            self.handle(result)

    def handle(self, result):
        result_len = len(result) - 1
        pos = 4
        self.fp = open('result.txt', 'a+')
        for i in xrange(0, result_len/6):
            if result[pos].string.strip() == 'experimental':
                self.fp.write(result[pos-2].string + '\n')
                self.fp.write(result[pos-1].string + '\n')
            pos += 6
        self.fp.close()

def main():
    search = Search()
    search.get_html()

if __name__ == '__main__':
    os.system('clear')

    main()
