from __future__ import print_function
import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostbyname('localhost') # Get local machine name (host to connect to)
port = 5555               # Reserve a port for your service.


server_addr = (host, port)
s.connect(server_addr)

f = open('testfile3.mp3','rb') #open in binary

x=1
tosend=f.read()

    
s.sendall(tosend) # remember to send as byte string
    
print('sending comlpete')
    
    
s.close()               # Close the socket when done
