# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
import re
import requests
import sys
import random
import string
from PIL import Image
import pytesseract


def test_pytesseract():
    image = Image.open('a.jpg')
    code = pytesseract.image_to_string(image)
    print code

def test_lambda():
    rand_str = lambda length: ''.join(random.sample(string.letters, length))
    test_str = rand_str(100)
    print test_str

def char_replace():
    # a = "test a a "
    a = "String.fromCharCode(104, 116, 116,112,58,47,47,49,57,50,46,49,54,56,46,49,46,49,48,54,47,119,111,114,100,112,114,101,115,115,47,101,120,112,108,111,105,116,46,106,11"
    b = a.replace(" ", "")
    print b


def test_while():
    while a < 10:
        print 'this is ', a
        a += 1
    else:
        print 'this stops'

def get_formhash():
    url = 'http://www.binvul.org'
    response = requests.get(url)
    fp = codecs.open('content.txt', 'w', 'utf-8')
    fp.write(response.content)
    fp.close()

if __name__ == '__main__':
    os.system('printf "\033c"')

    get_formhash()
    # test_while()
    # test_pytesseract()
