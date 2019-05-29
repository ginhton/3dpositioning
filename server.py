import socket
import sys

s = socket.socket()
#; host = socket.gethostname()
host = '0.0.0.0'
port = int(sys.argv[1])
s.bind((host, port))

print(host, port)

s.listen(5)
while True:
    c,addr = s.accept();
    print('addr ', addr);
    c.send(b'hello world!')
    print(c.recv(1024))
    c.close()
