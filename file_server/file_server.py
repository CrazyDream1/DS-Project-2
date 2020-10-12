import socket
import sys
import os
from subprocess import Popen, PIPE

BUFFER = 1024

#---------------- Functions --------------------

def init(sn):
    p = Popen('df -h .', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    ans = out.split()
    sn.send(ans[10])

def erase(sn):
    sn.send(bytes('Ok', 'utf-8'))
    name = sn.recv(BUFFER).decode("utf-8")
    p = Popen('rm ' + name, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()    

def create_empty(sn):
    sn.send(bytes('Ok', 'utf-8'))
    name = sn.recv(BUFFER).decode("utf-8")
    file_ = open(name, 'wb+')
    file_.close()

def info(sn):
    sn.send(bytes('Ok', 'utf-8'))
    name = sn.recv(BUFFER).decode("utf-8")
    p = Popen('stat -t ' + name, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    sn.send(bytes(out, 'utf-8'))

def copy(sn):
    sn.send(bytes('Ok', 'utf-8'))
    names = sn.recv(BUFFER).decode("utf-8").split()
    p = Popen('cp ' + names[0] + ' ' + names[1], shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()    

def download_file(sn):
    sn.send(bytes('Ok', 'utf-8'))
    name = sn.recv(BUFFER).decode("utf-8")
    print(name,flush=True)
    file_ = open(name, 'rb')
    data = file_.read(BUFFER)
    while (data):
        sn.send(data)
        data = file_.read(BUFFER)
    sn.close()
          
def upload_file(sn):
    sn.send(bytes('Ok', 'utf-8'))
    name = sn.recv(BUFFER).decode("utf-8")
    sn.send(bytes('Ok', 'utf-8'))
    print(name,flush=True)
    file = open(name, 'wb+')
    data = sn.recv(BUFFER)
    while (data):
        file.write(data)
        data = sn.recv(BUFFER)
    sn.close()

def send_file(sn):
    sn.send(bytes('Ok', 'utf-8'))
    a = sn.recv(BUFFER).decode("utf-8").split()
    id_ = a[0]
    Ip = a[1]
    s_to_st = socket.socket(socket.AF_INET)
    s_to_st.connect((Ip, 9000))
    s_to_st.send(bytes('receive', 'utf-8'))
    s_to_st.recv(BUFFER)
    s_to_st.send(bytes(id_, 'utf-8'))
    file_ = open(id_, 'rb+')
    data = file_.read(BUFFER)
    while(data):
        s_to_st.send(data)
        data = file_.read(BUFFER)
    s_to_st.close()
    
def receive_file(sn):
    sn.send(bytes('Ok', 'utf-8'))
    name = sn.recv(BUFFER).decode("utf-8")
    file_ = open(name, 'wb+')
    data = sn.recv(BUFFER)
    while(data):
        file_.write(data)
        data = sn.recv(BUFFER)
    
#---------------- Program --------------------

# Create socket
host = 'localhost'
port = 9000
addr = (host, port)
server = socket.socket(socket.AF_INET)
server.bind(addr)
server.listen(10)

# For each connection
while True:
    sn, address = server.accept()
    command = sn.recv(1024).decode("utf-8")
    if (command == 'write'):
        upload_file(sn)
    if (command == 'read'):
        download_file(sn)
    if (command == 'delete'):
        erase(sn)
    if (command == 'info'):
        info(sn)
    if (command == 'copy'):
        copy(sn)
    if (command == 'create'):
        create_empty(sn)
    if (command == 'init'):
        init(sn)
    if (command == 'send'):
        send_file(sn)
    if (command == 'receive'):
        receive_file(sn)
    print('Done ' + command)
    sn.close()

server.close()
