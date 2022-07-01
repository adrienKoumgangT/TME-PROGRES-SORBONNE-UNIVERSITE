import socket
import random

BUFFER_SIZE = 1024

server_port = 1234


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', server_port))

    print('server ready\n\n')
    while True:
        message_received, client_ip = server_socket.recvfrom(BUFFER_SIZE)
        print(f"Message reçu par le client d'address ip '{client_ip}'")
        random.seed()
        if random.randint(0, 1) == 0:
            print("Pas de réponse généré pour le client")
            print()
            continue
        server_socket.sendto("message from server to client".encode('utf-8'), client_ip)
        print(f"Message envoyé au client d'address ip '{client_ip}'")
        print()


if __name__ == '__main__':
    run()
