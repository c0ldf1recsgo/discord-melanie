import os
from dotenv import load_dotenv
# from alive import alive
# import json

import discord
from discord.ext import commands
from discord_slash import SlashCommand

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://melanie:c0ldf1re@bot.bvo7z.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster['discord']['data']

def get_prefix(client, message):
    prefixid = db.find_one({"id": 'prefix'})
    prefix = prefixid['value']
    return prefix

intents = discord.Intents().all()
client = discord.Client()
client = commands.Bot(command_prefix = get_prefix, help_command=None, intents=intents)
slash = SlashCommand(client, sync_commands=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
# alive()
client.run(os.getenv('TOKEN'))
