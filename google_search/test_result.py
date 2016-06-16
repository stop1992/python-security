# encoding:utf-8

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.coros import BoundedSemaphore
import codecs
import requests
from gevent.fileobject import FileObjectThread

sem = BoundedSemaphore(1)

class TestResult(object):

    def __init__ (self):

        codecs.open('200.txt', 'w', 'utf-8').close()


    def test_visit(self, file_name):

        pools = Pool(5)
        pools.map(self.handle, codecs.open(file_name, 'r', 'utf-8'))


    def handle(self, url):

        try:
            url = url.strip()
            response = requests.get(url, timeout=5, allow_redirects=False)

            fp = codecs.open('200.txt', 'a+', 'utf-8')
            f = FileObjectThread(fp, lock=True)
            if response.status_code == 200:
                print url + '  ---->success'
                f.write(url + '\n')
            else:
                print url, response.status_code
            f.close()

        except Exception, e:
            print 'error:', url


if __name__ == '__main__':

    test_result = TestResult()
    test_result.test_visit('google_results.txt')


