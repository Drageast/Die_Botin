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
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            return

        elif after.channel.id == Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "SpecifiedChannels", "SupportChannelVOICE") and not member.bot:

            channel = await self.client.fetch_channel(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "SpecifiedChannels", "AdminChat"))

            role1 = discord.utils.get(member.guild.roles, name=str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Roles", "ServerTeam", "Owner")))
            role2 = discord.utils.get(member.guild.roles, name=str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Roles", "ServerTeam", "Administrator")))
            role3 = discord.utils.get(member.guild.roles, name=str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Roles", "ServerTeam", "Developer")))

            embed = discord.Embed(
                title="Support Anfrage:",
                colour=discord.Colour(Utils.Farbe.Orange),
                description=f"**{role1.mention}/{role2.mention}/{role3.mention}**\nDer User: `{member.name}` wartet in dem Sprachkanal: `{after.channel.name}`."
            )
            embed.set_thumbnail(url=member.avatar_url)

            m = await channel.send(embed=embed)
            await asyncio.sleep(120)
            await m.delete()

        else:
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
            Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "SpecifiedChannels", "Welcome").lower()))

        m = await channel.send(embed=embed)

        role = discord.utils.get(user.guild.roles, name=str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Roles", "Standart")))
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
