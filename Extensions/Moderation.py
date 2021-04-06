# Import
from discord.ext import commands
import discord
import asyncio

# Utils
import Utils

# Cog Initialising


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def supporttell(self, ctx, user: discord.Member, *, message):

        embed = discord.Embed(
            title="-<SUPPORT>-",
            colour=discord.Colour(Utils.Farbe.TezzQu),
            description=f"{message}"
        )
        try:
            await ctx.message.delete()
        except:
            pass
        await user.send(embed=embed)

    @commands.command(aliases=["c"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, ctx, Anzahl):
        x = 0

        try:
            int(Anzahl)
            for message in await ctx.channel.purge(limit=int(Anzahl)):
                x += 1

            embed = discord.Embed(
                title='Und so geht die Freiheit zu grunde - mit donnerndem Applaus',
                colour=discord.Colour(Utils.Farbe.Dark_Blue),
                description=f'**{x}** Nachrichten gelöscht.\nWenn du alle Nachrichten löschen möchtest, gebe: `{self.client.command_prefix}c *` ein.'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            m = await ctx.send(embed=embed)
            await asyncio.sleep(8)
            try:
                return await m.delete()
            except:
                return

        except:

            if Anzahl == '*':
                for message in await ctx.channel.purge(limit=None):
                    x += 1

                embed = discord.Embed(
                    title='Und so geht die Freiheit zu grunde - mit donnerndem Applaus',
                    colour=discord.Colour(Utils.Farbe.Dark_Blue),
                    description=f'**{x}** Nachrichten gelöscht.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                m = await ctx.send(embed=embed)
                await asyncio.sleep(8)
                try:
                    return await m.delete()
                except:
                    return

            else:
                raise commands.BadArgument(f"{Anzahl} ist nicht gültig, bitte gebe einen Integer(Zahl) oder * an.")


# Cog Finishing


def setup(client):
    client.add_cog(Moderation(client))
