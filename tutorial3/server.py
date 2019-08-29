import socket
import pickle
headersize =10
d = {1: 'Hey',2:'There'}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))

s.listen(5)

while True:
    clientsocket, address = s.accept()

    d = {1: 'Hey',2:'There'}
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{headersize}}",'utf-8')+msg
    clientsocket.send(msg)
