import socket
import sys
import os
import pickle

#---------------- Global --------------------

def load_tree():
    with open('tree.pickle', 'rb') as f:
        return pickle.load(f)

def save_tree(tree):
    with open('tree.pickle', 'wb') as f:
        pickle.dump(tree, f)

def load_counter():
    with open('counter.pickle', 'rb') as f:
        return pickle.load(f)

def save_counter(counter):
    with open('counter.pickle', 'wb') as f:
        pickle.dump(counter, f)

BUFFER = 1024
file_counter = load_counter()
tree = load_tree()
current_dir = [tree]
# {name, (0, {})} - folder; {name, (1, id)} - file
storages = [('10.0.150.3', 9000), ('10.0.150.4', 9000)]
failed_storages = [False, False]
active_storages = []

host = 'localhost'
port = 8000
addr = (host, port)
server = socket.socket(socket.AF_INET)
server.bind(addr)
server.listen(10)

#---------------- Functions --------------------

def replica(id_):
    for addr in active_storages[1:]:
        s_to_st = socket.socket(socket.AF_INET)
        s_to_st.connect(active_storage[0])
        s_to_st.send(bytes('send', 'utf-8'))
        s_to_st.recv(BUFFER)
        s_to_st.send(bytes(str(id_) + ' ' + addr[0], 'utf-8'))
        s_to_st.close()
    return

def replicate_all(i):
    a = 0

def check_active():
    active_storages = []
    i = 0
    for addr in storages:
        try:
            s_to_st = socket.socket(socket.AF_INET)
            s_to_st.connect(addr)
        except:
            print('No connection to ' + [x for x,_ in addr])
            failed_storages[i] = True
        else:
            active_storage.append(addr)
            s_to_st.close()
            if (failed_storages[i]):
                replicate_all(i)
            failed_storages[i] = False
        i += 1
	    
def create_empty(counter):
    for addr in active_storages:
        s_to_st = socket.socket(socket.AF_INET)
        s_to_st.connect(addr)
        s_to_st.send(bytes('create', 'utf-8'))
        s_to_st.recv(BUFFER)
        s_to_st.send(bytes(str(counter), 'utf-8'))
        s_to_st.close()

def storage_copy(id_f, file_counter):
    s_to_st = socket.socket(socket.AF_INET)
    s_to_st.connect(('localhost', 9000))
    s_to_st.send(bytes('copy', 'utf-8'))
    s_to_st.recv(BUFFER)
    s_to_st.send(bytes(str(id_f) + ' ' + str(file_counter), 'utf-8'))
    s_to_st.close() 

def storage_delete(id_):
    for addr in active_storages:
        s_to_st = socket.socket(socket.AF_INET)
        s_to_st.connect(addr)
        s_to_st.send(bytes('delete', 'utf-8'))
        s_to_st.recv(BUFFER)
        s_to_st.send(bytes(str(id_), 'utf-8'))
        s_to_st.close()

# Delete all files and directories from dir_ on storage server
def rec_del(dir_):
    for i,j in dir_.items():
        code, id_or_dir = j
        if (code == 0):
            rec_del(id_or_dir)
        else:
            storage_delete(id_or_dir)

def info(sc, name):
    s_to_st = socket.socket(socket.AF_INET)
    s_to_st.connect(active_storage[0])
    s_to_st.send(bytes('info', 'utf-8'))
    s_to_st.recv(BUFFER)
    s_to_st.send(bytes(str(name), 'utf-8'))
    ans = s_to_st.recv(BUFFER)
    sc.send(BUFFER)

def init(sc):
    global tree
    global file_counter
    print(tree,flush=True)
    rec_del(tree)
    tree = {}
    file_counter = 0
    save_tree(tree)
    save_counter(file_counter)
    print(tree,flush=True)
    for addr in active_storages:
        s_to_st = socket.socket(socket.AF_INET)
        s_to_st.connect(('localhost',9000))
        s_to_st.send(bytes('init', 'utf-8'))
        ans = s_to_st.recv(BUFFER)
    print(ans)
    sc.send(ans)
    s_to_st.close()

def create(sc, name):
    global file_counter
    current_dir[len(current_dir) - 1].update({name:(1, file_counter)})
    create_empty(file_counter)
    file_counter += 1
    save_counter(file_counter)
    save_tree(tree)

def write(sc, name):
    global file_counter
    code, id_ = current_dir[len(current_dir) - 1].get(name, (-1,-1))
    if (code == 0):
        sc.send(bytes('1', 'utf-8'))
    else:
        sc.send(bytes('Ok', 'utf-8'))
    s_to_st = socket.socket(socket.AF_INET)
    s_to_st.connect(active_storages[0])
    s_to_st.send(bytes('write', 'utf-8'))
    if (code == -1):
        current_dir[len(current_dir) - 1].update({name:(1, file_counter)})
        id_ = file_counter
        file_counter += 1
        save_tree(tree) 
        save_counter(file_counter)
    s_to_st.recv(BUFFER)
    s_to_st.send(bytes(str(id_), 'utf-8'))
    s_to_st.recv(BUFFER)
    data = sc.recv(BUFFER)
    while (data):
        s_to_st.send(data)
        sc.send(bytes('Ok', 'utf-8'))
        data = sc.recv(BUFFER)
        if (data.decode('utf-8') == 'Eof0End0Eof'):
            break
    s_to_st.close()
    replica(id_)
    
def read(sc, name):
    code, id_ = current_dir[len(current_dir) - 1].get(name, (-1,-1))
    if (code == 0 or code == -1):
        sc.send(bytes('Empty', 'utf-8'))
        return
    else:
        sc.send(bytes('Ok', 'utf-8'))
    s_to_st = socket.socket(socket.AF_INET)
    s_to_st.connect(active_storages[0])
    s_to_st.send(bytes('read', 'utf-8'))
    s_to_st.recv(BUFFER)
    s_to_st.send(bytes(str(id_), 'utf-8'))
    data = s_to_st.recv(BUFFER)
    while (data):
        sc.send(data)
        data = s_to_st.recv(BUFFER)
        sc.recv(BUFFER)
    sc.send(bytes('Eof0End0Eof', 'utf-8'))
    s_to_st.close()

def delete(sc, name):
    code, id_ = current_dir[len(current_dir) - 1].pop(name, (-1,-1))    
    if (code == -1 or code == 0):
        sc.send(bytes('1', 'utf-8'))
        print('Error code 1')
        return
    sc.send(bytes('Ok', 'utf-8'))
    storage_delete(id_)
    save_tree(tree)

def rename(sc, name1, name2):
    names = [name1,name2]
    code, id_ = current_dir[len(current_dir) - 1].pop(names[0], (-1,-1))
    if (code == -1):
        sc.send(bytes('1', 'utf-8'))
        print('Error code 1')
        return
    current_dir[len(current_dir) - 1].update({names[1]: (code, id_)})
    sc.send(bytes('Ok', 'utf-8'))
    save_tree(tree)
    
def copy(sc, name1, name2):
    global file_counter
    name = [name1, name2]
    code_f, id_f = current_dir[len(current_dir) - 1].get(name[0], (-1,-1))
    if (code_f == -1 or code_f == 0):
        sc.send(bytes('1', 'utf-8'))
        print('Error code 1')
        return 
    if (name[1] != '..'):
        code_d, directory = current_dir[len(current_dir) - 1].get(name[1], (-1,-1))
        if (code_d == -1 or code_d == 1):
            sc.send(bytes('2', 'utf-8'))
            print('Error code 2')
            return
        directory.update({name[0]:(1,file_counter)})
        storage_copy(id_f, file_counter)
        file_counter += 1
        sc.send(bytes('Ok', 'utf-8'))
    else:
        if (len(current_dir) < 2):
            sc.send(bytes('2', 'utf-8'))
            print('Error code 2')
            return
        current_dir[len(current_dir) - 2].update({name[0]:(1,file_counter)})
        storage_copy(id_f, file_counter)
        file_counter += 1
        sc.send(bytes('Ok', 'utf-8'))
    save_tree(tree)
    save_file_counter(file_counter)

def move(sc, name1, name2):
    name = [name1, name2]
    code_f, id_f = current_dir[len(current_dir) - 1].get(name[0], (-1,-1))
    if (code_f == -1 or code_f == 0):
        sc.send(bytes('1', 'utf-8'))
        print('Error code 1')
        return 
    if (name[1] != '..'):
        code_d, directory = current_dir[len(current_dir) - 1].get(name[1], (-1,-1))
        if (code_d == -1 or code_d == 1):
            sc.send(bytes('2', 'utf-8'))
            print('Error code 2')
            return
        current_dir[len(current_dir) - 1].pop(name[0], (-1,-1))
        directory.update({name[0]:(1,id_f)})
        sc.send(bytes('Ok', 'utf-8'))
    else:
        if (len(current_dir) < 2):
            sc.send(bytes('2', 'utf-8'))
            print('Error code 2')
            return
        current_dir[len(current_dir) - 1].pop(name[0], (-1,-1))
        current_dir[len(current_dir) - 2].update({name[0]:(1,id_f)})
        sc.send(bytes('Ok', 'utf-8'))
    save_tree(tree)
    
def cd(sc, dir_name):
    if (dir_name == '..' and len(current_dir) > 1):
        sc.send(bytes('Ok', 'utf-8'))
        current_dir.pop()
        return
    for i,j in current_dir[len(current_dir) - 1].items():
        code, new_dir = j
        if (i == dir_name and code == 0):
            sc.send(bytes('Ok', 'utf-8'))
            current_dir.append(new_dir)
            return
    sc.send(bytes('Fail', 'utf-8'))
    
def ls(sc):
    ans_d = ' '
    ans_f = ' '
    for i,j in current_dir[len(current_dir) - 1].items():
        code, n = j # code 0 - dir, code 1 - file
        if (code == 1):
            ans_f += i + ' '
        else:
            ans_d += i + ' '
    sc.send(bytes(ans_d, 'utf-8'))
    sc.recv(BUFFER)
    sc.send(bytes(ans_f, 'utf-8'))
    
def mkdir(sc, name):
    current_dir[len(current_dir) - 1].update({name:(0, {})})
    save_tree(tree)
    
def deldir(sc, name):
    code, n_dir = current_dir[len(current_dir) - 1].get(name,(-1,-1))
    if (code != 0):
        print('Error code 1')
        sc.send(bytes('1', 'utf-8'))
        return
    if (len(n_dir) > 0):
        sc.send(bytes('Not empty', 'utf-8'))
    else:
        sc.send(bytes('Ok', 'utf-8'))
    rep = sc.recv(BUFFER).decode('utf-8')
    if (rep == 'Ok'):
        rec_del(current_dir[len(current_dir) - 1].pop(name,0))
        save_tree(tree)
 
#---------------- Program --------------------

#print(tree)
# Create socket
host = 'localhost'
port = 8000
addr = (host, port)
server = socket.socket(socket.AF_INET)
server.bind(addr)
server.listen(10)

while True:
    soc_to_c, address = server.accept() # Connect to client
    
    check_active()
    if (len(active_storage) == 0):
        print('No active servers')
        continue
    
    while True:
        command = soc_to_c.recv(1024).decode("utf-8").split() # Get command
        print(command, flush=True)
        add_com1 = ''
        add_com2 = ''
        if (len(command) > 2):
            add_com2 = command[2]
        if (len(command) > 1):
            add_com1 = command[1]
        if (len(command) > 0):
        	command = command[0]
        if (command == "create"):
            create(soc_to_c, add_com1)
            continue
        if (command == "read"):
            read(soc_to_c, add_com1)
            continue
        if (command == "write"):
            write(soc_to_c, add_com1)
            continue
        if (command == "delete"):
            delete(soc_to_c, add_com1)
            continue
        if (command == "init"):
            init(soc_to_c)
            continue
        if (command == "info"):
            info(soc_to_c, add_com1)
            continue
        if (command == "rename"):
            rename(soc_to_c, add_com1, add_com2)
            continue        
        if (command == "copy"):
            copy(soc_to_c, add_com1, add_com2)
            continue
        if (command == "move"):
            move(soc_to_c, add_com1, add_com2)
            continue
        if (command == "cd"):
            cd(soc_to_c, add_com1)
            continue
        if (command == "ls"):
            ls(soc_to_c)
            continue
        if (command == "mkdir"):
            mkdir(soc_to_c, add_com1)
            continue
        if (command == "deldir"):
            deldir(soc_to_c, add_com1)
            continue
        if (command == 'close'):
            break
    soc_to_c.close()
    current_dir = [tree]

server.close()
