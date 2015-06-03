import pexpect
import os, sys
import time
import pxssh

def start_localmongo():
	# kill mongo progress
	os.system('kill 2 `pgrep mongo`')
	# delete file
	os.system('rm -rf /data')

	# prepare shard1 files
	os.system('mkdir -p /data/shard1_1/db')
	os.system('mkdir -p /data/shard1_1/log')
	os.system('echo "this is a test key" > /data/shard1_1/key')
	os.system('chmod 600 /data/shard1_1/key')

	# prepare shard2 files
	os.system('mkdir -p /data/shard2_1/db')
	os.system('mkdir -p /data/shard2_1/log')
	os.system('echo "this is a test key" > /data/shard2_1/key')
	os.system('chmod 600 /data/shard2_1/key')

	# start shard1 & shard2
	os.system('mongod --shardsvr --replSet shard1 --dbpath /data/shard1_1/db --logpath /data/shard1_1/log/server.log --fork --port 27018 --directoryperdb --keyFile /data/shard1_1/key')
	# mongod --replSet shard1 --port 27020 --dbpath /data/shard1_1/arb --keyFile /data/shard1_1/key --fork --logpath /data/shard1_1/arbiter.log
	os.system('mongod --shardsvr --replSet shard2 --dbpath /data/shard2_1/db --logpath /data/shard2_1/log/server.log --fork --port 27019 --directoryperdb --keyFile /data/shard2_1/key')
	# mongod --replSet shard2 --dbpath /data/shard2_1/arb --port 27021 --keyFile /data/shard2_1/key --fork --logpath /data/shard2_1/arbiter.log

	# prepare configserver files
	os.system('mkdir -p /data/config/db')
	os.system('mkdir -p /data/config/log')
	os.system('echo "this is a test key" > /data/config/key')
	os.system('chmod 600 /data/config/key')

	# starting configserver
	os.system('mongod --configsvr --dbpath /data/config/db --logpath /data/config/log/config.log --keyFile /data/config/key --port 30000 --fork')

def prepare(child):
	child.sendline('rm -rf /data')
	child.sendline('kill 2 `pgrep mongo`')
	child.sendline('kill 2 `pgrep mongo`')

def start_dtpc2(child):
	prepare(child)
	# prepare shard1 files
	child.sendline('mkdir -p /data/shard1_2/db')
	child.sendline('mkdir -p /data/shard1_2/log')
	child.sendline('echo "this is a test key" > /data/shard1_2/key')
	child.sendline('chmod 600 /data/shard1_2/key')

	# prepare shard2 files
	child.sendline('mkdir -p /data/shard2_2/db')
	child.sendline('mkdir -p /data/shard2_2/log')
	child.sendline('echo "this is a test key" > /data/shard2_2/key')
	child.sendline('chmod 600 /data/shard2_2/key')

	# start shard1 & shard2
	child.sendline('mongod --shardsvr --replSet shard1 --dbpath /data/shard1_2/db --logpath /data/shard1_2/log/server.log --fork --port 27018 --directoryperdb --keyFile /data/shard1_2/key')
	# mongod --replSet shard1 --port 27020 --dbpath /data/shard1_1/arb --keyFile /data/shard1_1/key --fork --logpath /data/shard1_1/arbiter.log
	child.sendline('mongod --shardsvr --replSet shard2 --dbpath /data/shard2_2/db --logpath /data/shard2_2/log/server.log --fork --port 27019 --directoryperdb --keyFile /data/shard2_2/key')
	# mongod --replSet shard2 --dbpath /data/shard2_1/arb --port 27021 --keyFile /data/shard2_1/key --fork --logpath /data/shard2_1/arbiter.log

	# prepare configserver files
	child.sendline('mkdir -p /data/config/db')
	child.sendline('mkdir -p /data/config/log')
	child.sendline('echo "this is a test key" > /data/config/key')
	child.sendline('chmod 600 /data/config/key')

	# starting configserver
	child.sendline('mongod --configsvr --dbpath /data/config/db --logpath /data/config/log/config.log --keyFile /data/config/key --port 30000 --fork')


def start_dtpc3(child):

	prepare(child)
	# prepare shard1 files
	child.sendline('mkdir -p /data/shard1_3/db')
	child.sendline('mkdir -p /data/shard1_3/log')
	child.sendline('echo "this is a test key" > /data/shard1_3/key')
	child.sendline('chmod 600 /data/shard1_3/key')

	# prepare shard2 files
	child.sendline('mkdir -p /data/shard2_3/db')
	child.sendline('mkdir -p /data/shard2_3/log')
	child.sendline('echo "this is a test key" > /data/shard2_3/key')
	child.sendline('chmod 600 /data/shard2_3/key')

	# start shard1 & shard2
	child.sendline('mongod --shardsvr --replSet shard1 --dbpath /data/shard1_3/db --logpath /data/shard1_3/log/server.log --fork --port 27018 --directoryperdb --keyFile /data/shard1_3/key')
	# mongod --replSet shard1 --port 27020 --dbpath /data/shard1_1/arb --keyFile /data/shard1_1/key --fork --logpath /data/shard1_1/arbiter.log
	child.sendline('mongod --shardsvr --replSet shard2 --dbpath /data/shard2_3/db --logpath /data/shard2_3/log/server.log --fork --port 27019 --directoryperdb --keyFile /data/shard2_3/key')
	# mongod --replSet shard2 --dbpath /data/shard2_1/arb --port 27021 --keyFile /data/shard2_1/key --fork --logpath /data/shard2_1/arbiter.log

	# prepare configserver files
	child.sendline('mkdir -p /data/config/db')
	child.sendline('mkdir -p /data/config/log')
	child.sendline('echo "this is a test key" > /data/config/key')
	child.sendline('chmod 600 /data/config/key')

	# starting configserver
	child.sendline('mongod --configsvr --dbpath /data/config/db --logpath /data/config/log/config.log --keyFile /data/config/key --port 30000 --fork')

def ssh_command(user, host):
	child = pxssh.pxssh()
	child.login(host, user)
	return child
	# child.sendline(cmd)

def start_localmongos():
	# prepare mongos files
	os.system('mkdir -p /data/mongos')
	os.system('echo "this is a test key" > /data/mongos/key')
	os.system('chmod 600 /data/mongos/key')
	# starting mongos
	os.system('mongos --configdb 192.168.1.108:30000,192.168.1.110:30000,192.168.1.112:30000 --port 40000 --fork --logpath /data/mongos/monos.log --keyFile /data/mongos/key')


def start_mongos(child):
	# prepare mongos files
	child.sendline('mkdir -p /data/mongos')
	child.sendline('echo "this is a test key" > /data/mongos/key')
	child.sendline('chmod 600 /data/mongos/key')
	# starting mongos
	child.sendline('mongos --configdb 192.168.1.108:30000,192.168.1.110:30000,192.168.1.112:30000 --port 40000 --fork --logpath /data/mongos/monos.log --keyFile /data/mongos/key')

if __name__ == '__main__':
	os.system('printf "\033c"')

	start_localmongo()

	users = 'root'
	hosts = []
	hosts.append('192.168.1.110')
	hosts.append('192.168.1.112')
	child_2 = ssh_command(users, hosts[0])
	start_dtpc2(child_2)
	child_3 = ssh_command(users, hosts[1])
	start_dtpc3(child_3)

	start_localmongos()
	start_mongos(child_2)
	start_mongos(child_3)
