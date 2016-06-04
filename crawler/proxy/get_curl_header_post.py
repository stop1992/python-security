#!/usr/bin/env python
# encoding: utf-8

def get_curl_header_post(curl_header_post):

    # strip "curl" and "--compressed"
    curl_header_post = curl_header_post[5:-12]
    curl_data = ''
    curl_post_data = ''

    if '--data' in curl_header_post:
        post_headers = curl_header_post.split('--data')
        curl_data = post_headers[0].split('-H')
        curl_post_data = post_headers[1].strip(' \'').split('&')
    else:
        curl_data = curl_header_post.split('-H')

    # delete url
    curl_data = curl_data[1:]

    headers = dict()
    for header in curl_data:

        split_header = header.strip(' \'').split(': ')
        header_key = split_header[0]
        header_word = split_header[1].strip()
        headers[header_key] = header_word


    post_datas = dict()
    for post_data in curl_post_data:
        cut_post_data = post_data.split('=')
        post_key = cut_post_data[0]
        post_word = cut_post_data[1]
        post_datas[post_key] = post_word

    return headers, post_datas
