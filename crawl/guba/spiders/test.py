
import os

def test():
    # for i in open('stocknum.txt', 'r'):
        # print i
    direc = 'stocknum_03'
    # print os.listdir('stocknum_03')
    print 'test'
    fp = open(direc + '\\' + 'stocknum_03_01.txt', 'r')
    fp = fp.readlines()
    print len(fp)
    # print fp.name
    for i in fp:
        print i
        raw_input('please enter ....')

def test2():
    os.system("cd /d c:\\Python27")
    print '#####################################'
    print os.getcwd()
    print os.system('dir')
    # for i in xrange(3):
        # os.system('start dir')

if __name__ == '__main__':
    # os.system('printf "\033c"')

    test2()
