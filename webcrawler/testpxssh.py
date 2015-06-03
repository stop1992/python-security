#-*- encoding:utf-8 -*-

import pxssh
import os

if __name__ == "__main__":
	os.system('printf "\033c"')

	os.system('python testrepl.py')

	ssh = pxssh.pxssh()
	try:
		ssh.login('192.168.1.110', 'root')
		# print ssh
	except Exception, e:
		print str(e)

	ssh.sendline('pgrep mongo')
	ssh.prompt()
	print ssh.before + '\n\n\n'

	# ssh.sendline('kill 9 `pgrep mongo`')
	# ssh.sendline('kill 9 `pgrep mongo`')
	ssh.sendline('kill 9 `pgrep mongo`')
	ssh.prompt()
	print ssh.before

	ssh.sendline('pgrep mongo')
	print ssh.before
