from BaseHTTPServer import *
import urllib2

class MyHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path
path=path[path.find('id=')+3:]
proxy_support = urllib2.ProxyHandler({"http":"http://127.0.0.1:8087"})
opener = urllib2.build\_opener(proxy\_support)
urllib2.install_opener(opener)
url="http://www.xxxxxxxxxxxxx.edu/magazine/imedia/gallery/dickinsons-last-dance/"
try:
    response=urllib2.urlopen(url+path)
html=response.read()
except urllib2.URLError,e:
    html=e.read()
self.wfile.write(html)
server = HTTPServer(("", 8000), MyHTTPHandler)
server.serve_forever()
