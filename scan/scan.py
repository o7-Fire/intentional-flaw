from mcstatus import JavaServer
import random
import threading
import time

savefile = "found.txt"
threadcount = 2000


def randomip():
	return f"{random.randint(0, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

while True:
	def do():
		ip = randomip()
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
			
	if threading.active_count() < threadcount:
		try:
			t1 = threading.Thread(target=do)
			t1.start()
		except:
			time.sleep(1)
	else:
		time.sleep(1)
