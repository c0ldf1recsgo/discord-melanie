import difflib

from replit import db

import discord
from discord.ext import commands


class Dev(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['up'])
    @commands.is_owner()
    async def update(self, ctx, *args):
        # prefix = db['prefix'][0]
        if (str(ctx.author.id) == '394520281814925313'):
          await ctx.message.delete()
          embedVar = discord.Embed(
                title="UPDATE MELANIE version 1.3.0a",
                description=
                "**LEVEL SYSTEM**\nMelanie new update can now check your level on server and your ranking. Check `{0}help 8` or `{0}help level` for more information.\nMore feature will be added soon.\n\n**Enjoy and Have a nice day. Love y'all.**".format(db['prefix'][0]),
                color=0x03fcfc)
          await ctx.channel.send(embed = embedVar)


def setup(client):
    client.add_cog(Dev(client))