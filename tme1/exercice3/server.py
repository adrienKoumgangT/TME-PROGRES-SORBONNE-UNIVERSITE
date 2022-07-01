import datetime
import socket
import threading
import struct
import pathlib
import zlib


VERSION_ENCODE = 'utf-8'
BUFFER_SIZE = 1024
SERVER_LISTEN = 5

storage_server = '.'
header_struct = struct.Struct('>i')


def send_message(sock, message):
    block_length = len(message)
    sock.sendall(header_struct.pack(block_length))
    sock.sendall(message)


def receive_all(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left'
                           ' in this block'.format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)


def receive_message(sock):
    dim = receive_all(sock, header_struct.size)
    (length_message,) = header_struct.unpack(dim)
    return receive_all(sock, length_message)


def analyse_request(request):
    pos_cap = request.find("\n")
    if pos_cap == -1:
        return None
    line1 = request[0:pos_cap]
    pos_s = line1.find("/")
    if pos_s == -1:
        return None
    pos_ss = line1.find(" ", pos_s)
    if pos_ss == -1:
        return request[pos_s+1]
    else:
        return request[pos_s+1: pos_ss]


def form_response(response, base, app_version, info_date,
                  content_type, content_length):
    line1 = "HTTP/1.0 " + response
    line2 = "Server: " + base + ":" + app_version
    line3 = "Date: " + info_date
    line4 = "Content-type: " + content_type
    line5 = "Content-length: " + str(content_length)
    return line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5


def get_file(filename):
    if not filename:
        return None
    d = pathlib.Path(storage_server)
    for file in d.rglob(filename):
        if file.is_file():
            with open(str(file), 'rb') as f:
                return f.read()
    return None


def handle_client(socket_client):
    request = receive_message(socket_client).decode(VERSION_ENCODE)
    name_file = analyse_request(request)
    file = None
    if name_file:
        print()
        print("REQUEST: Demande du fichier" + name_file)
        print()
        file = get_file(name_file)
    else:
        print()
        print("REQUEST: Demande invalide")
        print()
    if file:
        data = zlib.compress(file)
        length_file = len(data)
        dt = datetime.datetime.now()
        response = form_response("200 OK", "BaseHTTP/0.6", "Python/3.8.10", str(dt), "text", length_file)
        send_message(socket_client, response.encode(VERSION_ENCODE))
        socket_client.sendall(data)
    else:
        dt = datetime.datetime.now()
        response = form_response("404 Not Found", "BaseHTTP/0.6", "Python/3.8.10", str(dt), "text", 0)
        send_message(socket_client, response.encode(VERSION_ENCODE))
    socket_client.close()


def run(server_port=1234):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(SERVER_LISTEN)
    print("server ready")
    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, )).start()


if __name__ == '__main__':
    run()
