from subprocess import run


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
        nb = (2 ** (32 - masque)) - 2
        return nb
    elif ad_ip and mask:
        cidr = get_cidr(ad_ip=ad_ip, mask=mask)
        return num_machine(cidr=cidr)


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


def add_n_address(addr_ip, n):
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
    sub_net = get_subnet_address(cidr)
    nm = num_machine(cidr)
    first_addr = add_n_address(sub_net, 1)
    last_addr = add_n_address(sub_net, nm)
    if last_addr == "255.255.255.255":
        return first_addr, "255.255.255.254", "255.255.255.255"
    else:
        broadcast_addr = add_n_address(sub_net, nm+1)
        return first_addr, last_addr, broadcast_addr


def run_ping(adress_ip: str = "172.23.234.47", masque: str = "255.255.240.0"):
    cidr_addr = get_cidr(ad_ip=adress_ip, mask=masque)
    first_addr, last_addr, broadcast_addr = get_info_network(cidr=cidr_addr)
    ip_adress = first_addr
    result_ping = ""
    while ip_adress != broadcast_addr:
        result = run(['ping', '-c', '1', ip_adress], capture_output=True).stdout.decode('utf-8')
        result_ping += result
        print(result)
        ip_adress = add_n_address(addr_ip=ip_adress, n=1)
    with open('res_ping.txt', 'w') as file_out:
        file_out.write(result_ping)


if __name__ == '__main__':
	run_ping()
