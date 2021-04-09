# Import
import asyncio
import discord
import yaml
from .Database_Preconditioning import DBPreconditioning


class YamlContainerManagement:


    @staticmethod
    def get_yamlC(container: str):
        with open("Utils/config.yaml", "r") as f:
            container_ = yaml.safe_load(f)
        container_ = container_[container]
        return container_

    @staticmethod
    def get_yamlCGL(container: str, group: str, load: str = None):
        container_ = YamlContainerManagement.get_yamlC(container)

        return container_[group] if load is None else container_[group][load]


# SMOOTH_SEND

class TimeSend:

    @staticmethod
    async def se_ctx(ctx, embed, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await ctx.message.delete()
            m = await ctx.send(embed=embed)
            await asyncio.sleep(seconds_)
            await m.delete()
        except:
            pass

    @staticmethod
    async def se_message(message, embed, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await message.delete()
        except:
            pass
            m = await message.channel.send(embed=embed)
            await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass

    @staticmethod
    async def e_m(m, embed, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await m.edit(embed=embed)
            try:
                await m.clear_reactions()
            except:
                pass
            await asyncio.sleep(seconds_)
            await m.delete()
        except:
            pass


    @staticmethod
    async def sm_ctx(ctx, message, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await ctx.message.delete()
        except:
            pass
            m = await ctx.send(message)
            await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass

    @staticmethod
    async def sm_message(message, message_content, seconds=None):

        seconds_ = seconds if seconds is not None else 10

        try:
            await message.delete()
        except:
            pass
            m = await message.channel.send(message_content)
            await asyncio.sleep(seconds_)
        try:
            await m.delete()
        except:
            pass


class TicketReactor:
    def __init__(self, client):
        self.client = client

    async def wait_message(self, user):
        new_message = await self.client.wait_for('message', check=lambda message: message.author == user,
                                                 timeout=120.0)

        return new_message

    async def ListenAndReact(self, ctx, user):
        DiscordUser = []
        GamerTag = []
        control = []
        x = 0

        data = DBPreconditioning.GET_Ticket(self, user)

        channel = self.client.get_channel(data.ChannelID)
        m = await channel.fetch_message(data.MessageID)


        def check(reaction, user):
            return user == user and str(reaction.emoji) == "✅" or "❌" or "🛑"

        sender = await self.client.fetch_user(data._id)

        while x < int(data.RequiredParticipants):
            reaction, user = await self.client.wait_for("reaction_add", check=check)

            if user.bot:
                return

            if str(reaction.emoji) == "✅":

                _data = DBPreconditioning.GET_Uccount(self, user)

                if _data.TicketEntry is False:

                    embed2 = discord.Embed(
                        title="-Anmeldung-",
                        colour=discord.Colour(Farbe.Light_Blue),
                        description=f"Der Spieler `{sender.name}` benötigt noch deinen Gamertag. Bitte Antworte mit deinem Gamertag."
                    )

                    t = await user.send(embed=embed2)
                    try:
                        r = await TicketReactor.wait_message(self, user)
                    except asyncio.TimeoutError:
                        await m.remove_reaction(reaction, user)
                        return

                    a = "" if _data.Reports is None else f"\n_Achtung! Der Spieler wurde schon {_data.Reports} mal als Spielverderber gemeldet!_"


                    embed = discord.Embed(
                        title=f"-Anmeldung-",
                        colour=discord.Colour(Farbe.Light_Blue),
                        description=f"Der Discord Nutzer: `{user.name}` hat sich mit dem **InGame Namen**: `{r.content}` angemeldet.{a}"
                    )
                    await sender.send(embed=embed)
                    await t.edit(embed=embed)

                    DiscordUser.append(user)
                    GamerTag.append(r.content)
                    control.append(user.id)

                    DBPreconditioning.POST_Uccount(self, user, TicketEntry=True)

                    x += 1

                else:

                    await m.remove_reaction(reaction, user)

                    embed2 = discord.Embed(
                        title="Du kannst dich nicht Anmelden!",
                        colour=discord.Colour(Farbe.Dark_Blue),
                        description=f"Du bist schon in einem Ticket eingetragen!"
                                    f"\nWenn du dies für einen Fehler in der Datenbank hältst, gebe: `!debug bool` ein."
                    )
                    await user.send(embed=embed2)

            elif str(reaction.emoji) == "❌":

                if control.count(user.id) >= 1:

                    index = int(control.index(user.id))

                    del DiscordUser[index]
                    del GamerTag[index]
                    del control[index]

                    embed = discord.Embed(
                        title=f"-Abmeldung-",
                        colour=discord.Colour(Farbe.Dark_Blue),
                        description=f"Der Discord Nutzer: `{user.name}` hat sich abgemeldet."
                    )

                    await sender.send(embed=embed)
                    try:
                        await m.remove_reaction("✅", user)
                        await m.remove_reaction(reaction, user)
                    except:
                        pass

                    DBPreconditioning.POST_Uccount(self, user)

                    x -= 1

                else:

                    try:
                        await m.remove_reaction(reaction, user)
                    except:
                        pass

            elif str(reaction.emoji) == "🛑":
                if user == ctx.author:
                    for user_ in DiscordUser:
                        DBPreconditioning.POST_Uccount(self, user_)
                        embed2 = discord.Embed(
                            title=f"-Anmeldung-",
                            colour=discord.Colour(Farbe.Dark_Blue),
                            description=f"Der Ticket-Ersteller hat das Ticket frühzeitig abgebrochen!"
                        )
                        await user_.send(embed=embed2)
                    await DBPreconditioning.DEL_Ticket(self, ctx.author)
                    break
        try:
            await m.delete()
        except:
            return
        await DBPreconditioning.DEL_Ticket(self, ctx.author)
        DBPreconditioning.POST_Uccount(self, ctx.author)

        for user_ in DiscordUser:

            embed2 = discord.Embed(
                title=f"-Anmeldung-",
                colour=discord.Colour(Farbe.Dark_Blue),
                description=f"Die gewünschte Spielerzahl ist erreicht.\n\nWenn während der Aktivität sich jemand daneben"
                            f"benimmt, melde den Spieler mit `!report @Spieler`. _Bitte melde aber nur, wenn die Person negativ auffällt._"
            )
            test = len(control)
            for i in range(test):
                embed2.add_field(name=f"{DiscordUser[i]}", value=f"{GamerTag[i]}")

            await user_.send(embed=embed2)
            DBPreconditioning.POST_Uccount(self, user_)

        embed2 = discord.Embed(
            title=f"-Anmeldung-",
            colour=discord.Colour(Farbe.Dark_Blue),
            description=f"{sender.mention} die gewünschte Spielerzahl ist erreicht.\n\nWenn während der Aktivität sich jemand daneben"
                        f"benimmt, melde den Spieler mit `!report @Spieler`. _Bitte melde aber nur, wenn die Person negativ auffällt._"
        )

        test = len(control)
        for i in range(test):
            embed2.add_field(name=f"{DiscordUser[i]}", value=f"{GamerTag[i]}")

        await sender.send(embed=embed2)




class ChannelSending:

    @staticmethod
    async def get_channel(user, embed, name):
        channel = discord.utils.get(user.guild.text_channels, name=name)

        if channel is None:
            return

        else:

            message = await channel.send(embed=embed)
            return message


class Pagination:
    def __init__(self, client):
        self.client = client

    async def Pag(self, ctx, content, info=None):

        contents = content

        info_ = None

        pages = len(contents)

        cur_page = 0
        try:
            await ctx.message.delete()
        except:
            pass
        message = await ctx.send(embed=contents[cur_page])

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("⏹️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        if info is not None:
            await message.add_reaction("ℹ️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⏪", "◀️", "⏹️", "▶️", "⏩", "ℹ️"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)

                if str(reaction.emoji) == "▶️":
                    if cur_page != pages - 1:
                        cur_page += 1
                        await message.edit(embed=contents[cur_page])
                        await message.remove_reaction(reaction, user)
                    else:
                        pass

                elif str(reaction.emoji) == "◀️" and cur_page > 0:
                    cur_page -= 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    try:
                        await message.delete()
                    except:
                        pass
                    try:
                        await info_.delete()
                    except:
                        pass
                    break

                elif str(reaction.emoji) == "⏪":
                    cur_page = 0
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏩":
                    cur_page = pages - 1
                    await message.edit(embed=contents[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "ℹ️":
                    if info_ is None:
                        info_ = await ctx.send(info)
                    else:
                        try:
                            await info_.delete()
                        except:
                            pass
                        info_ = None

                    await message.remove_reaction(reaction, user)


                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except:
                    pass
                try:
                    await info_.delete()
                except:
                    pass
                break


# VARIABLEN

# FARBEN

class Farbe:

    Dark_Blue = 0xf3e63

    Light_Blue = 0x84a4cd

    Orange = 0xfd9644

    Darker_Theme = 0x23272a

    TezzQu = 0xff6a00

    Welcome_Blue = 0x14dd

    Welcomer_Blue = 0x7c5f8
