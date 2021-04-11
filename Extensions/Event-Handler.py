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
        try:
            await Utils.DBPreconditioning.DEL_Uccount(self, user)
        except:
            pass


    @commands.Cog.listener()
    async def on_member_join(self, user: discord.Member):

        embed = discord.Embed(
            title=f"Hallo {user.name}!",
            colour=discord.Colour(Utils.Farbe.Welcome_Blue),
            description=f"Hallo {user.mention} willkommen auf dem Discord Server:\n**{user.guild.name}** !\nUm Spieler zu suchen, gehe in den Korrespondierenden Kanal,\n"
                        f"die Angepinnte Nachricht oben im Chat erklärt, wie es funktioniert.\n**Viel Spaß!**"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_image(url=user.avatar_url)

        channel = discord.utils.get(user.guild.text_channels, name=str(
            Utils.YamlContainerManagement.get_yamlCGL("Variablen", "SpecifiedChannels", "Welcome").lower()))

        m = await channel.send(embed=embed)

        role = discord.utils.get(user.guild.roles, name=str(Utils.YamlContainerManagement.get_yamlCGL("Variablen", "SpecifiedRoles", "Standart")))
        await user.add_roles(role)

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
