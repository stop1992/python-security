# encoding:utf-8

from selenium import webdriver
import os
import threading
# import Queue
from multiprocessing import Queue, Pool
import time


MAX_THREADS = 20
# OUTPUT_QUEUE = Queue.Queue()  # store gene names
# INPUT_QUEUE = Queue.Queue()  # store html data
INPUT_QUEUE = Queue()  # store html data

complete = Queue()
result1 = Queue()
result2 = Queue()

NUMS = 4

class WorkManager(object):
    def __init__(self, thread_pool_size=1):
        self.thread_pool = [] # initiate, no have a thread
        self.thread_pool_size = thread_pool_size
        self.__init_thread_pool()

    def __init_thread_pool(self):
        for i in xrange(self.thread_pool_size):
            self.thread_pool.append(WorkThread())

    def finish_all_threads(self):
        for i in xrange(self.thread_pool_size):
            self.thread_pool[i].join()


class WorkThread(threading.Thread):
    def __init__(self):

        threading.Thread.__init__(self)
        self.man = Man()
        self.start()

    def run(self):
        while True:
            try:
                self.man.handle(INPUT_QUEUE.get())
                if INPUT_QUEUE.empty():
                    self.man.driver.quit()
                    break
            except Exception, e:
                print e
                continue

def get_gene_name():

    for gene in open('geneName.txt', 'r'):
        INPUT_QUEUE.put(gene.strip())


class Man(object):

    def __init__(self):

        self.url ='http://www.genecards.org/cgi-bin/carddisp.pl?gene=%s'


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
                # print e

        if 'GeneCards Summary for' in source_code:
            try:
                if entrez_element != 'empty':
                    gene_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[2]/p').text
                else:
                    gene_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[1]/p').text
            except Exception, e:
                pass
                # print e

        if 'UniProtKB/Swiss-Prot for' in source_code:
                if entrez_element != 'empty' and gene_element != 'empty':
                    try:
                        uniprot_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[3]/ul/li/p').text
                    except Exception,e:
                        pass
                        # print e
                elif entrez_element == 'empty' and gene_element == 'empty':
                    try:
                        uniprot_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[1]/ul/li/p').text
                    except Exception, e:
                        pass
                        # print e
                else:
                    try:
                        uniprot_element = self.driver.find_element_by_xpath('//*[@id="_summaries"]/div[2]/ul/li/p').text
                    except Exception, e:
                        pass
                        # print e

        # print 'entrez_element: ', entrez_element
        # print '#' * 20
        # print 'gene_element: ', gene_element
        # print '#' * 20
        # print 'uniprot_element: ', uniprot_element
        # print '#' * 50
        result1.put(gene+'##'+entrez_element+'##'+gene_element+'##'+uniprot_element+'##'+new_gene+'\n')


    def get_localization(self, gene, new_gene):

        compartment = 'empty'
        confidence = 'empty'
        goid = 'empty'
        goterm = 'empty'

        try:
            compartment = self.driver.find_element_by_xpath('//*[@id="compartmentsTable"]/tbody/tr[1]/td[1]').text
            # if compartment == 'extracellular':
            confidence = self.driver.find_element_by_xpath('//*[@id="compartmentsTable"]/tbody/tr[1]/td[2]').text
            # else:
                # compartment = 'empty'
        except Exception, e:
            pass
            # print e

        try:
            goterm = self.driver.find_element_by_xpath('//*[@id="_localization"]/div[3]/div[2]/div/table/tbody/tr[1]/td[2]').text
            goid = self.driver.find_element_by_xpath('//*[@id="_localization"]/div[3]/div[2]/div/table/tbody/tr[1]/td[1]/a').text
        except Exception, e:
            pass
            # print e
        # print compartment, confidence, goid, goterm, new_gene
        result2.put(gene+'##'+compartment+'##'+confidence+'##'+goid+'##'+new_gene+'\n')


    def handle(self, gene):

        # use http proxy
        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=http'
            ]

        # self.driver = webdriver.PhantomJS(service_args=service_args)
        self.driver = webdriver.PhantomJS()

        print 'handling %s ....' % gene

        url = self.url % gene

        self.driver.get(url)
        self.driver.refresh()

        sign = 'same'
        # new_gene = 'same'
        try:
            new_gene = self.driver.current_url.split('=')[1].strip()
        except Exception, e:
            print e
            print self.driver.current_url, gene, url
            print '---------------------'
        if new_gene == gene:
            sign = 'same'
        else:
            sign = 'diff'

        self.get_summaries(gene, sign)
        self.get_localization(gene, sign)

def start_threads(name):

    print name
    workmanager = WorkManager(10)
    workmanager.finish_all_threads()

    complete.put('DONE')



def check_pools_complete():

    while True:

        if complete.qsize() == NUMS:
            print 'complete.....'
            break
        else:
            time.sleep(5)
            # print 'not complete...'


def main():

    get_gene_name()
    pools = Pool(NUMS)
    for i in xrange(NUMS):
        pools.apply_async(start_threads, args=('prossing '+str(i), ))

    check_pools_complete()

    # pools.close()
    # pools.join()

if __name__ == '__main__':
    os.system('clear')

    main()
