import os
import time
import socket



class ExpRedis(object):

    def __init__(self):
        pass

    def verify_redis(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        cmd = 'info\n'
        s.send(cmd)
        vul_redis = False
        if "redis_version" in s.recv(1024):
            print 'redis is vul'
            vul_redis = True
        else:
            print 'redis is not vul'

    def



def main():

    # host = '192.168.1.104'
    host = '127.0.0.1' # remote cannot connect
    port = 6379

    expredis = ExpRedis()
    expredis.verify_redis(host, port)


if __name__ == '__main__':
    os.system('clear')

    main()

