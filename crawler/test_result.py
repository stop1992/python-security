# encoding:utf-8

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.coros import BoundedSemaphore
import codecs
import requests

sem = BoundedSemaphore()

class TestResult(object):

    def __init__ (self):

        codecs.open('200.txt', 'w', 'utf-8')

    def test_visit(self, file_name):

        pools = Pool(20)
        pools.map(self.handle, codecs.open(file_name, 'r', 'utf-8'))


    def handle(self, url):
        try:
            url = url.strip()
            response = requests.get(url, timeout=5)
            sem.acquire()
            fp = codecs.open('200.txt', 'a+', 'utf-8')
            if response.status_code == '200':
                print url, 200
                fp.write(url)
            else:
                print url, response.status_code
            fp.close()
            sem.release()
        except Exception, e:
            print e
            print 'error url:', url


def main():

    result = TestResult()
    result.test_visit('google_results.txt')

if __name__ == '__main__':

    main()
