import socket
import sys
import os

# Create socket
host = ''
port = 8000
addr = (host, port)
server = socket.socket(socket.AF_INET)
server.bind(addr)
server.listen(10)

# For each connection
while True:
    sc, address = server.accept() # Connect to client
    filename = sc.recv(1024).decode("utf-8") # Get name of file

    f.close()
    sc.close()

server.close()