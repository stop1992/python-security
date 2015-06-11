#-*- encoding:utf-8 -*- 

import os
import requests 
import re
import codecs
from selenium import webdriver
import xlrd

def get_data_from_excel():
    data = xlrd.open_workbook('mRNAdata.xls')
    table = data.sheets()[0]
    col_values = table.col_values(7)
    return col_values


if __name__ == "__main__":
	os.system('printf "\033c"')

	genes_name = get_data_from_excel()
	genes_name.reverse()
	for i in xrange(11):
		genes_name.pop()

	base_url = 'http://www.ncbi.nlm.nih.gov/gene/?term='

	# if os.path.exists('result.txt'):
		# os.remove('result.txt')

	# genes_name = []
	# genes_name.append('CFH')

	# fp = open('result.txt', 'a')

	while len(genes_name) > 0:
		gene_name = genes_name.pop()
		print gene_name
		url = base_url + gene_name
		driver = webdriver.PhantomJS()
		driver.get(url)

		try:
			result_element = driver.find_element_by_xpath('//*[@id="padded_content"]/div[4]/div/h2')
		except:
			print 'no result' 
			# fp.write('no result' + '\n')
			continue

		line_numbers = 20
		if len(result_element.text) < 15:
			tmp_text = result_element.text.split()
			# print tmp_text[1]
			line_numbers = int(tmp_text[1])

		for line in xrange(line_numbers):
			line += 1
			xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[2]/em'
			exists_homo_sapiens = driver.find_element_by_xpath(xpath)

			if exists_homo_sapiens.text == 'Homo sapiens':
				xpath = '//*[@id="gene-tabular-docsum"]/div[2]/table/tbody/tr[' + str(line) + ']/td[1]/div[2]/a'
				get_gene_href = driver.find_element_by_xpath(xpath)
				
				url = get_gene_href.get_attribute('href')

				# before run get, just quit
				driver.quit()
				os.system('kill 2 `pgrep phantomjs`')

				driver = webdriver.PhantomJS()
				driver.get(url)

				try:
					gene_type = driver.find_element_by_xpath('//*[@id="summaryDl"]/dd[5]')
					exon_count = driver.find_element_by_xpath('//*[@id="padded_content"]/div[5]/div[2]/div[2]/div[2]/div/dl/dd')
				except:
					print '\n\nerror url:', driver.current_url, '\n\n\n'
					driver.quit()
					os.system('kill 2 `pgrep phantomjs`')
					break

				print 'gene_type: ', gene_type.text
				# fp.write('gene_type:' + gene_type.text + '\n')
				print 'exon_count: ', exon_count.text
				# fp.write('exon_count:' + gene_type.text + '\n')
				driver.quit()
				os.system('kill 2 `pgrep phantomjs`')
				break
	fp.close()
