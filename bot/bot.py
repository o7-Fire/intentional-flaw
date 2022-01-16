from mcstatus import MinecraftServer
import random
import threading
import discord
import os

TOKEN = os.getenv("TOKEN")
datafile = "found.txt"
client = discord.Client()


@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
	# if message.author.bot:
	#	return
	if message.author.id == client.user.id:
		return
	if message.content == "scan random":
		await message.channel.send("scanning . . .")
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

	if message.content == "scan all":
		with open(datafile, "r") as f:
			randomips = f.read().split("\n")
		for randomip in randomips:
			randomipt = randomip.split(" ")[0]
			ip = randomipt.split(":")[0]
			port = randomipt.split(":")[1]
			try:
				# print(ip, port)
				server = MinecraftServer(ip, int(port))
				server.status()
				server.ping()
				with open("online.txt", "a+") as f:
					f.write(f"\n{randomip}")
			except:
				ignorethisvaluelol = 0
			
	
client.run(TOKEN)
