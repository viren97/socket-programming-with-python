import socket
import select

headersize = 10
ip = '127.0.0.1'
port = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip, port))
server_socket.listen();

socket_list = [server_socket]
clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(headersize)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8'))
        return {'header': message_header,
                'data': client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        #if notifieed socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            if user is False:
                continue
            socket_list.append(client_socket)
            #saving username_header and username in clients dict
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
        #if existing socket is sending message
        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            #broadcasting message over the clients in chatroom
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header']+user['data']+message['header']+message['data'])


    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
