import json
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown

def get_prefix():
    with open('./cogs/prefixes.json', 'r') as f:
        prefix = json.load(f)
    return prefix['prefix']

class Start(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game( get_prefix() + 'help !!!'))
        print('Bot is ready to go as {0.user}'.format(self.client))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            return
        elif isinstance(error, CommandOnCooldown):
            await ctx.send('Vui lòng chờ một chút rồi mới được nhập lại lệnh này.', delete_after=4)
            return
        raise error

def setup(client):
    client.add_cog(Start(client))