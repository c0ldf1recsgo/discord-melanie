import os
from dotenv import load_dotenv
from alive import alive
import json

# from replit import db

import discord
from discord.ext import commands

def get_prefix(client, message):
    with open('./cogs/prefixes.json', 'r') as f:
        prefix = json.load(f)
    return prefix['prefix']

intents = discord.Intents().all()
client = discord.Client()
client = commands.Bot(command_prefix = get_prefix, help_command=None, intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
# alive()
client.run(os.getenv('TOKEN'))
