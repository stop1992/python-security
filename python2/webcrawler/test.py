#-*-coding:utf-8-*-
#!/usr/bin/env python

import urllib2
import os
#import cookielib
import urllib
#import re
#import types
#import time
import requests
import bs4
import codecs
import json
import chardet

import mythread


if __name__ == '__main__':
	os.system('printf "\033c"')

	data = {'username':'2014544007', 'password':'709860'}
	session = requests.Session()
	response = session.post('http://gim.jlu.edu.cn/check.jsp', data=data)
	score = session.get('http://gim.jlu.edu.cn/pyc/menu_stu.jsp?menu=xuanke_check')
	soup = bs4.BeautifulSoup(score.text)
	tables = soup.find_all('table')
	#print tables[7].tr.children
	#for i in tables[7].descendants:
		#print i
	#print type(tables[7].stripped_strings)
	rows = 0
	cols = 0
	max_len = 0
	out_format = {}
	tmp_list = []
	for i in tables[7].stripped_strings:
		cols += 1
		i.strip()
		tmp_list.append(i)
		if cols % 12 == 0:
			out_format[rows] = tmp_list
			tmp_list = []
			rows += 1
	rows_list = range(len(out_format))
	cols_list = range(len(out_format[0]) - 1)
	for i in rows_list:
		for j in cols_list:
			if j == 2:
				print '%s' % (out_format[i][j]) + ' ' * (15 - len(out_format[i][j]) + 30 - len(out_format[i][j])), type(out_format[i][j]),
			else:
				if j == 1:
					print '%s' % (out_format[i][j]),
				else:
					print '%s' % (out_format[i][j]),
		print '\n'

	#print len(tables[2].tr.contents)
	#fp = codecs.open('tables.txt', 'w', 'utf-8')
	#for i in range(len(tables)):
		#fp.write('table ' + str(i + 1) + '\n')
		#fp.write(tables[i].prettify() + '\n\n\n')
	#fp.write(tables[2].tr.contents[0].prettify()+'\n\n\n\n')
	#fp.write(tables[2].tr.contents[1].prettify())
	#print len(tables[2].tr.contents[1].prettify())
	#fp.close()
	#raw_input('press any key to continue....')
	#for i in range(len(tables)):
	#	if tables[i].has_attr('class'):
	#		first_line =  tables[i].tr.contents
	#line = []
	#for i in range(len(first_line)):
	#	line.append(first_line[i].string.strip() + ' ')
	#print ''.join(line)

	#if soup.table.has_attr('class') and soup.table['class'] == u'xy_tab_main':
		#print soup.table
	#response.encoding = 'utf-8'
	#print response.encoding
	#content = response.text
	#unicode(content, response.encoding)
	#print type(response.text)
	#print response.text
	#print response.content
	#unicode(response.text, response.encoding)
	#content.encode('utf-8')
	#print content


	#responseresponse.text
	#print response.content
	#print response.text
	#print response.status_code
	#print response.encode
	#threads = []
	#loops = [2, 3, 4]
	#loops_len = range(len(loops))
	#url = u'http://www.baidu.com'
	#for i in loops_len:
	#	tables_threads = mythread.MyThread(func=loop, args=(url,))
	#	threads.append(tables_threads)

	#for i in loops_len:
	#	threads[i].start()
	#for i in loops_len:
	#	threads[i].join()

	#pattern = re.findall(r'<a href="/p/3499327292" .*? class="j_th_tit">.*? </a>', '<a href="/p/3665325492" title="skdjhfk" target="_blank" class="j_th_tit">skdhjh</a>')
	#ch = ur'<a href="/p/\d+" title="[\u4e00-\u9fff\ufb00-\ufffd\s\S]+?" target="_blank" class="j_th_tit">[\u4e00-\u9fff\ufb00-\ufffd\s\S]+?</a>'
	#fp = open('onepiece.txt', 'r')
	#lines = fp.readlines()
	#print len(lines)
	#for i in range(len(lines)):
	#	result = re.search(ch, lines[i])
	#	if type(result) != types.NoneType:
	#		print result.group()
	#		raw_input('press any key to continue....')
	#pattern = re.findall(r'<a href=.*? class="j_th_tit">.*?</a>', '<a href="/p/3665325492" title="skdjhfk" target="_blank" class="j_th_tit">skdhjh</a>')
	#print pattern.group()
	#print pattern.group(1)
	#url = 'http://www.qiushibaike.com/hot/page/1'
	#headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
	#print 'entering req'
	#req = urllib2.Request(url, headers = headers)
	#print 'entering response'
	#response = urllib2.urlopen(req)
	#print 'entering content'
	#content = response.read()
	#print 'entered content'
	#print type(content)
	#old_url = 'http://rrurl.cn/b1UZuP'
	#old_url = 'http://www.baidu.com'
	#url = 'https://www.google.com/'
	#url = 'http://www.sina.com'
	#cookie = cookielib.CookieJar()
	#handler = urllib2.HTTPCookieProcessor(cookie)
	#opener = urllib2.build_opener(handler)
	#response = opener.open(url)
	#print type(cookie)
	#for item in cookie:
	#	print item.name, item.value
	#url = 'http://www.wangxi.com'
	#try:
	#	response = urllib2.urlopen(url)
	#except urllib2.HTTPError, e:
	#	print 'httperror'
	#	print e.message
	#	print e.code
	#except urllib2.URLError, e:
	#	#print 'urlerror'
	#	#print e.message
	#	print e
	#	if hasattr(e, 'code'):
	#		print e.code
	#else:
	#	print 'no wrongs'
	#print cookie.name
	#print cookie.value
	#response = urlopen(url)
	#print response.geturl()
	#req = Request(old_url)
	#response = urlopen(req)
	#print response.info()
	#print 'Old_url:', old_url
	#print 'Actual_url:', response.geturl()
