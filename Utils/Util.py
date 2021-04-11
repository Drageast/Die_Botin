# Import
import asyncio
import functools
import inspect
import time
import discord
import yaml


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


class ChannelSending:

    @staticmethod
    async def get_channel_embed(user, embed, name):
        channel = discord.utils.get(user.guild.text_channels, name=name)

        if channel is None:
            return

        else:

            message = await channel.send(embed=embed)
            return message

    @staticmethod
    async def get_channel_message(user, message, name):
        channel = discord.utils.get(user.guild.text_channels, name=name)

        if channel is None:
            return

        else:

            message_ = await channel.send(message)
            return message_


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


class WrapperDecorator:

    @staticmethod
    def TimeLogger(func):

        def wrapper_NONE_async(*args, **kwargs):
            before = time.time()
            func_ = func(*args, **kwargs)
            print(f"Executed Function: |{func.__name__}|-|NONE_ASYNC| ; Execution took: |{time.time() - before} seconds|")
            return func_

        @functools.wraps(func)
        async def wrapper_IS_async(*args, **kwargs):
            before = time.time()
            func_ = await func(*args, **kwargs)
            print(f"Executed Function: |{func.__name__}|-|IS_ASYNC| ; Execution took: |{time.time() - before} seconds|")
            return func_

        if inspect.iscoroutinefunction(func):
            return wrapper_IS_async
        else:
            return wrapper_NONE_async


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
