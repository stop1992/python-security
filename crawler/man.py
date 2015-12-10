# encoding:utf-8

from selenium import webdriver
import os

class Man(object):

    def __init__(self):

        self.url ='http://www.genecards.org/cgi-bin/carddisp.pl?gene=%s'
        # self.loc_url = 'http://www.genecards.org/cgi-bin/carddisp.pl?gene=%s#localization'

    def get_gene_name(self):

        self.gene_names = map(self.ch_strip, open('geneName.txt', 'r').readlines())

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

        print 'entrez_element: ', entrez_element
        print '#' * 20
        print 'gene_element: ', gene_element
        print '#' * 20
        print 'uniprot_element: ', uniprot_element
        print '#' * 50


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
            # if 'extracellular' in goterm:
            goid = self.driver.find_element_by_xpath('//*[@id="_localization"]/div[3]/div[2]/div/table/tbody/tr[1]/td[1]/a').text
            # else:
                # goterm = 'empty'
        except Exception, e:
            pass
            # print e
        print compartment, confidence, goid, goterm, new_gene


    def handle(self):

        # use http proxy
        service_args = [
            '--proxy=139.196.108.68:80'
            '--proxy-type=http'
            ]

        self.driver = webdriver.PhantomJS(service_args=service_args)

        self.get_gene_name()
        for gene in self.gene_names:
            print '-' * 100
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
            raw_input('stop here.....')

        self.driver.quit()

def main():

    man = Man()
    man.handle()


if __name__ == '__main__':
    os.system('clear')

    main()
