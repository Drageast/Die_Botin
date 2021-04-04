# Imports
import discord
from discord.ext import commands
from pymongo import MongoClient
import os
# Utils
import Utils

#  Erstellen des Client für discord

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(command_prefix=Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "Prefix"),
                                 intents=intents,
                                 case_insensitive=True)


# MongoDB Initialisierung / Benachrichtigung sobald der Bot Online.


@client.listen()
async def on_ready():
    client.connection_url = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "MongoDB")

    await client.change_presence(status="", activity=discord.Game(""))
    client.mongo = MongoClient(str(client.connection_url))
    client.ticket = client.mongo["Die_Botin"]["Tickets"]
    print(f'DATENBANK AKTIV\n<-->\nONLINE\n<-->\n{client.user}\n<-->')


# Laden der Erweiterungen


x = 0

for filename in os.listdir('Extensions'):
    client.load_extension(f'Extensions.{filename[:-3]}') if filename.endswith(".py") else None
    x += 1
print(f"<-->\nCogs geladen! Anzahl: {x}\n<-->")


# Starten des Client mit dem Token


def token_output():
    data = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "Token")
    return data


client.run(token_output())

