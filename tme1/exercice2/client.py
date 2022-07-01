import socket
import struct
import datetime
import random
import time

VERSION_ENCODE = 'utf-8'
BUFFER_SIZE = 1024


def diff_time(time_begin, time_end):
    r = 0
    h = 0
    m = 0
    try:
        milliseconds = int(time_end[9:]) - int(time_begin[9:])
        if milliseconds < 0:
            milliseconds *= -1
        seconds = int(time_end[6:8]) - int(time_begin[6:8])
        if seconds < 0:
            seconds += 60
            m = 1
        minutes = int(time_end[3:5]) - int(time_begin[3:5]) - m
        if minutes < 0:
            minutes += 60
            h = 1
        hours = int(time_end[0:2]) - int(time_begin[0:2]) - h
        if hours < 0:
            hours *= -1
            r = 1
        return [hours, minutes, seconds, milliseconds, r]
    except ValueError:
        return []


def run(server_ip='10.0.2.15', server_port=1236):
    n = 3
    cnt = 0
    while n:
        try:
            cnt = int(input("Entrez le nombre de fois que vous voulez avoir l'heure du serveur: "))
            if cnt < 1:
                cnt = 1
            n = 0
        except ValueError:
            n = n - 1
            if n > 0:
                print("La valeur entré n'est pas un entier. Veuillez essayer à nouveau.")
            else:
                print("Nombre d'essaie atteint. Valeur par défaut = 3")
                cnt = 3
    df = []
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Tentative de connection au serveur...")
    client_socket.connect((server_ip, server_port))
    print("Connection au serveur réussit.")
    print()
    print("Envoie du nombre de fois que l'on veut l'heure du serveur au serveur")
    client_socket.send(struct.pack('>i', cnt))
    for i in range(0, cnt):
        time.sleep(random.random() * 10)
        print(f"Demande n°{i} au serveur...")
        time_send = datetime.datetime.now().time()
        client_socket.send("SEND HOUR".encode(VERSION_ENCODE))
        time_received = client_socket.recv(BUFFER_SIZE).decode(VERSION_ENCODE)
        df.append(diff_time(time_received, str(time_send)))
    client_socket.close()
    print("Communication avec le serveur terminé")
    print()
    return df


if __name__ == '__main__':
    t = run()
    print("Différence d'heure avec le serveur enregistré:")
    for d in t:
        if not d:
            pass
        else:
            print(f"{d[0]}h {d[1]}min {d[2]}s {d[3]}ms")
