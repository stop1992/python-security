#encoding:utf-8

import random

def randomuseragent(user_f):
    useragents = open(user_f, 'r').readlines()
    useragents_len = len(useragents)
    return useragents[random.randrange(useragents_len)].strip()


if __name__ == '__main__':
    print randomuseragent('/home/xinali/python/security/useragents.txt')
