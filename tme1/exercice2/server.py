import socket
import threading
import struct
import datetime

VERSION_ENCODE = 'utf-8'
BUFFER_SIZE = 1024
SERVER_LISTEN = 5


def handle_client(server_socket):
    client_socket, address = server_socket.accept()
    (cnt, ) = struct.unpack('>i', client_socket.recv(BUFFER_SIZE))
    if not cnt:
        client_socket.close()
    while cnt:
        message = client_socket.recv(BUFFER_SIZE).decode(VERSION_ENCODE)
        t = datetime.datetime.now().time()
        client_socket.sendall(str(t).encode(VERSION_ENCODE))
        cnt = cnt - 1
    client_socket.close()


def run(server_port=1236):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(SERVER_LISTEN)
    print("Serveur pret!")
    for i in range(SERVER_LISTEN):
        threading.Thread(target=handle_client, args=(server_socket, )).start()


if __name__ == '__main__':
    run()