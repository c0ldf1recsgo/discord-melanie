import os
from dotenv import load_dotenv
from alive import alive

from replit import db

import discord
from discord.ext import commands

def get_prefix(client, message):
    return db['prefix'][0]

client = discord.Client()
client = commands.Bot(command_prefix = get_prefix, help_command=None)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
alive()
client.run(os.getenv('TOKEN'))