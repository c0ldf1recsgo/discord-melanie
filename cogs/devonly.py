import json

import discord
from discord.ext import commands

def get_prefix():
    with open('./cogs/prefixes.json', 'r') as f:
        prefix = json.load(f)
    return prefix['prefix']

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
                title="BIG UPDATE MELANIE version 2.0",
                description=
                "**FINALLY**\nActually there is no new feature.\n\nBut hey!! Melanie is now have a new home with Herokuapp. Say goodbye to trash Replit. :)", 
                color=0x03fcfc)
          await ctx.channel.send(embed = embedVar)


def setup(client):
    client.add_cog(Dev(client))
