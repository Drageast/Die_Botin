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
                                                 timeout=360)

        return new_message

    @commands.guild_only()
    @commands.command(aliases=["ct"])
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

            choice = "Vorhut" if str(reaction.emoji) == Vorhut else ("Schmelztiegel" if str(reaction.emoji) == Schmelztiegel else ("Gambit" if str(reaction.emoji) == Gambit else "Raid"))

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
                        f"soll. Dazu Füge nach der Beschreibung ein `= Uhrzeit` ein._\nBeispiel: *Tiefsteinkrypta Fresh mit Erfahrung = 13:00*"
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

        response1 = inhalt1 if inhaltUhrzeit is not None else r3.content
        colour = Utils.Farbe.TezzQu if ctx.author.id == "336549722464452620" else Utils.Farbe.Light_Blue

        data = await Utils.Ticket.create_Ticket(self, ctx.author, choice, int(r2.content), response1, 2)


        embed = discord.Embed(
            title=f"Spieler suche: {choice}",
            colour=discord.Colour(colour),
            description=f"{data.activity}"
        )
        embed.add_field(name="Benötigte Spieler:", value=f"{data.NeededParticipants}")
        embed.set_footer(text=f"Gesucht von: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        if inhaltUhrzeit is not None:
            embed.add_field(name="Startzeit:", value=f"{inhaltUhrzeit}")

        message = await Utils.ChannelSending.get_channel(ctx.author, embed, choice.lower())
        await message.add_reaction("✅")
        await asyncio.sleep(1)

        await m1.delete()

        await Utils.Ticket.edit_Ticket(self, ctx.author, message.id, 1)
        await Utils.Ticket.edit_Ticket(self, ctx.author, message.channel.id, 2)

        await Utils.TicketReactor.ListenAndReact(self, ctx, ctx.author)

    @commands.guild_only()
    @commands.command(aliases=["dt"])
    async def deleteTicket(self, ctx):

        data = await Utils.Ticket.get_Ticket(self, ctx.author)
        await ctx.message.delete()

        if data.MID is None or data.CID is None:
            await Utils.Ticket.delete_Ticket(self, ctx.author)

        else:

            channel = self.client.get_channel(data.CID)
            m = await channel.fetch_message(data.MID)

            try:
                await m.delete()
            except:
                pass
            await Utils.Ticket.delete_Ticket(self, ctx.author)


# Cog Finishing


def setup(client):
    client.add_cog(TicketSystem(client))
