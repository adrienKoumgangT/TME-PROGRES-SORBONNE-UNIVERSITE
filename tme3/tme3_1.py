from subprocess import run
from threading import *
import time
import sys

BASE_HEX = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5",
            "6": "6", "7": "7", "8": "8", "9": "9",
            "a": "10", "b": "11", "c": "12", "d": "13", "e": "14", "f": "15",
            "10": "a", "11": "b", "12": "c", "13": "d", "14": "e", "15": "f"}


def convert_base_ten_to_b(number: int, base: int = 2) -> str:
    """
    Méthode qui me permet de convertir un nombre de base 10
    vers une base b (par défaut b = 2)
    """
    if number <= 0 or base <= 1:
        return ""
    remains = []
    dividende = number
    while dividende != 0:
        rest = dividende % base
        remains.append(BASE_HEX[str(rest)])
        dividende //= base
    remains.reverse()
    return "".join(remains)


def convert_base_b_to_ten(number: str, base: int = 2) -> int:
    """
    Méthode qui me permet de convertir un nombre
    d'une base b (par défaut b = 2) vers la base 10.
    """
    if not number:
        raise Exception("Invalid number")
    if base <= 1:
        raise Exception("The base must be greater than 1")
    lists = []
    for symbol in number:
        lists.append(symbol)
    lists.reverse()
    valeur = 0
    for i in range(0, len(lists)):
        valeur += int(BASE_HEX[lists[i]]) * (base ** i)
    return valeur


def convert_base_b1_to_b2(number: str, base1: int, base2: int) -> str:
    return convert_base_ten_to_b(number=convert_base_b_to_ten(number=number, base=base1), base=base2)


def count_one(number: str):
    if not number:
        return 0
    count = 0
    for bit in number:
        if int(bit) == 1:
            count += 1
    return count


def inverse_nombre(number):
    if number == 255:
        return 0
    if number == 0:
        return 255
    nb = convert_base_ten_to_b(number=number, base=2)
    ni = ""
    for bit in nb:
        if bit == "0":
            ni += "1"
        else:
            ni += "0"
    return convert_base_b_to_ten(number=ni, base=2)


def inverse_masque(masque):
    m = masque.split(".")
    s = []
    for elem in m:
        s.append(str(inverse_nombre(int(elem))))
    return ".".join(s)


def get_cidr(ad_ip, mask):
    """
    Fonction qui à partir de l' adresse ip et du masque, retourner l' adresse sous forme cidr
    :param ad_ip: l' adresse ip
    :param mask: le masque de l' adresse ip
    :return: l' adresse ip et le masque sous forme cidr
    """
    s = mask.split(".")
    one = 0
    for elem in s:
        if int(elem) != 0:
            r = convert_base_ten_to_b(number=int(elem), base=2)
            one += count_one(r)
    return ad_ip + "/" + str(one)


def get_ip_masque(cidr):
    """
    Fonction qui à partir d' une adresse sous forme cidr, retourne l' adresse ip et le masque de cet adresse
    :param cidr: l' adresse
    :return: (ip, mask)
    """
    if not cidr:
        return ()
    ip_masque = cidr.split("/")
    ad_ip = ip_masque[0]
    masque = int(ip_masque[1])
    if masque == 32:
        return ad_ip, "255.255.255.255"
    elif masque == 24:
        return ad_ip, "255.255.255.0"
    elif masque == 16:
        return ad_ip, "255.255.0.0"
    elif masque == 8:
        return ad_ip, "255.0.0.0"
    elif masque == 0:
        return ad_ip, "0.0.0.0"
    mask = ""
    # premier set de bit 255.-.-.-
    for i in range(0, 4):
        if masque == 0:
            mask += "0"
        elif masque >= 8:
            mask += "255"
            masque -= 8
        elif masque != 0:
            bit_number = "1" * masque
            bit_number += "0" * (9 - masque)
            bit_number = bit_number[:len(bit_number) - 1]
            num = convert_base_b_to_ten(number=bit_number, base=2)
            mask += str(num)
            masque = 0
        if i != 3:
            mask = mask + "."
    return ad_ip, mask


def num_machine(cidr: str, ad_ip: str = None, mask: str = None):
    """
    Fonction qui calcule le nombre de machine que l' on peut connecter à un sous-réseau
    :param cidr: adresse de sous-réseau sous forme cidr
    :param ad_ip: adresse ip
    :param mask: mask
    :return: le nombre de machine du sous-réseau
    """
    if cidr:
        masque = int(cidr.split("/")[1])
        # le nombre est égal au nombre d'adresse du sous-réseau (2^(32 - masque)) moins 2 (on retire l'adresse du sous-réseau et celle de broadcast)
        nb = (2 ** (32 - masque)) - 2
        return nb
    elif ad_ip and mask:
        cidr = get_cidr(ad_ip=ad_ip, mask=mask)
        return num_machine(cidr=cidr)
    else:
        return -1


def get_subnet_address(cidr: str = None, ad_ip: str = None, mask: str = None):
    if not cidr and not ad_ip and not mask:
        return ""
    if cidr:
        (ip, masque) = get_ip_masque(cidr)
    else:
        ip = ad_ip
        masque = mask
    list_number_ip = ip.split(".")
    list_number_masque = masque.split(".")
    subnet = []
    for i in range(0, 4):
        subnet.append(str(int(list_number_ip[i]) & int(list_number_masque[i])))
    return ".".join(subnet)


def add_n_address(addr_ip: str, n: int):
    if n <= 0:
        return addr_ip
    list_number_in_ip = addr_ip.split(".")
    fourth_n = int(list_number_in_ip[3]) + n
    if fourth_n <= 255:
        return ".".join([list_number_in_ip[0], list_number_in_ip[1], list_number_in_ip[2], str(fourth_n)])
    else:
        third_n = (fourth_n // 256) + int(list_number_in_ip[2])
        fourth_n = fourth_n % 256
        if third_n <= 255:
            return ".".join([list_number_in_ip[0], list_number_in_ip[1], str(third_n), str(fourth_n)])
        else:
            second_n = (third_n // 256) + int(list_number_in_ip[1])
            third_n = third_n % 256
            if second_n <= 255:
                return ".".join([list_number_in_ip[0], str(second_n), str(third_n), str(fourth_n)])
            else:
                first_n = (second_n // 256) + int(list_number_in_ip[0])
                second_n = second_n % 256
                if first_n <= 255:
                    return ".".join([str(first_n), str(second_n), str(third_n), str(fourth_n)])
                else:
                    return "255.255.255.255"


def get_info_network(cidr):
    # obtention de l'adresse de sous-réseau
    sub_net = get_subnet_address(cidr)
    nm = num_machine(cidr)
    first_addr = add_n_address(sub_net, 1)
    last_addr = add_n_address(sub_net, nm)
    if last_addr == "255.255.255.255":
        return first_addr, "255.255.255.254", "255.255.255.255", nm
    else:
        broadcast_addr = add_n_address(sub_net, nm+1)
        return first_addr, last_addr, broadcast_addr, nm


def run_ping(first_addr: str, last_addr: str, file_name: str):
    ip_adress = first_addr
    result_ping = ""
    # création du fichier résultat
    with open(file_name, 'w') as file_out:
        file_out.write('')
    
    while ip_adress != last_addr:
        result_ping = run(['ping', '-c', '1', ip_adress], capture_output=True).stdout.decode('utf-8')
        # si le ping a eu succès, écriture de l'adresse ip dans le fichier résultat
        if '1 received' in result_ping:
            print(result_ping)
            with open(file_name, 'a') as file_out:
                file_out.write(ip_adress + "\n")
        ip_adress = add_n_address(addr_ip=ip_adress, n=1)


if __name__ == '__main__':
    ip = "10.188.241.28"
    masque = "255.255.0.0"
    n_thread = 5
    has_help = False
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            one_arg = sys.argv[i].split("=")
            if one_arg[0] == "-help":
                has_help = True
                print(f"syntax: {sys.argv[0]} -help -ip=x -masque=y\n"
                      f"\t -help: affiche la syntax d'utilisation avec les options\n"
                      f"\t -ip=x: x = adresse ip de la machine concerné (default: 10.188.241.28)\n"
                      f"\t -masque=y: y = masque associé à l'adresse ip concerné (default: 255.255.0.0)\n"
                      f"\t -nthread=z: z = numero de thread créer pour gérer en parallèle les ping (default: 5 threads)")
            elif one_arg[0] == "-ip":
                if one_arg[1]:
                    ip = one_arg[1]
                else:
                    print("Nom logique non valide")
            elif one_arg[0] == "-masque":
                if one_arg[1]:
                    masque = one_arg[1]
                else:
                    print("Nom de fichier non valide")
            elif one_arg[0] == "-nthread":
                if one_arg[1]:
                    try:
                        n_thread = int(one_arg[1])
                    except Exception:
                        print(f"Valeur {one_arg[1]} pour l'argument nthread non valide")
                        n_thread= 5
                else:
                    print("Valeur de pause non valide")
            else:
                print(f"Argument {sys.argv[i]} non reconnu!")

        if has_help:
            exit(0)
    else:
        print(f"Valeur par défaut:\n"
              f"ip address = {ip}\n"
              f"masque = {masque}\n"
              f"nthread = {n_thread}")
    if 0 > n_thread > 5:
        print("\nNumero de threads > 5: réinitialisation à 5 (nthread = 5)\n")
    cidr_addr = get_cidr(ad_ip=ip, mask=masque)
    first_addr, last_addr, broadcast_addr, n_mach = get_info_network(cidr=cidr_addr)
    if n_thread == 1:
	    run_ping(first_addr=first_addr, last_addr=broadcast_addr, file_name="ping.txt")
    else:
        n = n_mach // n_thread
        n_add = n
        f_address = first_addr
        T = []
        # Création de n_thread pour gérer les différentes requetes ping
        for i in range(n_thread):
            l_address = add_n_address(addr_ip=ip, n=n_add)
            T.append(Thread(target=run_ping, args=(f_address, l_address, "ping"+str(i+1)+".txt")))
            T[i].start()
            n_add += n
            f_address = l_address
        # Attendre la fin de chaque thread
        for i in range(n_thread):
            T[i].join()
        # création du fichier final des résultats des pings
        with open("ping.txt", "w") as f:
            f.write('')
        # écriture des résultats intermédiares dans le fichiers principales
        with open("ping.txt", "a") as f:
            for i in range(n_thread):
                with open("ping"+str(i+1)+".txt", "r") as f2:
                    f.write(f2.read())
