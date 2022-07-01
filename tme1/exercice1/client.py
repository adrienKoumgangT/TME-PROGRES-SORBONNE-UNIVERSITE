import socket
import time
import statistics

BUFFER_SIZE = 1024


def run():
    server_ip = '10.0.2.15'
    server_port = 1234
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Envoie du message au serveur...")
    start = time.time()
    client_socket.sendto("message from client to server".encode('utf-8'), (server_ip, server_port))
    message_received, server_ip = client_socket.recvfrom(BUFFER_SIZE)
    done = time.time()
    print(f"Envoie et reception de paquet au serveur à l'adress '{server_ip}.{server_port}"
          f"avec une durée de temps = {done-start} secondes")
    client_socket.close()
    return done - start


if __name__ == '__main__':
    count = 0
    tmp = []
    while True:
        cnt = int(input("Entrez '1' pour envoyer un message au serveur et '0' pour sortir: "))
        if cnt == 0:
            break
        tmp.append(run())
        count += 1
    print()
    print("Nombre de message envoyé = " + str(count))
    print("Moyenne des RTT = " + str(statistics.mean(tmp)) + " secondes")
