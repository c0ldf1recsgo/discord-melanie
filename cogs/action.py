import json
import random
import os
import requests
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

load_dotenv()
def get_slap():
  key = os.getenv('TENOR_KEY')
  url = 'https://api.tenor.com/v1/random?key=' + key + '&q=anime-slap&media_filter=minimal&limit=1&pos={0}'
  offset = random.randrange(0,120)
  URL = url.format(offset)
  reponse = requests.get(URL)
  json_data = json.loads(reponse.text)
  result = json_data['results'][0]['media'][0]['gif']['url']

  return result


def get_kiss():
  key = os.getenv('TENOR_KEY')
  url = 'https://api.tenor.com/v1/random?key=' + key + '&q=anime-kiss&media_filter=minimal&limit=1&pos={0}'
  offset = random.randrange(0,120)
  URL = url.format(offset)
  reponse = requests.get(URL)
  json_data = json.loads(reponse.text)
  result = json_data['results'][0]['media'][0]['gif']['url']

  return result


def get_hug():
  key = os.getenv('TENOR_KEY')
  url = 'https://api.tenor.com/v1/random?key=' + key + '&q=anime-hug&media_filter=minimal&limit=1&pos={0}'
  offset = random.randrange(0,120)
  URL =url.format(offset)
  reponse = requests.get(URL)
  json_data = json.loads(reponse.text)
  result = json_data['results'][0]['media'][0]['gif']['url']

  return result


def get_pat():
  key = os.getenv('TENOR_KEY')
  url = 'https://api.tenor.com/v1/random?key=' + key + '&q=anime-pat&media_filter=minimal&limit=1&pos={0}'
  offset = random.randrange(1,120)
  URL = url.format(offset)
  reponse = requests.get(URL)
  json_data = json.loads(reponse.text)
  result = json_data['results'][0]['media'][0]['gif']['url']
  
  return result

class Action(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    
    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def slap(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            gif = get_slap()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " vả toàn server", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent slap')
        elif '<@!' in args[0] and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][3:-1])
            gif = get_slap()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " vả " + (str(taggered))[:-5] + '! Hư này !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent slap')
        elif '<@' in args[0] and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][2:-1])
            gif = get_slap()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " vả " + (str(taggered))[:-5] + '! Hư này !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent slap')
        else:
            await ctx.channel.send('Sai cú pháp')


    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def kiss(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            gif = get_kiss()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " Moah <3", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent kiss')
        elif '<@!' in args[0] and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][3:-1])
            gif = get_kiss()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " hun " + (str(taggered))[:-5] + '! So sweat !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent kiss')
        elif '<@' in args[0] and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][2:-1])
            gif = get_kiss()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " hun " + (str(taggered))[:-5] + '! So sweat !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent kiss')
        else:
            await ctx.channel.send('Sai cú pháp')


    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def hug(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            gif = get_hug()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " Awww <3", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent hug')
        elif '<@!' in args[0] and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][3:-1])
            gif = get_hug()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " ôm " + (str(taggered))[:-5] + '! Awww !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent hug')
        elif '<@' in args[0] and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][2:-1])
            gif = get_hug()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " ôm " + (str(taggered))[:-5] + '! Awww !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent hug')
        else:
            await ctx.channel.send('Sai cú pháp')


    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def pat(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            gif = get_pat()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " xoa đầu tất cả mọi người <3", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent pat')
        elif ('<@!' in args[0]) and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][3:-1])
            gif = get_pat()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " xoa đầu " + (str(taggered))[:-5] + '! Ahyhy !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent pat')
        elif ('<@' in args[0]) and '>' in args[0]:
            print(ctx.author.id)
            taggered = await self.client.fetch_user(args[0][2:-1])
            gif = get_pat()
            embedVar = discord.Embed(description=" ", color=0xffff00)
            embedVar.set_author(name=ctx.author.display_name + " xoa đầu " + (str(taggered))[:-5] + '! Ahyhy !!', icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=gif)
            await ctx.channel.send(embed=embedVar)
            print('sent pat')
        else:
            await ctx.channel.send('Sai cú pháp')

def setup(client):
    client.add_cog(Action(client))