from mcstatus import MinecraftServer
import random
import threading
import discord
import os
import time

TOKEN = os.getenv("TOKEN")
datafile = "found.txt"
threadlimit = 500
client = discord.Client()


@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

totalonline = 0
@client.event
async def on_message(message):
	global totalonline
	# if message.author.bot:
	#	return
	if message.author.id == client.user.id:
		return
	if message.content == "scan random":
		await message.channel.send("pinging . . .")
		Active = True
		
		while Active:
			with open(datafile, "r") as f:
				randomip = random.choice(f.read().split("\n")).split(" ")[0]
			ip = randomip.split(":")[0]
			port = randomip.split(":")[1]
			server = MinecraftServer(ip, int(port))
			try:
				# print(ip, port)
				status = server.status()
				query = server.query()
				#ping = str(server.ping()).split(".")[0]
				
				embedVar = discord.Embed(title=f"{ip}:{port} ({query.players.online} Online)", description=f"{query.motd}",
				                         color=0x00ff00)
				#embedVar.add_field(name="Ping", value=f" {ping}ms", inline=False)
				if len(query.players.names) == 0:
					embedVar.add_field(name="Players", value=f"None", inline=False)
				else:
					embedVar.add_field(name="Players", value=f"{', '.join(query.players.names)}", inline=False)
				embedVar.add_field(name="Version", value=f"{status.version.name}", inline=False)
				await message.channel.send(embed=embedVar)
				Active = False
			except Exception as e:
				ignorethisvaluelol = 0
				#await message.channel.send("offline")
				#embedVar = discord.Embed(title=f"{ip}:{port} (0 Online)", description=f"Offline", color=0x00ff00)
				#embedVar.add_field(name=f"Error", value=f"{e}", inline=False)
				#await message.channel.send(embed=embedVar)
	
	if message.content == "scan online":
		Active = True
		
		while Active:
			with open("online.txt", "r") as f:
				randomip = random.choice(f.read().split("\n")).split(" ")[0]
			ip = randomip.split(":")[0]
			port = randomip.split(":")[1]
			server = MinecraftServer(ip, int(port))
			try:
				# print(ip, port)
				status = server.status()
				query = server.query()
				# ping = str(server.ping()).split(".")[0]
				
				embedVar = discord.Embed(title=f"{ip}:{port} ({query.players.online} Online)",
				                         description=f"{query.motd}",
				                         color=0x00ff00)
				# embedVar.add_field(name="Ping", value=f" {ping}ms", inline=False)
				if len(query.players.names) == 0:
					embedVar.add_field(name="Players", value=f"None", inline=False)
				else:
					embedVar.add_field(name="Players", value=f"{', '.join(query.players.names)}", inline=False)
				embedVar.add_field(name="Version", value=f"{status.version.name}", inline=False)
				await message.channel.send(embed=embedVar)
				Active = False
			except Exception as e:
				ignorethisvaluelol = 0
				# await message.channel.send("offline")
				# embedVar = discord.Embed(title=f"{ip}:{port} (0 Online)", description=f"Offline", color=0x00ff00)
				# embedVar.add_field(name=f"Error", value=f"{e}", inline=False)
				# await message.channel.send(embed=embedVar)
			
	if message.content == "scan all":
		with open(datafile, "r") as f:
			ips = f.read().split("\n")
		total = len(ips)
		totalonline = 0
		for randomip in ips:
			done = False
			while done == False:
				def do():
					global totalonline
					randomipt = randomip.split(" ")[0]
					ip = randomipt.split(":")[0]
					port = randomipt.split(":")[1]
					try:
						# print(ip, port)
						server = MinecraftServer(ip, int(port))
						server.status()
						server.ping()
						totalonline += 1
						try:
							with open("online.txt", "r") as f:
								os.remove("online.txt")
						except:
							ignorethisvaluelol = 0
						with open("online.txt", "a+") as f:
							f.write(f"{randomip}\n")
					except Exception as e:
						ignorethisvaluelol = 0
				if threading.active_count() < threadlimit:
					t1 = threading.Thread(target=do)
					t1.start()
					done = True
				else:
					time.sleep(0.1)
		await message.channel.send(f"Finished scanning\nTotal servers: {total}\nServers online: {totalonline}\nServers offline: {total - totalonline}")
				
			
	
client.run(TOKEN)
