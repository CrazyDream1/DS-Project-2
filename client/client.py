import socket
import sys
from pathlib import Path

# Get parameters from console
# filename = sys.argv[1]
#host = sys.argv[1]
#port = int(sys.argv[2])

# Get size of file in bytes
# filesize = Path(filename).stat().st_size
# currentfilesize = 0

# Create socket
# s = socket.socket(socket.AF_INET)
# Connect to server
# s.connect((host,port))

# Send name of file
# s.send(bytes(filename, 'utf-8'))
# Send file data
# f = open (filename, "rb")
# l = f.read(1024)

while (True):
    input_str = input().split()
    if (input_str[0] == "help"):
        print("init - Initialize the storage on a new system, remove any existing file in the dfs root directory and return available size.")
        print("create *file name* -  create a new empty file")
        print("read *file name* - download a file from the DFS")
        print("write *file name* - upload a file from the Client side to the DFS")
        print("delete *file name* - delete file from DFS")
        print("info *file name* - information about the file")
        print("copy *file name* *path* - create a copy of file")
        print("move *file name* *path* - move a file to the specified path")
        print("cd *path* - change directory")
        print("ls - list of files, which are stored in the directory")
        print("mkdir *path* - create a new directory")
        print("deldir *path* - delete directory")
        print("q - exit")
    if (input_str[0] == "create"):
        print("")
    if (input_str[0] == "read"):
        print("")
    if (input_str[0] == "write"):
        print("")
    if (input_str[0] == "delete"):
        print("")
    if (input_str[0] == "init"):
        print("")
    if (input_str[0] == "info"):
        print("")
    if (input_str[0] == "copy"):
        print("")      
    if (input_str[0] == "move"):
        print("")
    if (input_str[0] == "cd"):
        print("")
    if (input_str[0] == "ls"):
        print("")
    if (input_str[0] == "mkdir"):
        print("")
    if (input_str[0] == "deldir"):
        print("")    
    if (input_str[0] == "q"):
        break;
#s.close()

# python client.py car.png "18.188.141.97" 8888