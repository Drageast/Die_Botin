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
    async def CreateTicket(self, ctx):

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

        def check1(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [Vorhut, Schmelztiegel, Gambit, Raid]

        m1 = await ctx.send(embed=embed)
        await m1.add_reaction(Raid)
        await m1.add_reaction(Vorhut)
        await m1.add_reaction(Gambit)
        await m1.add_reaction(Schmelztiegel)

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check1)

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
            description=f"Bitte klicke unten auf das Symbol, **passend zu der Anzahl, der benötigten Spieler**."
        )
        await m1.edit(embed=embed)
        await m1.clear_reactions()
        await m1.add_reaction("1️⃣")
        await m1.add_reaction("2️⃣")
        await m1.add_reaction("3️⃣")
        await m1.add_reaction("4️⃣")
        await m1.add_reaction("5️⃣")

        def check2(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check2)

            Anzahl = 1 if str(reaction.emoji) == "1️⃣" else (
                2 if str(reaction.emoji) == "2️⃣" else (
                    3 if str(reaction.emoji) == "3️⃣" else (4 if str(reaction.emoji) == "4️⃣" else 5)))

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
        await m1.clear_reactions()

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

        embed = discord.Embed(
            title=f"Spielersuche",
            colour=discord.Colour(colour),
            description=f"{response1}"
        )
        embed.set_thumbnail(url=Utils.YamlContainerManagement.get_yamlCGL("Bilder", choice))
        embed.add_field(name="Benötigte Spieler:", value=f"{Anzahl}")
        embed.set_footer(text=f"Gesucht von: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        if inhaltUhrzeit is not None:
            embed.add_field(name="Startzeit:", value=f"{inhaltUhrzeit}")

        message = await Utils.ChannelSending.get_channel(ctx.author, embed, choice.lower())
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await message.add_reaction("🛑")
        await asyncio.sleep(1)

        await m1.delete()

        Utils.DBPreconditioning.POST_Ticket(self, ctx.author, RequiredParticipants=Anzahl, ChannelID=message.channel.id, MessageID=message.id)

        await Utils.TicketReactor.ListenAndReact(self, ctx, ctx.author)


    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def Report(self, ctx, user: discord.Member):

        Utils.DBPreconditioning.POST_Uccount(self, user, Reports=1)

        embed = discord.Embed(
            title="Report",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"Der Spieler: **{user.name}** wurde erfolgreich gemeldet.\n_Danke, dass du die Community sauber hältst!_"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await Utils.TimeSend.se_ctx(ctx, embed, 10)


# Cog Finishing


def setup(client):
    client.add_cog(TicketSystem(client))
