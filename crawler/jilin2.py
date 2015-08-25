# -*-coding:utf-8-*-
#!/usr/bin/env python

import urllib2
import os
import urllib
import codecs
import json

import requests
import bs4

# import chardet
import mythread


# judge char is chinese or not
def is_chinese(unchar):
    if unchar >= u'\u4e00' and unchar <= u'\u9fa5':
        return True
    else:
        return False


#align output, if unichar is str ,then add space, else add chinese space
def align_out(unichar, length):
    if length == 0:
        return unichar
    slen = len(unichar)
    tmp_unichar = unichar
    if isinstance(unichar, str):
        placeholder = ' '
    else:
        placeholder = u'\u3000'
    while slen < length:
        tmp_unichar += placeholder
        slen += 1
    return tmp_unichar


if __name__ == '__main__':
    os.system('printf "\033c"')

    data = {'username': '2014544007', 'password': '709860'}
    session = requests.Session()
    response = session.post('http://gim.jlu.edu.cn/check.jsp', data=data)
    score = session.get('http://gim.jlu.edu.cn/pyc/menu_stu.jsp?menu=xuanke_check')
    soup = bs4.BeautifulSoup(score.text)
    tables = soup.find_all('table')
    rows = 0
    cols = 0
    max_len = 0
    # save strings in out_format, each line as a element in out_format
    out_format = {}
    # tmp_list to save each line, just tmp
    tmp_list = []

    # striped_strings can strip the space and blank line
    for i in tables[7].stripped_strings:
        cols += 1
        i.strip()
        tmp_list.append(i)
        if cols % 12 == 0:  # each line has 12 elements
            out_format[rows] = tmp_list
            tmp_list = []
            rows += 1
    rows_list = range(1, len(out_format))
    cols_list = range(len(out_format[0]) - 1)
    for i in rows_list:
        for j in cols_list:
            if j == 2:
                # count numbers and alphabet
                count_num_alphabet = 0
                for k in range(len(out_format[i][j])):
                    if not is_chinese(out_format[i][j][k]):
                        count_num_alphabet += 1
                # here, count_num_alphabet is odd, so count_num_alphabet - 1,
                # beause a str occupy a space, a chinese occupy two space
                print '%-s' % (align_out(out_format[i][j], 20) + ' ' * (count_num_alphabet - 1)),
            else:
                if j == 1:
                    print '%s' % (align_out(out_format[i][j], 8)),
                else:
                    if j == 3:  # difficult to handle, so ignore it
                        pass
                    else:
                        print '%5s' % (out_format[i][j]),
        print '\n'

