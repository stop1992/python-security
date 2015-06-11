import pexpect
import os
import pxssh

CREATE_DB_DIR = 'mkdir -p /testrepl/data/db' 
CREATE_LOG_DIR = 'mkdir -p /testrepl/data/log'
CREATE_KEY = 'echo "this is a test" >> /testrepl/data/key'
CHMOD_KEY = 'chmod 600 /testrepl/data/key'
START_MONGOD = 'mongod --fork --replSet rs --dbpath /testrepl/data/db --logpath /testrepl/data/log/server.log --port 50000 --keyFile /testrepl/data/key'

def start_localhost():
	os.system('kill 2 `pgrep mongo`')
	os.system('rm -rf /testrepl')
	os.system('mkdir -p /testrepl/data/db')
	os.system('mkdir -p /testrepl/data/log')
	os.system('echo "this is a test" >> /testrepl/data/key')
	os.system('chmod 600 /testrepl/data/key')
	os.system(START_MONGOD)

def ssh_command(user, host):
	# child = pexpect.spawn('ssh ' + user + host)
	child = pxssh.pxssh()
	child.login(host, user)
	child.sendline('kill 2 `pgrep mongo`')
	child.sendline('rm -rf /testrepl')
	child.sendline(CREATE_DB_DIR)
	child.sendline(CREATE_LOG_DIR)
	child.sendline(CREATE_KEY)
	child.sendline(CHMOD_KEY)
	child.sendline(START_MONGOD)
	child.prompt()
	print child.before
	# child.expect('successfully')
	# print child.after + '\n\n'

if __name__ == '__main__':
	os.system('printf "\033c"')

	start_localhost()

	user = 'root'
	hosts = []
	hosts.append('192.168.1.110')
	hosts.append('192.168.1.112')

	length = len(hosts)
	for i in xrange(length):
		ssh_command(user, hosts[i])
