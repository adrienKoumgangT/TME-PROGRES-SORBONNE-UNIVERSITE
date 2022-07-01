import socket
import struct
import zlib

VERSION_ENCODE = 'utf-8'
BUFFER_SIZE = 1024

storage_client = '.'
header_struct = struct.Struct('>i')


def form_request(url_request, address_ip, address_port, accept_encoding,
                 user_agent, content_length):
    line1 = "GET /" + url_request + " HTTP/1.1"
    line2 = "HOST: " + address_ip + ":" + str(address_port)
    line3 = "Accept-Encoding: " + accept_encoding
    line4 = "User-Agent: " + user_agent
    line5 = "Content-length: " + content_length
    return line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line5


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


def analyse_response(response):
    # print(f'response = {response}')
    r = []
    pos_cap = response.find("\n")
    if pos_cap == -1:
        return None
    line1 = response[0:pos_cap]
    pos_sp = line1.find(" ")
    if pos_sp == -1:
        return None
    r.append(response[pos_sp+1:pos_cap])
    pos_l = response.find("Content-length")
    if pos_l == -1:
        return None
    r.append(response[pos_l+15:])
    # print(f'r0 = {r[0]} et r1 = {r[1]}')
    return r


def write_file(filename, data):
    with open(filename, 'wb') as f:
        print("Fichier à écrire:" + filename)
        f.write(data)


def run(server_ip='10.0.2.15', server_port=1234):
    file_request = input("Entrez le nom du fichier que vous désirez: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Tentative de connection au serveur...")
    client_socket.connect((server_ip, server_port))
    print("Connection au serveur réussit.")
    print()
    print("Envoie de la requete au serveur")
    send_message(client_socket, form_request(file_request, server_ip, server_port,
                                             "gzip", "Python/3.8.10", "0").encode(VERSION_ENCODE))
    response_request = receive_message(client_socket)
    r = analyse_response(response_request.decode(VERSION_ENCODE))
    if r[0] == "200 OK":
        d = zlib.decompressobj()
        message = d.decompress(receive_all(client_socket, int(r[1])))
        write_file(file_request, message)
        print("Ecriture du fichier recu dans le storage")
    else:
        print(r[0])
    client_socket.close()
    print("Communication avec le serveur terminé")


if __name__ == '__main__':
    run()
