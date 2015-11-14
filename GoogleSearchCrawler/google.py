# encoding:utf-8


import os
from bs4 import BeautifulSoup
import re
import urllib
import urllib2
import requests


class Google():
    def __init__(self):
        self.base_url = "https://www.google.com.hk/search"
        self.raw_data = """GET /search?safe=strict&biw=1477&bih=782&q=intext:test&oq=intext:test&gs_l=serp.3...1025216.1028150.2.1034027.11.9.0.0.0.0.0.0..0.0....0...1c.1.64.serp..11.0.0.5h6vR50O-1I&bav=on.2,or.&bvm=bv.107406026,d.d24&fp=f21f2f8ad92d7e6d&tch=1&ech=1&psi=Cv1DVrb9K8fSUanGr9AN.1447296273010.5 HTTP/1.1
        Host: www.google.com.hk
        User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
        Accept-Encoding: gzip, deflate
        DNT: 1
        Referer: https://www.google.com.hk
        Cookie: PREF=ID=1111111111111111:FF=2:LD=zh-CN:TM=1447296224:LM=1447296226:V=1:S=uLNKRThUqHchrNDn; NID=73=jMOtb7xjRQcoMiiRvc0Lq5ZIH0Vog96gizIdv4idGBLqtxa08HC1ChbwLc22TMJ8F4HUm2jotYNMTJltMsV-YWm3uA4FLS1h0piuSTf7-oZKEdzzQigrT5COMdnIcwjHbzIi7pKwZiGGRw92WR6mSO0hEEOgZKcigFx20W2yoR0CCg_D545nEQVG
        Connection: keep-alive
        """

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)
        return domain

    #extract a url from a link
    def extract_url(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)
        return url

    def trans_data_headers(self):
        payload_headers = re.split('\n', self.raw_data)
        # datas = OrderedDict()
        datas = {}
        headers = {}
        for i in xrange(len(payload_headers)):
            if len(payload_headers[i]) > 4:
                if i == 0:
                    data_all = re.split('\?| ', payload_headers[i])[2].split('&')
                    for data in data_all:
                        data = data.split('=')
                        if len(data) == 2:
                            key = data[0]
                            value = data[1]
                            datas[key] = value
                else:
                    header = payload_headers[i].split(': ')
                    if len(header) == 2:
                        key = header[0].strip()
                        value = header[1].strip()
                        headers[key] = value
        return datas, headers

    def extract_search_results(self):
        # results = list()
        soup = BeautifulSoup(self.html, "html.parser")
        div = soup.find('div', id  = 'search')
        if (type(div) != types.NoneType):
            lis = div.findAll('li', {'class': 'g'})
            if(len(lis) > 0):
                for li in lis:
                    # result = SearchResult()
                    h3 = li.find('h3', {'class': 'r'})
                    if(type(h3) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = h3.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    url = self.extract_url(url)
                    if(cmp(url, '') == 0):
                        continue
                    title = link.renderContents()
                    # result.set_url(url)
                    # result.setTitle(title)
                    global count
                    count += 1
                    print count, url
                    global fp
                    fp.write(url+'\n')

                    span = li.find('span', {'class': 'st'})
                    if (type(span) != types.NoneType):
                        content = span.renderContents()
                        # result.setContent(content)
                    # results.append(result)
        raw_input('please enter .....')
        # return results

    def get_google_html(self):
        datas, headers = self.trans_data_headers()
        print datas, headers
        raw_input('enter ...')
        encode_datas = urllib.urlencode(datas)
        req = urllib2.Request(self.base_url, encode_datas, headers)
        response = urllib2.urlopen(req)
        self.html = response.read()

def main():
    google = Google()
    google.get_google_html()
    google.extract_search_results()

if __name__ == "__main__":
    os.system('clear')

    main()
