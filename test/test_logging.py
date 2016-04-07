# encoding:utf-8


import logging
import os


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log.txt',
                    filemode='w')

# print log info to stream
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s:%(levelname)-8s%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def test():

    logging.debug('this is a debug')
    logging.info('this is a info')
    logging.warning('this is a warning')


def main():

    test()

    # for i in open('log.txt', 'r'):
        # print i

if __name__ == '__main__':

    os.system('clear')

    main()
