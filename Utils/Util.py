# Import
import asyncio
import discord
import yaml
from .DB_Preconditioning import Ticket


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

    async def ListenAndReact(self, ctx, user):

        x = 0

        data = await Ticket.get_Ticket(self, user)

        senderID = data["_id"]
        thema = data["Activity"]
        messageID = data["IDs"]["MessageID"]
        channelid = data["IDs"]["ChannelID"]
        neededParticipants = data["NeededParticipants"]

        channel = self.client.get_channel(channelid)
        m = await channel.fetch_message(messageID)

        await m.add_reaction("✅")

        def check(reaction, user):
            return user != self.client and str(reaction.emoji) == "✅"

        sender = await self.client.fetch_user(senderID)

        while x < int(neededParticipants):
            reaction, user = await self.client.wait_for("reaction_add", check=check)

            embed = discord.Embed(
                title=f"Es hat sich jemand für: {thema} gemeldet.",
                colour=discord.Colour(Farbe.Light_Blue),
                description=f"Der Discord Name lautet: `{user.name}`, melde dich bei ihm, wenn du den Gamertag benötigst."
            )

            await sender.send(embed=embed)

            embed2 = discord.Embed(
                title="Ich habe dich angemeldet!",
                colour=discord.Colour(Farbe.Light_Blue),
                description=f"Der Spieler `{sender.name}` benötigt noch deinen Gamertag, bitte melde dich bei ihm."
            )

            await user.send(embed=embed2)

            x += 1

        await m.delete()
        await Ticket.delete_Ticket(self, ctx.author)


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

    async def Pag(self, ctx, content, info = None):

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
