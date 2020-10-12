import socket
import sys
from pathlib import Path

#---------------- Global --------------------

BUFFER = 1024
current_dir = []

#---------------- Functions --------------------

def print_current_dir():
    for i in current_dir:
        print(i + '/',end='')

def help():
    print("init - Initialize the storage on a new system, remove any existing file in the dfs root directory and return available size.")
    print("create *file name* -  create a new empty file")
    print("read *file name* - download a file from the DFS")
    print("write *file name* - upload a file from the Client side to the DFS")
    print("delete *file name* - delete file from DFS")
    print("info *file name* - information about the file")
    print("rename *file name* *new file name* - information about the file")
    print("copy *file name* *path* - create a copy of file")
    print("move *file name* *path* - move a file to the specified path")
    print("cd *path* - change directory")
    print("ls - list of files, which are stored in the directory")
    print("mkdir *path* - create a new directory")
    print("deldir *path* - delete directory")
    print("q - exit")    

def init(in_str, s_to_name):
    s_to_name.send(bytes(in_str[0], 'utf-8'))
    print('Size available: ' + s_to_name.recv(BUFFER).decode('utf-8'))

def create(in_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
    else:
        print('Error: Incorrect number of parameters')
        
def write(in_str, s_to_name):
    if (len(in_str) == 2):
        file_ = open (in_str[1], "rb")
        data = file_.read(BUFFER)
        if (not data):
            print('File is empty! use create')
            return        
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
        res = s_to_name.recv(BUFFER).decode('utf-8')
        if (res == '1'):
            print('It\'s directory! Not the file')
            file_.close()
            return
        while(data):
            s_to_name.send(data)
            s_to_name.recv(BUFFER)
            data = file_.read(BUFFER)  
        s_to_name.send(bytes('Eof0End0Eof', 'utf-8'))
        file_.close()
    else:
        print('Error: Incorrect number of parameters')  
        
def read(in_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == 'Empty'):
            print('Empty file or file does not exist')
        else:
            file_ = open(in_str[1],'wb+')
            data = s_to_name.recv(BUFFER)
            while (data):
                file_.write(data)
                s_to_name.send(bytes('Ok', 'utf-8'))
                data = s_to_name.recv(BUFFER)
                if (data.decode('utf-8') == 'Eof0End0Eof'):
                    break
            file_.close()           
    else:
        print('Error: Incorrect number of parameters')  

def info(input_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == '1'):
            print('No such file')
        print(ans)
    else:
        print('Error: Incorrect number of parameters')  

def delete(in_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == '1'):
            print('No such file')      
    else:
        print('Error: Incorrect number of parameters')    

def rename(in_str, s_to_name):
    if (len(in_str) == 3):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1] + ' ' + in_str[2], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == '1'):
            print('No such file or directory')      
    else:
        print('Error: Incorrect number of parameters')

def copy(in_str, s_to_name):
    if (len(in_str) == 3):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1] + ' ' + in_str[2], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == '1'):
            print('No such file')
        if (ans == '2'):
            print('No such directory')            
    else:
        print('Error: Incorrect number of parameters')  

def move(in_str, s_to_name):
    if (len(in_str) == 3):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1] + ' ' + in_str[2], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == '1'):
            print('No such file')
        if (ans == '2'):
            print('No such directory')            
    else:
        print('Error: Incorrect number of parameters')  
    
def cd(in_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
        ans = s_to_name.recv(BUFFER).decode('utf-8')
        if (ans == 'Ok'):
            if (in_str[1] != '..'):
                current_dir.append(in_str[1])
            else:
                current_dir.pop()
        else:
            print('Command failed')
    else:
        print('Error: Incorrect number of parameters')
    
def ls(in_str, s_to_name):
    if (len(in_str) == 1):
        s_to_name.send(bytes(in_str[0], 'utf-8'))
        ans_d = s_to_name.recv(BUFFER * 2).decode("utf-8")
        s_to_name.send(bytes('Ok', 'utf-8'))
        ans_f = s_to_name.recv(BUFFER * 2).decode("utf-8")
        print('directories:' + ans_d)
        print('files:' + ans_f)
    else:
        print('Error: Incorrect number of parameters')    
    
def mkdir(in_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8')) 
    else:
        print('Error: Incorrect number of parameters')    
    
def deldir(in_str, s_to_name):
    if (len(in_str) == 2):
        s_to_name.send(bytes(in_str[0] + ' ' + in_str[1], 'utf-8'))
        rep = s_to_name.recv(BUFFER).decode('utf-8')
        if (rep == 'Ok'):
            s_to_name.send(bytes('Ok', 'utf-8'))        
        if (rep == 'Not empty'):
            print('Directory is not empty. Delete directory? (print ''Ok'' to accept)')
            s_to_name.send(bytes(input(), 'utf-8'))
        if (rep == '1'):
            print('No such directory')
    else:
        print('Error: Incorrect number of parameters')     

#---------------- Program --------------------


# Get parameters from console
# filename = sys.argv[1]
host = sys.argv[1]
port = 8000 # int(sys.argv[2])

# Get size of file in bytes
# filesize = Path(filename).stat().st_size
# currentfilesize = 0

# Create socket
s = socket.socket(socket.AF_INET)
# Connect to server
s.connect((host,port))

# Send name of file
# s.send(bytes(filename, 'utf-8'))
# Send file data
# f = open (filename, "rb")
# l = f.read(1024)

while (True):
    print(">>",end='')
    print_current_dir()
    input_str = input().split()
    if (input_str[0] == "help"):
        help()
        continue
    if (input_str[0] == "create"):
        create(input_str, s)
        continue
    if (input_str[0] == "read"):
        read(input_str, s)
        continue
    if (input_str[0] == "write"):
        write(input_str, s)
        continue
    if (input_str[0] == "delete"):
        delete(input_str, s)
        continue
    if (input_str[0] == "init"):
        init(input_str, s)
        continue
    if (input_str[0] == "info"):
        info(input_str, s)
        continue
    if (input_str[0] == "rename"):
        rename(input_str, s)
        continue    
    if (input_str[0] == "copy"):
        copy(input_str, s)
        continue
    if (input_str[0] == "move"):
        move(input_str, s)
        continue
    if (input_str[0] == "cd"):
        cd(input_str, s)
        continue
    if (input_str[0] == "ls"):
        ls(input_str, s)
        continue
    if (input_str[0] == "mkdir"):
        mkdir(input_str, s)
        continue
    if (input_str[0] == "deldir"):
        deldir(input_str, s)
        continue
    if (input_str[0] == "q"):
        s.send(bytes('close', 'utf-8'))
        break;
    print("Unknow command")
s.close()

# python client.py car.png "18.188.141.97" 8888
