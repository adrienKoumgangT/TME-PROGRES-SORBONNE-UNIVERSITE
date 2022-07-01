from subprocess import run
import time
import sys


def run_dig(name_adress: str = "www.google.com", file_name: str = "dig.txt", pause: int = 5):
	with open(file_name, "w") as file_out:
		file_out.write(f"IP address of {name_adress}:\n")
	while True:
		result_dig = run(['dig', '+short', name_adress], capture_output=True).stdout.decode('utf-8')
		# print(f"result dig = {result_dig}")
		list_ip = result_dig.split("\n")
		for adr_ip in list_ip:
			if not adr_ip:
				continue
			result_grep = run(["grep", "-e", adr_ip, file_name], capture_output=True).stdout.decode('utf-8')
			# print(f"result grep == {result_grep}")
			if not result_grep:
				print("adress ip of " + name_adress + " : " + adr_ip)
				with open(file_name, "a") as file_out:
					file_out.write(adr_ip + "\n")
		time.sleep(pause)

if __name__ == '__main__':
	adress = "www.google.com"
	file_name = "dig.txt"
	pause = 5
	has_help = False
	if len(sys.argv) > 1:
		for i in range(1, len(sys.argv)):
			one_arg = sys.argv[i].split("=")
			if one_arg[0] == "-help":
				has_help = True
				print(f"syntax: {sys.argv[0]} -help -adress=x -file=y -pause=z\n"
					  f"\t -help: affiche la syntax d'utilisation avec les options\n"
					  f"\t -adress=x: x = nom de logique dont on recherche les adresses ip (default: www.google.com)\n"
					  f"\t -file=y: y = fichier où sauvegarder les adresses ip (default: dig.txt)\n"
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
	run_dig(name_adress=adress, file_name=file_name, pause=pause)
