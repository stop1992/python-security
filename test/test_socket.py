

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.1.104'
# host = 'localhost'
host = '127.0.0.1'
port = 6379
sock.connect((host, port))

while True:
    cmd = 'info' + '\n'
    sock.send(cmd)
    data = sock.recv(1024)
    print data
    raw_input('wait...')

sock.close()
