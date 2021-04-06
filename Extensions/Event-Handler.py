# Import
from discord.ext import commands
import discord
import asyncio

# Utils
import Utils

# Cog Initialising


class EventHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, user: discord.Member):

        x = self.client.ticket.find_one({"_id": user.id})

        if x is None:
            pass
        else:
            await Utils.Ticket.delete_Ticket(self, user)

    @commands.Cog.listener()
    async def on_member_join(self, user: discord.Member):

        embed = discord.Embed(
            title=f"Hallo {user.name}!",
            colour=discord.Colour(Utils.Farbe.Welcome_Blue),
            description=f"Hallo {user.mention} willkommen auf dem Discord Server:\n**{user.guild.name}** !\nUm Spieler zu suchen, gebe `!ct` in einem Kanal ein, "
                        f"der Commands Akzeptiert. Um ein Ticket vorzeitig zu löschen, gebe `!dt` ein. Der Rest ist selbsterklärend.\nJe nach dem, was du suchst, "
                        f"schaue in der Kategorie: _Spielersuche_ nach der gewünschten Aktivität in den Reitern. Um bei einer Aktivität teilzunehmen, drücke auf die Reaktion (✅). "
                        f"Der Rest ist wieder selbsterklärend.\n**Viel Spaß!**"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_image(url=user.avatar_url)

        channel = discord.utils.get(user.guild.text_channels, name=str(Utils.YamlContainerManagement.get_yamlCGL("Variablen", "SpecifiedChannels", "Welcome").lower()))

        m = await channel.send(embed=embed)
        await asyncio.sleep(300)
        try:
            await m.delete()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        embed = discord.Embed(
            title="Hallo!",
            colour=discord.Colour(Utils.Farbe.Welcomer_Blue),
            description=f"Hallo {guild.default_role.mention}! Ich bin **{self.client.user.name}**.\nIch bin der Discord Bot von [DrageastLP](https://github.com/Drageast).\n"
                        f"Ich wurde extra für diesen Server geschrieben und freue ich schon, euch zu assistieren."
        )
        embed.set_image(url=self.client.user.avatar_url)

        await guild.text_channels[0].send(embed=embed)

# Cog Finishing


def setup(client):
    client.add_cog(EventHandler(client))
