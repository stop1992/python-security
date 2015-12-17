# encoding:utf-8


import os
from multiprocessing import Pool, Queue, Process

# from file_lock import FileLock

# queue = Queue()

# fp = open('test.txt', 'w')
# flock = FileLock(fp)


# def handle(slogan, queue):
def handle(queue):

    # print 'test'

    # for i in xrange(1000000):
    for i in xrange(1000000):
        queue.put('test')
        # queue.put(slogan)
    print 'put done'


def main():

    queue = Queue()

    p1 = Process(target=handle, args=(queue,))
    p2 = Process(target=handle, args=(queue,))
    p1.start()
    p2.start()

    print 'before: ' , queue.qsize()

    while queue.qsize() > 0:
        queue.get()

    print 'after: ', queue.qsize()

    p1.join(timeout=5)
    p2.join(timeout=4)
    print 'all done...'

    print queue.qsize()
    print 'done'

def test():

    pools = Pool(2)
    for i in xrange(3):
        # pools.apply_async(handle, args=(str(i)*5+'\n', queue))
        result = pools.apply_async(handle, args=(queue,))

    pools.close()
    pools.join()

    print 'all put done'

    print queue.qsize()

    # fp = open('text.txt', 'w')
    # while queue.qsize() > 0:
        # fp.write(queue.get())
    # fp.close()


if __name__ == '__main__':
    os.system('clear')

    main()
