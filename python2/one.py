#!/usr/bin/env python

import os
from string import Template

os.system('printf "\033c"')

__metaclass__ = type
class Bird:
	def __init__(self):
		self.sound = "bugubugu"
	def sing(self):
		print self.sound

class SongBird:
	def __init__(self):
		#Bird.__init__(self)
		super(SongBird, self).__init__()
		self.sound = "wangwang"
	def sing(self):
		print self.sound

bird = Bird()
bird.sing()
songBird = SongBird()
songBird.sing()
#s = Template('$thing, glorious $action!')
#d = {}
#d['thing'] = "daitao"
#d['action'] = "wangxi"
#s.substitute(d)
