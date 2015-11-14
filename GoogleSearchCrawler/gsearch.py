#!/usr/bin/python
#-*- coding: utf-8 -*-

# Create by Meibenjin.

import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import gzip, StringIO
import re, random, types

from bs4 import BeautifulSoup
import traceback

base_url = 'https://www.google.com.hk/search'
results_per_page = 10

user_agents = list()

count = 0
fp = open('urls.txt', 'w')

# results from the search engine
# basically include url, title,content
class SearchResult:
    def __init__(self):
        self.url= ''
        self.title = ''
        self.content = ''

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def printIt(self, prefix = ''):
        global count
        print count, 'url   ->', self.url
        # print 'title\t->', self.title
        # print 'content\t->', self.content
        print

    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url+ '\n')
            file.write('title:' + self.title + '\n')
            file.write('content:' + self.content + '\n\n')

        except IOError, e:
            print 'file error:', e
        finally:
            file.close()


class GoogleAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime =  random.randint(60, 120)
        time.sleep(sleeptime)

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    #extract a url from a link
    def extractUrl(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)

        return url

    # extract serach results list from downloaded html file
    def extractSearchResults(self, html):
        results = list()
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find('div', id  = 'search')
        # global count
        # count = 0
        if (type(div) != types.NoneType):
            lis = div.findAll('li', {'class': 'g'})
            if(len(lis) > 0):
                for li in lis:
                    result = SearchResult()
                    h3 = li.find('h3', {'class': 'r'})
                    if(type(h3) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = h3.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    url = self.extractUrl(url)
                    if(cmp(url, '') == 0):
                        continue
                    title = link.renderContents()
                    result.setURL(url)
                    result.setTitle(title)
                    global count
                    count += 1
                    print count, url
                    global fp
                    fp.write(url+'\n')

                    span = li.find('span', {'class': 'st'})
                    if (type(span) != types.NoneType):
                        content = span.renderContents()
                        result.setContent(content)
                    results.append(result)
        raw_input('please enter .....')
        return results

    # search web
    # @param query -> query key words
    # @param lang -> language of search results
    # @param num -> number of search results to return
    def search(self, query, lang='en', num=results_per_page):
        lang = 'zh-CN'
        search_results = list()
        query = urllib2.quote(query)
        if(num % results_per_page == 0):
            pages = num / results_per_page
        else:
            pages = num / results_per_page + 1

        for p in range(0, pages):
            start = p * results_per_page
            url = base_url + 'search'
            data = {
                    'hl': lang,
                    'num': results_per_page,
                    'start':start,
                    'q':query
                    }

            headers = {}
            retry = 3
            while(retry > 0):
                try:
                    request = urllib2.Request(url, data)
                    length = len(user_agents)
                    index = random.randint(0, length-1)
                    user_agent = user_agents[index]
                    cookie = "SID=DQAAAB8BAAD1O00o6GDD6T8fsDYO2_OTl3DMsvCz8-QlN9x5o2RDEq0mIY9jrC2A3DGbeski-q8Zz-ca7uokhDIL15vwdzF9Y2gOvX5zK8XrDUIhGRZ1QHKwSTE0cYRZ57Jm3gEbEKYVySlkrXOj4PWVVxt8GYKEIT7jJ6STrELI5MAOJLtqkUa0hhdWsqKSgWjL-TeNg4YeFRlwceiGjLmR463akCfgh6zqVtEWxYCBOq8oo8u0Vzp3YcxxF6kO_oFu3qf0h67KhczztY1K-sVQM7CNlpnaCHxT1Xv21glaqZjWjnp6TVTgjPkn621mvMN5ijfuNQGydcF3LKdPoprvCpSIvjPZPO79wIzc-qFAgDh_uY2iDxJnYhTJV8RCT2P_isR5q0k; HSID=Ag80cQUm_5uzpiDcH; SSID=AeYKuz1WS0svu2EKz; APISID=eKUWNAnn4tngnK-m/AO5R0Sbi-sIonU8zb; SAPISID=dT8cftk4PiFNN7Ec/An6G2qV1kN6-pQ79G; NID=73=EY9SPKP0Bipx5G0lplykfinocyJ5yA6EDd0je5WjGzIE2GZ5n5criTcYxW0mtUjeW0OprW728GaYnAP4B1haqwl7kEj4RlbYnG1VBPu7QP2viuZ1TsIX40JdijMu2Vesma4zR-KjNTwv5_3Ik4ASQup7NnzZEmlGQhrotJaPf6mDvWq6QvFaSmDPZ5LkVe-as1EAUUHSq990nQTTfUYhHgoQXMVwCI8jF2EkAwFfDzbhePS7hgQpq77xVFtAalGII_xVC5CPvVM8rS8-MzJPtJfxabiWNMaLsfYuDJtry7n0nUTzaRPnaurrHe1KziFHt2zY358; PREF=ID=1111111111111111:FF=2:LD=zh-CN:NR=10:NW=1:TM=1447078639:LM=1447156433:SG=1:V=1:S=haPZfXhE97t8UvEm"
                    # request.add_header('cookie', cookie)
                    request.add_header('User-agent', user_agent)
                    # request.add_header('connection','keep-alive')
                    # request.add_header('Accept-Encoding', 'gzip')
                    # refer = "https://ipv4.google.com/sorry/IndexRedirect?continue=https://www.google.com.hk/search%3Fnewwindow%3D1%26safe%3Dstrict%26es_sm%3D122%26q%3Dintext%253Axinali%26oq%3Dintext%253Axinali%26gs_l%3Dserp.3...12118168.12125338.0.12125587.13.12.0.0.0.0.459.1743.4-4.4.0....0...1c.1j4.64.serp..10.3.1325.0._PcWsBu9gy4&q=CGMSBC5lMzoY6r2HsgUiGQDxp4NLNUsyrkMU6CrmPfWnERWCHQAi5o0"
                    # request.add_header('referer', refer)
                    # x_client_data = "CKW2yQEIqbbJAQjBtskBCO2IygEI/ZXKAQi8mMoBCKCaygE="
                    # request.add_header('x-client-data', x_client_data)

                    # accept = "accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                    # request.add_header('accept', accept)

                    # accept_encoding = ""
                    # request.add_header('accept-encoding', accept_encoding)

                    # avail_dictionary="sFiQm0Xh,HuaaZ89d"
                    # request.add_header('avail-dictionary', avail_dictionary)


                    response = urllib2.urlopen(request)
                    html = response.read()
                    if(response.headers.get('content-encoding', None) == 'gzip'):
                        html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

                    results = self.extractSearchResults(html)
                    search_results.extend(results)
                    break;
                except urllib2.URLError,e:
                    print 'url error:', e
                    self.randomSleep()
                    retry = retry - 1
                    continue

                except Exception, e:
                    print 'error:', e
                    traceback.print_exc()
                    retry = retry - 1
                    self.randomSleep()
                    continue
        return search_results

def load_user_agent():
    fp = open('./user_agents', 'r')

    line  = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()

def crawler():
    # Load use agent string from file
    load_user_agent()

    # Create a GoogleAPI instance
    api = GoogleAPI()

    # set expect search results to be crawled
    expect_num = 1000
    # if no parameters, read query keywords from file
    if(len(sys.argv) < 1):
        keywords = open('./keywords', 'r')
        keyword = keywords.readline()
        while(keyword):
            results = api.search(keyword, num = expect_num)
            for r in results:
                r.printIt()
            keyword = keywords.readline()
        keywords.close()
    else:
        # keyword = sys.argv[1]
        # keyword = 'inurl:wp-content/themes/persuasion/lib/scripts/dl-skin.php'
        keyword = 'test'
        # keyword = "intext:xinali"
        results = api.search(keyword, num = expect_num)
        for r in results:
            r.printIt()

if __name__ == '__main__':
    os.system('clear')
    crawler()
