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

    async def wait_message2(self, user):
        new_message = await self.client.wait_for('message', check=lambda message: message.author == user,
                                                 timeout=360)

        return new_message

    @commands.guild_only()
    @commands.command(aliases=["ticket"])
    async def CreateTicket(self, ctx, *, Beschreibung):

        await ctx.message.delete()
        Vorhut = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Vorhut")
        Schmelztiegel = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Schmelztiegel")
        Gambit = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Gambit")
        Raid = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "UniversalEmoji", "Raid")

        embed = discord.Embed(
            title="Ticket",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"Bitte klicke unten auf das Symbol, passend zu der Aktivität.\n({Raid}) **Raid**, ({Vorhut}) **Vorhut**, ({Gambit}) **Gambit**, ({Schmelztiegel}) **Schmelztiegel**, (♾) **Sonstiges**"
        )

        def check1(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [Vorhut, Schmelztiegel, Gambit, Raid, "♾"]

        m1 = await ctx.send(embed=embed)
        await m1.add_reaction(Raid)
        await m1.add_reaction(Vorhut)
        await m1.add_reaction(Gambit)
        await m1.add_reaction(Schmelztiegel)
        await m1.add_reaction("♾")

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check1)

            choice = "Vorhut" if str(reaction.emoji) == Vorhut else (
                "Schmelztiegel" if str(reaction.emoji) == Schmelztiegel else (
                    "Gambit" if str(reaction.emoji) == Gambit else (
                        "Raid" if str(reaction.emoji) == Raid else "Sonstiges")))

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

        inhalt = Beschreibung

        if "=" in inhalt:
            inhalt1, inhalt2 = inhalt.split("=")

            if inhalt2.endswith("Uhr" or "uhr"):
                inhaltUhrzeit = inhalt2
            else:
                inhaltUhrzeit = f"{inhalt2}Uhr"
        else:
            inhaltUhrzeit = None

        await m1.delete()
        await asyncio.sleep(2)

        # Variablen umformen

        Description = Beschreibung if inhaltUhrzeit is None else inhalt1
        RequiredParticipants = Anzahl
        StartTime = inhaltUhrzeit
        sender = ctx.author

        colour = Utils.Farbe.TezzQu if ctx.author.id == "336549722464452620" else Utils.Farbe.Light_Blue

        Standart_Embed = discord.Embed(
            title=f"Spielersuche",
            colour=discord.Colour(colour),
            description=f"{Description}"
        )
        if choice != "Sonstiges":
            Standart_Embed.set_thumbnail(url=Utils.YamlContainerManagement.get_yamlCGL("Bilder", choice))

        Control_Embed = discord.Embed(
            title=f"Spielersuche",
            colour=discord.Colour(colour),
            description=f"{Description}"
        )

        if choice != "Sonstiges":
            Control_Embed.set_thumbnail(url=Utils.YamlContainerManagement.get_yamlCGL("Bilder", choice))

        Control_Embed.add_field(name="Benötigte Spieler:", value=f"{RequiredParticipants}")
        Control_Embed.set_footer(text=f"Gesucht von: {ctx.author.name}", icon_url=ctx.author.avatar_url)

        if StartTime is not None:
            Control_Embed.add_field(name="Startzeit:", value=f"{StartTime}")

        message = await Utils.ChannelSending.get_channel_embed(ctx.author, Control_Embed, choice.lower())
        try:
            Utils.DBPreconditioning.POST_Ticket(self, ctx.author, RequiredParticipants=Anzahl,
                                                ChannelID=message.channel.id, MessageID=message.id)
        except Utils.DBPreconditioning as e:
            await message.delete()
            raise Utils.DBPreconditioning(e)

        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await message.add_reaction("⛔")

        _User = []
        _Tag = []
        _Control = []
        x = 0
        m = message

        def Reaction_Check(reaction, user):
            return user and str(reaction.emoji) in ["⛔", "✅", "❌"]

        while x < int(RequiredParticipants):

            reaction, user = await self.client.wait_for("reaction_add", check=Reaction_Check)

            if user.bot:
                return

            elif str(reaction.emoji) == "✅":

                Uccount_Data = Utils.DBPreconditioning.GET_Uccount(self, user)

                if Uccount_Data.TicketEntry is False:

                    embed2 = discord.Embed(
                        title="-Anmeldung-",
                        colour=discord.Colour(Utils.Farbe.Light_Blue),
                        description=f"Der Spieler `{sender.name}` benötigt noch deinen PSN-Namen, Bitte Antworte mir damit."
                    )

                    t = await user.send(embed=embed2)

                    try:

                        r = await self.wait_message2(user)

                    except asyncio.TimeoutError:

                        await m.remove_reaction(reaction, user)
                        await t.delete()

                        return

                    a = "" if Uccount_Data.Reports is None else f"\n_Achtung! Der Spieler wurde schon {Uccount_Data.Reports} mal als Spielverderber gemeldet!_"

                    embed = discord.Embed(
                        title=f"-Anmeldung-",
                        colour=discord.Colour(Utils.Farbe.Light_Blue),
                        description=f"Der Discord-Nutzer : `{user.name}` hat sich mit dem PSN-Namen: `{r.content}` angemeldet.\n{a}"
                    )

                    await sender.send(embed=embed)
                    await t.edit(embed=embed)

                    _User.append(user)
                    _Tag.append(r.content)
                    _Control.append(user.id)

                    Utils.DBPreconditioning.POST_Uccount(self, user, TicketEntry=True)

                    x += 1

                    Standart_Embed = discord.Embed(
                        title=f"Spielersuche",
                        colour=discord.Colour(colour),
                        description=f"{Description}\n_Beigetretene Spieler:_\n"+"\n".join(_Tag)
                    )
                    if choice != "Sonstiges":
                        Standart_Embed.set_thumbnail(url=Utils.YamlContainerManagement.get_yamlCGL("Bilder", choice))

                    await m.edit(embed=Standart_Embed)
                    await asyncio.sleep(4)
                    await t.delete()

                else:

                    await m.remove_reaction(reaction, user)

                    embed2 = discord.Embed(
                        title="Du kannst dich nicht Anmelden!",
                        colour=discord.Colour(Utils.Farbe.Dark_Blue),
                        description=f"Du bist schon in einem Ticket eingetragen!"
                                    f"\nWenn du dies für einen Fehler in der Datenbank hältst, gebe: `!debug bool` ein."
                    )

                    m = await user.send(embed=embed2)
                    await asyncio.sleep(8)
                    await m.delete()

            elif str(reaction.emoji) == "❌":

                if _Control.count(user.id) >= 1:
                    index = int(_Control.index(user.id))
                    del _User[index]
                    del _Tag[index]
                    del _Control[index]

                    embed = discord.Embed(
                        title=f"-Abmeldung-",
                        colour=discord.Colour(Utils.Farbe.Dark_Blue),
                        description=f"Der Discord Nutzer: `{user.name}` hat sich abgemeldet."
                    )

                    l = await sender.send(embed=embed)
                    try:
                        await m.remove_reaction("✅", user)
                        await m.remove_reaction(reaction, user)
                    except:
                        pass

                    Utils.DBPreconditioning.POST_Uccount(self, user)

                    x -= 1

                    Standart_Embed = discord.Embed(
                        title=f"Spielersuche",
                        colour=discord.Colour(colour),
                        description=f"{Description}\n_Beigetretene Spieler:_\n" + "\n".join(_Tag)
                    )
                    if choice != "Sonstiges":
                        Standart_Embed.set_thumbnail(url=Utils.YamlContainerManagement.get_yamlCGL("Bilder", choice))

                    await m.edit(embed=Standart_Embed)
                    await asyncio.sleep(4)
                    await l.delete()

                else:

                    try:
                        await m.remove_reaction(reaction, user)
                    except:
                        pass

            elif str(reaction.emoji) == "⛔":

                if user.id == ctx.author.id:

                    for user_ in _User:
                        Utils.DBPreconditioning.POST_Uccount(self, user_)
                        embed2 = discord.Embed(
                            title=f"-Anmeldung-",
                            colour=discord.Colour(Utils.Farbe.Dark_Blue),
                            description=f"Der Ticket-Ersteller hat das Ticket frühzeitig abgebrochen!"
                        )
                        await user_.send(embed=embed2)
                    await Utils.DBPreconditioning.DEL_Ticket(self, ctx.author)
                    break

                else:
                    await m.remove_reaction(reaction, user)
        try:
            await m.delete()
        except:
            return
        await Utils.DBPreconditioning.DEL_Ticket(self, ctx.author)
        Utils.DBPreconditioning.POST_Uccount(self, ctx.author)

        for user_ in _User:

            embed2 = discord.Embed(
                title=f"-Anmeldung-",
                colour=discord.Colour(Utils.Farbe.Dark_Blue),
                description=f"Die gewünschte Spielerzahl ist erreicht.\n\nWenn während der Aktivität sich jemand daneben"
                            f"benimmt, melde den Spieler mit `!report @Spieler`. _Bitte melde aber nur, wenn die Person negativ auffällt._"
            )
            test = len(_Control)
            for i in range(test):
                embed2.add_field(name=f"{_User[i]}", value=f"{_Tag[i]}")

            await user_.send(embed=embed2)
            Utils.DBPreconditioning.POST_Uccount(self, user_)

        embed2 = discord.Embed(
            title=f"-Anmeldung-",
            colour=discord.Colour(Utils.Farbe.Dark_Blue),
            description=f"{sender.mention} die gewünschte Spielerzahl ist erreicht.\n\nWenn während der Aktivität sich jemand daneben"
                        f"benimmt, melde den Spieler mit `!report @Spieler`. _Bitte melde aber nur, wenn die Person negativ auffällt._"
        )

        test = len(_Control)
        for i in range(test):
            embed2.add_field(name=f"{_User[i]}", value=f"{_Tag[i]}")

        await sender.send(embed=embed2)

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
