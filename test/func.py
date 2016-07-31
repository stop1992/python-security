#!/usr/bin/env python
# encoding: utf-8

import requests

def get_url(url):
    response = requests.get(url)
    return response.url
