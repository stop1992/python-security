import pexpect
import os
import pxssh

def ssh_command(user, host, cmd):
	child = pxssh.pxssh()
	child.login(host, user)

	child.sendline(cmd)
	child.prompt()
	print child.before

	child.sendline('rm -rf /testrepl')
	child.prompt()
	print child.before

	child.sendline('pgrep mongo')
	child.prompt()
	print child.before

if __name__ == '__main__':
	os.system('printf "\033c"')

	# os.system('python testrepl.py')

	os.system('/bin/kill 2 `pgrep mongo`')

	# user = 'root@'
	user = 'root'
	hosts = []
	hosts.append('192.168.1.110')
	hosts.append('192.168.1.112')
	cmd = 'kill 9 `pgrep mongo`'
	
	length = len(hosts)
	for i in xrange(length):
		ssh_command(user, hosts[i], cmd)
