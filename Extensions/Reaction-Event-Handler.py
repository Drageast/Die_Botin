# Import
from discord.ext import commands
import asyncio
import discord


# Utils
import Utils


# Cog Initialising


class Reaction_EventHandler(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reaction = str(Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Emojis", "Standart", "Accept"))

    async def wait_message(self, user):
        new_message = await self.client.wait_for('message', check=lambda message: message.author == user, timeout=360)

        return new_message

    @commands.Cog.listener()
    async def on_message(self, message):

        if isinstance(message.channel, discord.channel.DMChannel):
            return

        elif message.content.startswith(str(self.client.command_prefix)):
            return

        elif message.channel.name not in Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Channels", "SpielerSuche"):
            return

        elif message.author.bot:
            return
        else:

            await message.add_reaction(self.reaction)
            m = await message.author.send(f"**{message.author.mention} : `Deine Nachricht ist nun als Ticket markiert!`**\n"
                                          f"_Dieses Ticket wird für ungefähr die nächsten 2 Stunden eingebunden, danach wird dieses Abgeschaltet._")
            await asyncio.sleep(10)
            await m.delete()


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if isinstance(reaction.message.channel, discord.channel.DMChannel):
            return

        elif reaction.message.content.startswith(str(self.client.command_prefix)):
            return

        elif reaction.message.channel.name not in Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Channels", "SpielerSuche"):
            return

        elif user.bot:
            return

        elif str(reaction.emoji) != self.reaction:
            return

        else:
            m1 = await user.send("**Bitte schreibe in deiner Nächsten Nachricht an mich, was dein PSN-Name ist.**")

            try:

                response = await self.wait_message(user)

            except asyncio.TimeoutError:
                await m1.delete()
                m2 = await user.send("**Der Vorgang wurde abgebrochen, da du zu lange gebraucht hast!**")
                await reaction.message.remove_reaction(reaction, user)
                await asyncio.sleep(5)
                await m2.delete()
                return

            await m1.delete()

            m2 = await user.send("**Danke für die Übermittlung deines PSN-Namen.\n_Ich habe dich soeben angemeldet._**")

            Data = await Utils.DBPreconditioning.GET_Uccount(self, user)

            await asyncio.sleep(1.5)

            embed = discord.Embed(
                title="Jemand hat sich Angemeldet!",
                colour=discord.Color(Utils.Farbe.Light_Blue),
                description=f"Der Discord-Nutzer: `{user.name}` hat sich mit dem PSN-Namen: `{response.content}` angemeldet."
            )
            if Data.Reports != 0:
                embed.add_field(name="Achtung!", value=f"Der Nutzer wurde schon `{Data.Reports}` - mal gemeldet!")

            m3 = await reaction.message.author.send(embed=embed)
            await asyncio.sleep(10)
            await m2.delete()
            await asyncio.sleep(10)
            await m3.delete()


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        if isinstance(reaction.message.channel, discord.channel.DMChannel):
            return

        elif reaction.message.content.startswith(self.client.command_prefix):
            return

        elif reaction.message.channel.name not in Utils.YamlContainerManagement.GET_yamlAttr("Variablen", "Universals", "Channels", "SpielerSuche"):
            return

        elif user.bot:
            return

        elif str(reaction.emoji) != self.reaction:
            return

        else:
            m1 = await user.send("**Ich habe dich bei dieser Aktivität ausgetragen!**")

            embed = discord.Embed(
                title="Jemand hat sich Abgemeldet!",
                colour=discord.Color(Utils.Farbe.Light_Blue),
                description=f"Der Discord-Nutzer: `{user.name}` hat sich abgemeldet."
            )

            m2 = await reaction.message.author.send(embed=embed)

            await asyncio.sleep(10)
            await m1.delete()
            await asyncio.sleep(10)
            await m2.delete()


    @commands.command()
    async def Report(self, ctx, user: discord.Member):

        await Utils.DBPreconditioning.POST_Uccount(self, user, Reports=1)

        embed = discord.Embed(
            title="Report",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"Der Spieler: **{user.name}** wurde erfolgreich gemeldet.\n_Danke, dass du die Community sauber hältst!_"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.TimeSend.se_ctx(ctx, embed, 10)


    # Cog Finishing


def setup(client):
    client.add_cog(Reaction_EventHandler(client))
