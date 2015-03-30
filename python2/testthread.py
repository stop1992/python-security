#-*-coding:utf-8-*-

#!/usr/bin/env python

import thread
import os
import time

loops = [4, 2]

def loop(nloop, nsec, lock):
	print 'start loop', nloop, 'at: ', time.ctime()
	time.sleep(nsec)
	print 'end loop', nloop, 'done at:', time.ctime()
	lock.release()

def main():
	print 'starting main at:', time.ctime()
	locks = []
	nloops = range(len(loops))

	for i in nloops:
		lock = thread.allocate_lock()
		lock.acquire()
		locks.append(lock)

	for i in nloops:
		thread.start_new_thread(loop, (i, loops[i], locks[i]))

	for i in nloops:
		while locks[i].locked():
			pass

	print 'all DOne at:', time.ctime()

if __name__ == '__main__':
	os.system('printf "\033c"')
	main()
