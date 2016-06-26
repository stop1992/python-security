# encoding:utf-8

import os
import pexpect
import sys

def login_server():
	ip = 'sk557.webcnam.net'
	name = 'ftp270704'
	password = 'woaiwangxiWOAIWANGXI68'
	cmd = 'ftp ' + ip
	child = pexpect.spawn(cmd)
	index = child.expect(['Name', pexpect.EOF, pexpect.TIMEOUT])
	print index
	if index == 0:
		child.sendline(name)
		index = child.expect(['Password', pexpect.EOF, pexpect.TIMEOUT])
		if index == 0:
			child.sendline(password)
	else:
		print 'login failed'
		return None
	print 'ftp login successfully'
	return child

def put_files(child):
	if len(sys.argv) > 1:
		child.sendline('delete ' + sys.argv[1])
		child.sendline('put ' + sys.argv[1])
		print 'put files successfully'

if __name__ == '__main__':
	os.system('printf "\033c"')
	os.chdir('/home/xinali/PhpstormProjects')

	child = login_server()
	if child:
		put_files(child)
