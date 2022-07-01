from subprocess import run
import time


def run_traceroute(adress_ip: str = "www.google.com", file_name: str = "traceroute.txt", pause: int = 5):
	with open(file_name, "w") as f:
		f.write("Trace route for " + adress_ip + ":\n")
	while True:
		result_traceroute = run(['traceroute', "-n", adress_ip], capture_output=True).stdout.decode('utf-8')
		# print(f"traceroute == {result_traceroute}")
		list_lines = result_traceroute.split("\n")
		list_ip = []
		for i in range(1, len(list_lines)-1):
			line = list_lines[i]
			list_elem = line.split()
			# print(list_elem)
			if len(list_elem) > 0:
				ip_add = list_elem[1]
			list_ip.append(ip_add)
		if len(list_ip) > 0:
			result = "   ".join(list_ip)
			is_find = False
			with open(file_name, "r") as f:
				line_in_file = f.readline()
				while line_in_file and not is_find:
					if list_ip == line_in_file.split():
						is_find = True
					line_in_file = f.readline()
			if not is_find:
				print(result)
				with open(file_name, "a") as f:
					f.write(result + "\n")
		time.sleep(pause)


if __name__ == '__main__':
	adress = "www.google.com"
	file_name = "traceroute.txt"
	pause = 5
	has_help = False
	if len(sys.argv) > 1:
		for i in range(1, len(sys.argv)):
			one_arg = sys.argv[i].split("=")
			if one_arg[0] == "-help":
				has_help = True
				print(f"syntax: {sys.argv[0]} -help -adress=x -file=y -pause=z\n"
					  f"\t -help: affiche la syntax d'utilisation avec les options\n"
					  f"\t -adress=x: x = adress_ip (nom logique) dont on recherche la route (default: www.google.com)\n"
					  f"\t -file=y: y = fichier où sauvegarder les adresses ip (default: traceroute.txt)\n"
					  f"\t -pause=z: z = durée d'attente entre les requetes (en secondes) (default: 5 secondes)")
			elif one_arg[0] == "-adress":
				if one_arg[1]:
					adress = one_arg[1]
				else:
					print("Nom logique non valide")
			elif one_arg[0] == "-file":
				if one_arg[1]:
					file_name = one_arg[1]
				else:
					print("Nom de fichier non valide")
			elif one_arg[0] == "-pause":
				if one_arg[1]:
					try:
						pause = int(one_arg[1])
					except Exception:
						print(f"Valeur {one_arg[1]} pour l'argument pause non valide")
						pause = 5
				else:
					print("Valeur de pause non valide")
			else:
				print(f"Argument {sys.argv[i]} non reconnu!")

	if has_help:
		exit(0)
	run_traceroute(adress_ip=adress, file_name=file_name, pause=pause)
