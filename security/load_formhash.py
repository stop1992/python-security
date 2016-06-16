# encoding:utf-8


import os
import requests

def load_formhash():
    url = "http://192.168.1.106/test/load_formhash.swf"
    response = requests.get(url)
    print response.content

if __name__ == '__main__':
    os.system('clear')

    load_formhash()
