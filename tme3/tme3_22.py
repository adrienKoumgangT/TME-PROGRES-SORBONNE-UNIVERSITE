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
			result = " -> ".join(list_ip)
			is_find = False
			result_grep = run(["grep", "-e", result, file_name], capture_output=True).stdout.decode('utf-8')
			if not result_grep:
				print(result)
				with open(file_name, "a") as f:
					f.write(result + "\n")
		time.sleep(pause)

run_traceroute()
