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
                title="UPDATE MELANIE version 1.3.2a",
                description=
                "**LEVEL UP NOTIFICATIONS**\nHey!!, if the level-up notification does annoy you, just type `{0}levelupdisable` to turn it off and `{0}levelupenable` to turn it on again.\n\nBTW, this update includes the changes in the way to use `help` command. Check `{0}help` to understand.\nMore feature will be added soon.\n\n**Enjoy and Have a nice day. Love y'all.**".format(get_prefix()),
                color=0x03fcfc)
          await ctx.channel.send(embed = embedVar)


def setup(client):
    client.add_cog(Dev(client))
