import socket
import sys

s = socket.socket()

host  = 'localhost'
port = int(sys.argv[1])

s.connect((host, port))
print(s.recv(1024))
s.send(b'hello world')
s.close()
