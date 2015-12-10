# encoding:utf-8

from selenium import webdriver
import os

import gevent
from gevent.queue import Queue
from gevent.pool import Pool
from gevent import monkey
monkey.patch_socket()
from gevent.coros import BoundedSemaphore


INPUT_QUEUE = []

open('result1.txt', 'w').close()
open('result2.txt', 'w').close()
fp1 = open('result1.txt', 'a+')
fp2 = open('result2.txt', 'a+')

def get_gene_name():

    for gene in open('geneName.txt', 'r'):
        INPUT_QUEUE.append(gene.strip())


class Man(object):

    def __init__(self):

        self.url ='http://www.genecards.org/cgi-bin/carddisp.pl?gene=%s'

    def ch_strip(self, ch):

        return ch.strip()


    def get_summaries(self, gene, new_gene):

        # initiate 3 elements
        entrez_element = 'empty'
        gene_element = 'empty'
        uniprot_element = 'empty'

        source_code = self.driver.page_source

        if 'Entrez Gene Summary for' in source_code:
            try:
                entrez_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[1]/ul/li/p').text
            except Exception, e:
                pass

        if 'GeneCards Summary for' in source_code:
            try:
                if entrez_element != 'empty':
                    gene_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[2]/p').text
                else:
                    gene_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[1]/p').text
            except Exception, e:
                pass

        if 'UniProtKB/Swiss-Prot for' in source_code:
                if entrez_element != 'empty' and gene_element != 'empty':
                    try:
                        uniprot_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[3]/ul/li/p').text.strip()
                    except Exception,e:
                        pass
                elif entrez_element == 'empty' and gene_element == 'empty':
                    try:
                        uniprot_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[1]/ul/li/p').text.strip()
                    except Exception, e:
                        pass
                else:
                    try:
                        uniprot_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[2]/ul/li/p').text.strip()
                    except Exception, e:
                        pass
        sem1.acquire()
        fp1.write(gene+'\t'+entrez_element+'\t'+gene_element+'\t'+uniprot_element+'\t'+new_gene+'\n')
        sem1.release()

        # print 'entrez_element: ', entrez_element
        # print '#' * 20
        # print 'gene_element: ', gene_element
        # print '#' * 20
        # print 'uniprot_element: ', uniprot_element
        # print '#' * 50


    def get_localization(self, gene, new_gene):

        compartment = 'empty'
        confidence = 'empty'
        goid = 'empty'
        goterm = 'empty'

        try:
            compartment = self.driver.find_element_by_xpath('//*[@id="compartmentsTable"]/tbody/tr[1]/td[1]').text.strip()
            confidence = self.driver.find_element_by_xpath('//*[@id="compartmentsTable"]/tbody/tr[1]/td[2]').text.strip()
        except Exception, e:
            pass

        try:
            goterm = self.driver.find_element_by_xpath('//*[@id="_localization"]/div[3]/div[2]/div/table/tbody/tr[1]/td[2]').text.strip()
            goid = self.driver.find_element_by_xpath('//*[@id="_localization"]/div[3]/div[2]/div/table/tbody/tr[1]/td[1]/a').text.strip()
        except Exception, e:
            pass
        sem2.acquire()
        fp2.write(gene+'\t'+compartment+'\t'+confidence+'\t'+goid+'\t'+goterm+'\t'+new_gene+'\n')
        sem2.release()
        # print compartment, confidence, goid, goterm, new_gene


    def handle(self, gene):

        # use http proxy
        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=http'
            ]

        self.driver = webdriver.PhantomJS(service_args=service_args)

        print 'handling %s ....' % gene

        self.driver.get(self.url % gene)
        self.driver.refresh()

        new_gene = self.driver.current_url.split('=')[1].strip()
        if new_gene == gene:
            new_gene = 'same'
        else:
            new_gene = 'diff'

        self.get_summaries(gene, new_gene)
        self.get_localization(gene, new_gene)


def start_gevent(i):

    man = Man()
    man.handle(i)
    man.driver.quit()

# as a semaphore
sem1 = BoundedSemaphore()
sem2 = BoundedSemaphore()

def main():

    get_gene_name()

    pools = Pool(20)
    pools.map(start_gevent, INPUT_QUEUE)


if __name__ == '__main__':
    os.system('clear')

    main()
