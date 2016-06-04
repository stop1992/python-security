#!/usr/bin/env python
# encoding: utf-8

import os
import requests
import subprocess

class Zoomeye(object):

    def __init__(self):
        pass


    def get_access_token(self):
        # command = "curl -X POST http://api.zoomeye.org/user/login -d '{ \"username\": \"testmai1@sina.com\", \"password\": \"testmai1\" }'"
        url = "http://api.zoomeye.org/user/login"
        para = '{ "username": "testmai1@sina.com", "password": "testmai1" }'
        access_token = subprocess.Popen(['curl', '-X', 'POST', url, '-d', para], stdout=subprocess.PIPE)
        print access_token


def main():

    zoomeye = Zoomeye()
    zoomeye.get_access_token()

if __name__ == '__main__':
    os.system('clear')

    main()

