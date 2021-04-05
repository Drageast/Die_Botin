# Import
from discord.ext import commands
import asyncio
import discord

# Utils
import Utils

# Cog Initialising


class TicketSystem(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def wait_message(self, ctx):
        new_message = await self.client.wait_for('message', check=lambda message: message.author == ctx.author,
                                                 timeout=120.0)

        return new_message

    @commands.guild_only()
    @commands.command(aliases=["cticket"])
    async def createTicket(self, ctx):

        await ctx.message.delete()
        Vorhut = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Vorhut")
        Schmelztiegel = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Schmelztiegel")
        Gambit = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Gambit")
        Raid = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Raid")

        embed = discord.Embed(
            title="Ticket",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"Bitte klicke unten auf das Symbol, passend zu der Aktivität.\n({Raid}) **Raid**, ({Vorhut}) **Vorhut**, ({Gambit}) **Gambit**, ({Schmelztiegel}) **Schmelztiegel**"
        )

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [Vorhut, Schmelztiegel, Gambit, Raid]

        m1 = await ctx.send(embed=embed)
        await m1.add_reaction(Raid)
        await m1.add_reaction(Vorhut)
        await m1.add_reaction(Gambit)
        await m1.add_reaction(Schmelztiegel)

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)

            choice = "vorhut" if str(reaction.emoji) == Vorhut else ("schmelztiegel" if str(reaction.emoji) == Schmelztiegel else ("gambit" if str(reaction.emoji) == Gambit else "raid"))

        except asyncio.TimeoutError:
            try:
                await m1.delete()
            except:
                pass
            return

        embed = discord.Embed(
            title="Ticket",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description="Benenne nun in einer neuen Nachricht, **für welche Aktivität du Spieler suchst**.\nBeispiel: *Tiefsteinkrypta*"
        )
        await m1.edit(embed=embed)
        await m1.clear_reactions()

        try:

            r1 = await self.wait_message(ctx)
            await r1.delete()
        except asyncio.TimeoutError:
            try:
                await m1.delete()
            except:
                pass
            return

        embed = discord.Embed(
            title="Ticket",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"Benenne nun in einer neuen Nachricht, **wie viele Spieler du benötigst**.\nBeispiel: *3*"
        )
        await m1.edit(embed=embed)

        try:

            r2 = await self.wait_message(ctx)
            await r2.delete()
        except asyncio.TimeoutError:
            try:
                await m1.delete()
            except:
                pass
            return

        embed = discord.Embed(
            title="Ticket",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"Benenne nun in einer neuen Nachricht, **was deine Beschreibung dazu ist.** _Du kannst zusätzlich eine Uhrzeit anhängen, wann das event stattfinden,_"
                        f"_soll. Dazu Füge nach der Beschreibung ein `= Uhrzeit` ein._\nBeispiel: *Tiefsteinkrypta Fresh mit Erfahrung = 13:00*"
        )
        await m1.edit(embed=embed)

        try:

            r3 = await self.wait_message(ctx)
            await r3.delete()
        except asyncio.TimeoutError:
            try:
                await m1.delete()
            except:
                pass
            return

        # Textverarbeitung

        inhalt = r3.content

        if "=" in inhalt:
            inhalt1, inhalt2 = inhalt.split("=")

            if inhalt2.endswith("Uhr" or "uhr"):
                inhaltUhrzeit = inhalt2
            else:
                inhaltUhrzeit = f"{inhalt2}Uhr"
        else:
            inhaltUhrzeit = None

        response1 = inhalt1 if inhaltUhrzeit is not None else r1.content

        data = await Utils.Ticket.create_Ticket(self, ctx.author, r1.content, int(r2.content), response1, 1)


        embed = discord.Embed(
            title=f"Spieler suche: {r1.content}",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"{response1}"
        )
        embed.add_field(name="Benötigte Spieler:", value=f"{r2.content}")
        embed.set_footer(text=f"Gesucht von: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        if inhaltUhrzeit is not None:
            embed.add_field(name="Startzeit:", value=f"{inhaltUhrzeit}")

        message = await Utils.ChannelSending.get_channel(ctx.author, embed, choice)
        await message.add_reaction("✅")
        await asyncio.sleep(1)

        await m1.delete()

        await Utils.Ticket.edit_Ticket(self, ctx.author, message.id, 1)
        await Utils.Ticket.edit_Ticket(self, ctx.author, message.channel.id, 2)

        await Utils.TicketReactor.ListenAndReact(self, ctx, ctx.author)

    @commands.guild_only()
    @commands.command(aliases=["dticket"])
    async def deleteTicket(self, ctx):

        data = await Utils.Ticket.get_Ticket(self, ctx.author)
        await ctx.message.delete()

        if data["IDs"]["MessageID"] is None or data["IDs"]["ChannelID"] is None or data["IDs"]["MessageID"] == data["IDs"]["ChannelID"]:
            await Utils.Ticket.delete_Ticket(self, ctx.author)

        else:

            messageID = data["IDs"]["MessageID"]
            channelid = data["IDs"]["ChannelID"]

            channel = self.client.get_channel(channelid)
            m = await channel.fetch_message(messageID)

            try:
                await m.delete()
            except:
                pass
            await Utils.Ticket.delete_Ticket(self, ctx.author)

# Cog Finishing


def setup(client):
    client.add_cog(TicketSystem(client))
