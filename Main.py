# Imports
import discord
import tweepy
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands, tasks
import aiohttp
from pymongo import MongoClient
import os
# Utils
import Utils

#  Erstellen des Client für discord

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(
    command_prefix=Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "Prefix"),
    intents=intents,
    case_insensitive=True)

# Tweepy

auth = tweepy.OAuthHandler(Utils.YamlContainerManagement.get_yamlCGL("Variablen", "TwitterSide", "API_Key"),
                           Utils.YamlContainerManagement.get_yamlCGL("Variablen", "TwitterSide", "API_SECRET_Key"))
auth.set_access_token(Utils.YamlContainerManagement.get_yamlCGL("Variablen", "TwitterSide", "ACCESS_Token"),
                      Utils.YamlContainerManagement.get_yamlCGL("Variablen", "TwitterSide", "ACCESS_SECRET_Token"))

api = tweepy.API(auth)


# MongoDB Initialisierung / Benachrichtigung sobald der Bot Online.


@client.listen()
async def on_ready():
    client.connection_url = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "MongoDB")
    status = int(Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "Status"))

    choiceStatus = discord.Status.online if status == 1 else discord.Status.do_not_disturb
    choiceActivity = discord.Activity(type=discord.ActivityType.playing,
                                      name="Destiny 2") if status == 1 else discord.Activity(
        type=discord.ActivityType.watching, name="WARTUNGSARBEITEN")

    await client.change_presence(status=choiceStatus, activity=choiceActivity)
    client.mongo = MongoClient(str(client.connection_url))
    client.ticket = client.mongo["Die_Botin"]["Tickets"]
    client.Uccount = client.mongo["Die_Botin"]["Uccount"]
    client.Config = client.mongo["Die_Botin"]["Config"]

    get_twitter.start()
    print(f'DATENBANK AKTIV\n<-->\nONLINE\n<-->\n{client.user}\n<-->\nTwitter API AKTIV\n<-->')


@tasks.loop(minutes=15)
async def get_twitter():
    tweetL = api.user_timeline(id=2431136251, tweet_mode="extended")
    Newest_Tweet_Text = tweetL[0].full_text
    Newest_Tweet_Time = tweetL[0].created_at

    data = client.Config.find_one({"_id": "TwitterAPI"})

    if data["Time"] == Newest_Tweet_Time:

        return

    else:

        client.Config.update_one({"_id": "TwitterAPI"}, {"$set": {"Time": Newest_Tweet_Time}})

        async with aiohttp.ClientSession() as session:
            url = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "Webhook2")
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))

            embed = discord.Embed(
                title="",
                colour=discord.Colour(0x1495e6),
                description=f"[Twitter Link](https://twitter.com/BungieHelp)\n{Newest_Tweet_Text}"
            )
            embed.set_thumbnail(
                url="https://image.api.playstation.com/vulcan/img/rnd/202011/1022/r8FavqFIoXMLSAOasPmKuQQF.jpg")
            embed.set_author(name="@BungieHelp",
                             icon_url="https://pbs.twimg.com/profile_images/1362463058132492289/vNe1WM28_400x400.jpg")

            await webhook.send(username="@BungieHelp",
                               avatar_url=client.user.avatar_url, embed=embed)



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
