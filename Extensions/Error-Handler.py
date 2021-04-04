# Import
import asyncio
import datetime
import traceback
from datetime import datetime
import aiohttp
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
# Utils
import Utils

# Cog Initialising


class ErrorHandling(commands.Cog):

    def __init__(self, client):
        self.client = client

    # ERROR_HANDLER

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CheckFailure):
            try:
                await ctx.message.delete()
            except Exception as e:
                return
            return

        elif isinstance(error, commands.DisabledCommand) or isinstance(error, commands.NoPrivateMessage) or isinstance(error, commands.BadArgument or commands.ArgumentParsingError or commands.BadBoolArgument) or \
            isinstance(error, commands.MissingRequiredArgument or commands.TooManyArguments) or isinstance(error, commands.MissingPermissions or commands.BotMissingPermissions) or \
                isinstance(error, commands.NotOwner) or isinstance(error, commands.CommandOnCooldown) or isinstance(error, commands.CheckFailure):

            embed = discord.Embed(
                title=f'{Utils.YamlContainerManagement.get_yamlCGL("Embed", "HTitle")}',
                colour=discord.Colour(Utils.Farbe.Dark_Blue),
                description=f'Fehler:\n`{error}`\n'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            try:
                await ctx.message.delete()
            except discord.HTTPException:
                pass
            m = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            try:
                await m.delete()
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.CommandInvokeError):

            if isinstance(error.original, Utils.DatabasePreconditioning):
                embed = discord.Embed(
                    title=f'{Utils.YamlContainerManagement.get_yamlCGL("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Dark_Blue),
                    description=f'Ein Fehler in der Datenbank ist aufgetreten:\n`{error}`\n'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                try:
                    await ctx.message.delete()
                except discord.HTTPException:
                    pass
                m = await ctx.send(embed=embed)
                await asyncio.sleep(15)
                try:
                    await m.delete()
                except discord.HTTPException:
                    pass


            else:

                owner = await self.client.fetch_user(Utils.YamlContainerManagement.get_yamlCGL("Variablen", "Dev_IDs", "Drageast"))

                embed = discord.Embed(
                    title='ACHTUNG!',
                    colour=discord.Colour(Utils.Farbe.Dark_Blue),
                    description='Der Command ist **korrumpiert**!\nTritt dieser Fehler erneut auf, '
                                f'kontaktiere **dringend** meinen Developer: {owner.mention}'
                )
                embed.add_field(name='**LOG:**', value=f'```css\n[{error}]\n```')
                embed.set_thumbnail(url=self.client.user.avatar_url)

                async with aiohttp.ClientSession() as session:
                    url = Utils.YamlContainerManagement.get_yamlCGL("Variablen", "ClientSide", "Webhook")

                    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))

                    timestamp = datetime.utcnow()
                    trace = traceback.format_exception(None, error, error.__traceback__)
                    b = 0

                    erembed = discord.Embed(
                        title="\u200b\nEin schwerwiegender Fehler ist aufgetreten!\n\u200b",
                        colour=discord.Colour(Utils.Farbe.Dark_Blue)
                    )
                    erembed.set_author(name=f"{timestamp.strftime(r'%I:%M %p')}")
                    erembed.add_field(name='**OPERATOR:**', value=f'```fix\n[{ctx.author} / {ctx.author.id}]\n```',
                                      inline=False)
                    try:
                        erembed.add_field(name='**SERVER:**', value=f'```fix\n[{ctx.guild.name}]\n```', inline=False)
                        erembed.add_field(name='**KANAL:**', value=f'```fix\n[{ctx.channel.name}]\n```', inline=False)
                    except AttributeError:
                        pass
                    erembed.add_field(name='**COMMAND:**',
                                      value=f'```fix\n[{self.client.command_prefix}{ctx.command.qualified_name}]\n```',
                                      inline=False)
                    erembed.add_field(name='**NACHRICHT:**', value=f'```fix\n[{ctx.message.content}]\n```',
                                      inline=False)
                    erembed.add_field(name='**ERROR:**', value=f'```css\n[{error}]\n```\n\n\u200b', inline=False)
                    erembed.add_field(name='**TRACEBACK:**', value=f'\u200b', inline=False)
                    erembed.set_thumbnail(url=self.client.user.avatar_url)
                    for o in trace:
                        erembed.add_field(name='\u200b', value=f'```python\n{trace[b]}\n```', inline=False)
                        b += 1

                    await webhook.send(username="Ein korrumpierter Command wurde ausgelöst!",
                                       avatar_url=self.client.user.avatar_url, embed=erembed)

                    try:
                        await ctx.message.delete()
                    except discord.HTTPException:
                        pass
                    m = await ctx.send(embed=embed)
                    await asyncio.sleep(15)
                    try:
                        await m.delete()
                    except discord.HTTPException:
                        pass


    # COMMAND_HANDLER


    @commands.command(aliases=["ds"])
    @commands.is_owner()
    async def disable_commands(self, ctx, *, command_name):

        if command_name is not None:

            command = self.client.get_command(command_name)

            if command is None:

                embed = discord.Embed(
                    title=f'{Utils.YamlContainerManagement.get_yamlCGL("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Dark_Blue),
                    description=f'Dieser Command existiert nicht.\nÜberprüfe ihn auf Rechtschreibfehler.\nDeine Angabe: **{command_name}**'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.TimeSend.se_ctx(ctx, embed, 30)


            elif command == ctx.command:

                embed = discord.Embed(
                    title=f'{Utils.YamlContainerManagement.get_yamlCGL("Embed", "HTitle")}',
                    colour=discord.Colour(Utils.Farbe.Dark_Blue),
                    description=f'Du darfst diesen Command nicht Deaktivieren!'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.TimeSend.se_ctx(ctx, embed, 30)

            else:

                command.enabled = not command.enabled

                choice = "Aktiviert" if command.enabled else "Deaktiviert"
                choice_colour = Utils.Farbe.Light_Blue if command.enabled else Utils.Farbe.Dark_Blue

                embed = discord.Embed(
                    title=f'{choice}',
                    colour=discord.Colour(choice_colour),
                    description=f'Der Command: **{command}** wurde erfolgreich {choice}.'
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)

                await Utils.TimeSend.se_ctx(ctx, embed, 10)


# Cog Finishing


def setup(client):
    client.add_cog(ErrorHandling(client))
