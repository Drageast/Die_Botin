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

    @commands.command()
    async def createTicket(self, ctx):
        await ctx.message.delete()

        m1 = await ctx.send("Bitte spezifiziere mit deiner nächsten Nachricht die Aktivität, für die du suchst.\nBsp. Tiefsteinkrypta")

        try:

            r1 = await self.wait_message(ctx)
            await r1.delete()
        except asyncio.TimeoutError:
            try:
                await m1.delete()
            except:
                pass
            return

        a1 = f"Das Thema lautet: `{r1.content}`. Bitte spezifiziere in deiner Nächsten Nachricht, wie viele Spieler du benötigst.\nBsp. 3"
        await m1.delete()
        m2 = await ctx.send(a1)

        try:

            r2 = await self.wait_message(ctx)
            await r2.delete()
        except asyncio.TimeoutError:
            try:
                await m2.delete()
            except:
                pass
            return

        a2 = f"Das Thema lautet: `{r1.content}` und die Spielerzahl: `{r2.content}`. Bitte spezifiziere in deiner Nächsten Nachricht, was deine Beschreibung dazu ist.\nBsp. Tiefsteinkrypta Fresh mit erfahrung"
        await m2.delete()
        m3 = await ctx.send(a2)

        try:

            r3 = await self.wait_message(ctx)
            await r3.delete()
        except asyncio.TimeoutError:
            try:
                await m3.delete()
            except:
                pass
            return

        data = await Utils.Ticket.create_Ticket(self, ctx.author, r1.content, int(r2.content), r3.content, 1)


        embed = discord.Embed(
            title=f"Spieler suche: {r1.content}",
            colour=discord.Colour(Utils.Farbe.Light_Blue),
            description=f"{r3.content}"
        )
        embed.add_field(name="Benötigte Spieler:", value=f"{r2.content}")

        message = await Utils.ChannelSending.get_channel(ctx.author, embed, "tickets")

        await m3.delete()

        await Utils.Ticket.edit_Ticket(self, ctx.author, message.id, 1)
        await Utils.Ticket.edit_Ticket(self, ctx.author, message.channel.id, 2)

        await Utils.TicketReactor.ListenAndReact(self, ctx, ctx.author)

# Cog Finishing


def setup(client):
    client.add_cog(TicketSystem(client))
