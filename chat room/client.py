import socket
import select
import errno
import sys

headersize = 10
ip = '127.0.0.1'
port = 1234
my_username = input('username: ')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))

client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{headersize}}".encode('utf-8')
client_socket.send(username_header+username)

while True:
    message = input(f'{my_username}> ')
    if message:
        message = message.encode('utf-8')
        message_header = f'{len(message):<{headersize}}'.encode('utf-8')
        client_socket.send(message_header+message)

    try:
        #now we wwant to loop over received messages and print them
        while True:
            username_header = client_socket.recv(headersize)

            if not len(username_header):
                print('Connection closed by the serve')
                sys.exit()

            username_length = int(username_header.decode('utf-8'))
            username = client_socket.recv(username_length).decode('utf-8')


            message_header = client_socket.recv(headersize)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username}> {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print(str(e))
