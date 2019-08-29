import socket
headersize = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234 ))
s.listen(5)

while True:
    clientsocket , address = s.accept()
    print(f"connection from {address} establilsed!")
    msg ='welcome to the server !'
    msg = f"{len(msg):<{headersize}}"+msg
    clientsocket.send(bytes(msg, 'utf-8'))
    while True:
        import time
        time.sleep(3)
        msg = f"the time is ! {time.time()}"
        msg = f"{len(msg):<{headersize}}"+msg
        clientsocket.send(bytes(msg, 'utf-8'))
