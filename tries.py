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
        
save_counter(0)
save_tree({})