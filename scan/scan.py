from mcstatus import MinecraftServer
import random
import threading

savefile = "found.txt"
threadcount = 1000


def randomip():
	return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


def do():
	while True:
		ip = randomip()
		port = random.randint(0, 65535)
		
		try:
			server = MinecraftServer(ip, 25565)
			status = server.status()
			query = server.query()
			
			# print(status.version.name)
			# print(status.players.online)
			print(
				f"Server found ({ip}:25565) {server.ping()}ms version({status.version.name}) : {', '.join(query.players.names)}")
			with open(savefile, "a+") as f:
				f.write(f"\n{ip}:25565 {status.version.name}")
		except:
			gudfgudfg = 0


# print(f"invalid: {ip}")


for i in range(threadcount):
	t1 = threading.Thread(target=do)
	t1.start()
	print(f"created thread: {str(i + 1)}")
