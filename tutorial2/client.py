import socket
headersize = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))


while True:
    full_msg = ""
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f'lenght of the new_msg : {msg[:headersize]}')
            msglen = int(msg[:headersize])
            new_msg = False

        full_msg += msg.decode('utf-8')
        if len(full_msg)-headersize == msglen:
            print('full message is received !')
            print(f'{full_msg[headersize:]}')
            new_msg = True
            full_msg = ""
