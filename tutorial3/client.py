import socket
import pickle

headersize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    full_msg = b""
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f'length of the new msg {msg[:headersize]}')
            msglen = int(msg[:headersize])
            new_msg = False
        full_msg+=msg
        if len(full_msg)-headersize==msglen:
            print('full msg is received!')
            d = pickle.loads(full_msg[headersize:])
            print(d)
            new_msg = True
            full_msg= b''
