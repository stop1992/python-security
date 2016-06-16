#encoding:utf-8

import os


def test():

    a = 'sjflkjsdlfj%s'
    for i in xrange(10):
        print a % i


def main():

    test()

if __name__ == '__main__':

    os.system('clear')

    main()


