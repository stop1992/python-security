#!/usr/bin/env python
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("mail.html"))
print soup.prettify()
