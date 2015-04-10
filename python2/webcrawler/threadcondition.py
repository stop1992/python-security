#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import threading
import time

condition = threading.Condition()
product = 0

class Producer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		global product, condition
		while True:
			if condition.acquire():
				if product < 10:
					product += 1
					print 'Producer:%s produce a product, products:%d' % (self.name, product)
					condition.notify()
				else:
					print 'Product is already 10, so', self.name, 'wait'
					condition.wait()
					#print self.name, 'is waiting'
				condition.release()
				time.sleep(2)

class Consumer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		global condition, product
		while True:
			if condition.acquire():
				if product > 1:
					product -= 1
					print 'Consumer:', self.name, 'consume one, products:', product 
					condition.notify()
				else:
					print 'Consumer:', self.name, 'can not consume, product not enough'
					condition.wait()
				condition.release()
				time.sleep(2)

if __name__ == '__main__':
	os.system('printf "\033c"')

	for p in range(0, 2):
		p = Producer()
		p.start()

	for c in range(0, 5):
		c = Consumer()
		c.start()
