
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://blah-blah-blah")

db = cluster['discord']['data']

def get_prefix():
    prefixid = db.find_one({"id": 'prefix'})
    prefix = prefixid['value']
    return prefix

class Start(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game( get_prefix()[0] + 'help !!!'))
        print('Bot is ready to go as {0.user}'.format(self.client))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            return
        elif isinstance(error, CommandOnCooldown):
            await ctx.send(':woman_gesturing_no: Bình tĩnh nào, đừng spam như thế chứ.', delete_after=4)
            return
        raise error

def setup(client):
    client.add_cog(Start(client))
