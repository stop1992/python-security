#encoding:utf-8

import random
from lib.core.data import paths

def randomUserAgents():
    user_f = paths.USER_AGENTS
    useragents = open(user_f, 'r').readlines()
    useragents_len = len(useragents)
    return useragents[random.randrange(useragents_len)].strip()
