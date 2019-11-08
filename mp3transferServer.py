#my program works as it should
from __future__ import print_function
import socket 

# create a TCP socket for the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the address of localhost
host = socket.gethostbyname('localhost')
port = 5555

# set options to circumvent proper socket release
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# create pair for host address (this machine)
host_addr = (host, port)
s.bind(host_addr) # bind socket to aforementioned address


# make socket at server listen for incoming inconnections
s.listen(10)
print('Starting to listen for requests')
can1=0
can2=0
x=0
f = open('testsuccess.mp3','wb') # Open in binary
#while True:
c, addr = s.accept() # accept connection from client
print('Got connection from ', addr)
while True:
    musfile=c.recv(4096) 
    #musfile=musfile.decode()
    if not musfile:
        break
    f.write(musfile)
print('writing to file complete')
f.close()

c.close() # close connection after processing

