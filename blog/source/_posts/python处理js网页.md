---
title: python处理js网页
categories: Technology
tags:
  - python
  - javascript
  - nodejs
---

python处理含有js代码的数据，目前我能想到的有两种方法，以后要是有新的方法，再添加

## python利用phantomjs模拟浏览器发送请求

该方法遇到的主要弊端

1. 无法发送post请求
   看到SO上有人用seleniumrequests，也尝试使用了一下，但是request请求返回的response并不是解析完js的数据
    ```python
    from seleniumrequests import PhantomJS
    driver = PhantomJS()
    response = driver.request("GET/POST", url, data=post_data, headers=headers)
    ```
    response.text/driver.page_source 都不对

2. 发送修改后的headers，有各种问题
    ```python
    webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.settings.userAgent"] = user_agent
    for key, value in headers.iteritems():
        print key, value
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS()
    driver.get(url)
    ```
增加cookie的过程中也会出现各种各样的问题，我遇到的诸如数据无法解析，完全乱码，具体原因，我自己查了很久资料也没有弄明白~>_<~

**综合上面的讨论，在不需要post，不需要增加cookie，不需要更改header的情况下，phantomjs是一种不错的选择**
直接使用的代码片段
```python
driver = webdriver.PhantomJS()
driver.get(url)
// handle driver.page_source
```
> driver.page_source是js解析完成的数据

该种方法也可以用nodejs实现，但是实现的过程中也出现了各种各样的问题
简单的实现：
```javascript
var page = require('webpage').create();
var url = 'http://www.freeproxylists.net/zh/?page=1';
// get this data from chrome by "Copy as cURL"
var raw_curl_data = "curl 'http://www.freeproxylists.net/zh/?page=1' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' --compressed"

raw_curl_data  = raw_curl_data.substring(5, raw_curl_data.length-12);
var raw_headers = raw_curl_data.split('-H');
// delete curl and url
raw_headers.shift();
var headers = {};

for (var i in raw_headers) {
	header = raw_headers[i].replace(/'/g, '').split(':');
	header[1] = header[1].replace(/^\s/g, '')
		header[0] = header[0].replace(/^\s/g, '')
		if (header[0] == "User-Agent") {
			page.settings.userAgent = header[1]
		}
		else{
			headers[header[0]] = header[1];
		}
}
page.customHeaders = headers;
page.open(url, 'GET', function(status) {
	if (status == 'success'){
		//console.log(page.content);
		console.log(page.plainText);
	}
	phantom.exit();
});
```

## python利用requests请求,nodejs解析
该方法的主要弊端就是无法获取js处理后的数据，需要自己进行处理
> 该种方法如果在需要post/header/cookies的情况下，比第一种处理起来更加快速，并且更加的方便

主要的思路就是利用requests获取含有js代码的网页，之后下载网页的js代码，利用nodejs对需要nodejs处理的数据进行处理

这里用我处理过的一个例子做解说：
现在需要获取`http://www.freeproxylists.net/zh/?page=1`中1-24页的代理数据，因为需要进行谷歌验证，所以必须携带cookie和更改后的header，才能进行抓取
1. 利用浏览器对该网址进行访问(需要翻墙)，并填写谷歌验证码，成功打开proxy列表，此时利用谷歌开发者工具
> F12 => network选项 找到?page=1这个访问，右键Copy as cURL，成功获取相关header以及cookie 可以在粘贴到命令行下进行测试，测试成功

复制的数据应该像这样
>* culr_data

```shell
$ curl 'http://www.freeproxylists.net/zh/?page=1' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: visited=2016%2F05%2F19+22%3A15%3A19; hl=zh; pv=36; userno=20160517-009599; from=link; refdomain=blog.csdn.net; __atuvc=38%7C20; __atuvs=573ea90da7d10608003; __utma=251962462.39463521.1463478053.1463719902.1463724302.16; __utmb=251962462.8.10.1463724302; __utmc=251962462; __utmz=251962462.1463478053.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/ithomer/article/details/7639385; __utmv=251962462.United%20States' -H 'Connection: keep-alive' --compressed
```

写了一个专门处理复制curl数据的python文件，可以从复制的内容中提取cookie，header，post数据，源代码如下
>* filename: get_curl_header_post.py

```python
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
```
2. 我们需要的数据是ip和端口，从网页的源代码中观察到ip地址是经过js解析生成的。
```http
<script type="text/javascript">IPDecode("%3c%61%20%68%72%65%66%3d%22%68%74%74%70%3a%2f%2f%77%77%77%2e%66%72%65%65%70%72%6f%78%79%6c%69%73%74%73%2e%6e%65%74%2f%7a%68%2f%32%31%38%2e%31%38%2e%31%30%39%2e%31%38%37%2e%68%74%6d%6c%22%3e%32%31%38%2e%31%38%2e%31%30%39%2e%31%38%37%3c%2f%61%3e")</script>
```
数据的解析是通过IPDecode函数实现的，在查看网页的源码中发现IPDecode的定义如下：
```javascript
function IPDecode(IP)
{
	document.write(utf.URLdecode(IP));
}
```
搜索utf中的URLdecode函数，发现utf是在utf.js中定义的，查看utf.js的源码，发现URLdecode函数定义如下：
>* filename: utf.js

```javascript
utf = new function() {
    
    // some other functions here
    
    this.URLdecode = function(_dat)
    {
        _dat = _dat.replace(/\+/g, "\x20");
        _dat = _dat.replace( /%([a-fA-F0-9][a-fA-F0-9])/g, 
                function(_tmp, _hex){ return String.fromCharCode( parseInt(_hex, 16) ) } );
        return this.packChar( this.toUTF16( this.unpackUTF16(_dat) ) );
    }
}
```
既然已经知道了解析ip地址的js代码，利用nodejs实现起来就相当容易了。
首先，下载utf.js文件，将其改写为nodejs的一个模块，改写如下
> * filename: utf.js(updated)

```nodejs
utf = function() {
    
    // some other functions here
    
    this.URLdecode = function(_dat)
    {
        _dat = _dat.replace(/\+/g, "\x20");
        _dat = _dat.replace( /%([a-fA-F0-9][a-fA-F0-9])/g, 
                function(_tmp, _hex){ return String.fromCharCode( parseInt(_hex, 16) ) } );
        return this.packChar( this.toUTF16( this.unpackUTF16(_dat) ) );
    }
}
module.exports = utf;
```
改造完成之后，利用nodejs解析ip地址的代码
> * filename: get_ip.js

```nodejs
var fs = require('fs'),
    readline = require('readline'),
    Utf = require('./utf.js'),
    utf_obj = new Utf();

var rd = readline.createInterface({
    input: fs.createReadStream(process.argv[2]),
});

rd.on('line', function(line) {
    console.log(utf_obj.URLdecode(line));
});
```
完整的利用代码如下：
>* filename: get_proxy.py

```python
#!/usr/bin/env python
# encoding: utf-8

import requests
import IPython
import re
import subprocess
from get_curl_header_post import get_curl_header_post

class Getproxy(object):

    def __init__(self):
        self.proxy_file = open('proxy.txt', 'w')

    def handle_html(self):

        pattern_ip = re.compile("IPDecode\(\"(\S+)\"\)")
        pattern_port = re.compile("\"center\"\>(\d+)\<\/td")
        all_ip = pattern_ip.findall(self.response.text)
        all_port = pattern_port.findall(self.response.text)

        ip_file_name = 'ip.txt'
        ip_file = open(ip_file_name, 'w')
        for ip in all_ip:
            ip_file.write(ip+'\n')
        ip_file.close()
        // get the output of nodejs
        result_out = subprocess.Popen(["nodejs", "get_ip.js", ip_file_name], stdout=subprocess.PIPE)
        ip_readlines = result_out.stdout.readlines()

        i = 0
        for ip in ip_readlines:
            extract_ip = re.search(">(\S+)<", ip)
            if extract_ip:
                self.proxy_file.write(extract_ip.groups(0)[0] + ' ' + all_port[i] + '\n')
                i += 1

    def get_proxy(self):

        raw_curl_data = "curl data"
        headers, post_data = get_curl_header_post(raw_curl_data)

        for page in xrange(1, 25):
            url = 'http://www.freeproxylists.net/zh/?page=%s' % (str(page))
            self.response = requests.get(url, headers=headers)
            self.handle_html()
            print 'getting page %d successfully...' % page

        self.proxy_file.close()

def main():
    getproxy = Getproxy()
    getproxy.get_proxy()
    
if __name__ == '__main__':
    main()
```
