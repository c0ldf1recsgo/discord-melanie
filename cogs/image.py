import json
import random
import os
import requests
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

load_dotenv()
def get_boy_image():
  key = os.getenv('TUMBLR_KEY')
  ind = random.randrange(1,174)
  urls = 'https://api.tumblr.com/v2/blog/hawtguysbcwhynot.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}'.format(ind)
  reponse = requests.get(urls)
  json_data = json.loads(reponse.text)
  try:
    a = json_data['response']['posts'][0]['body']
  except:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return result
  res = ""
  check = False
  for i in range(len(a)):
      if a[i] == 'h' and a[i+1] == 't' and a[i+2] == 't' and a[i+3] == 'p' and a[i-5] == 's' and a[i-7] == 'g' and a[i-8] == 'm':
          check = True
      if a[i] == 'j' and a[i+1] == 'p' and a[i+2] == 'g':
          check = False
          res += 'jpg' 
          return res
      elif a[i] == 'p' and a[i+1] == 'n' and a[i+2] == 'g':
          check = False
          res += 'png' 
          return res
      if check == True:
          res += a[i]
  return res


def get_girl_image():
  key = os.getenv('TUMBLR_KEY')
  # urls = [
  #   'https://api.tumblr.com/v2/blog/lotonxyz-blog.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}', 'https://api.tumblr.com/v2/blog/c0ldf1recsgo.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}']
  # urls = [
  #   'https://api.tumblr.com/v2/blog/lotonxyz-blog.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}','https://api.tumblr.com/v2/blog/a-girls-beautiful.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}', 'https://api.tumblr.com/v2/blog/c0ldf1recsgo.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}']

  # selection = random.choice(urls)
  # ind = random.randrange(2,1383)
  # # ind = random.randrange(2,240)
  # if 'lotonxyz' in selection:
  #   ind = random.randrange(2,206)
  # elif 'c0ldf1recsgo' in selection:
  #   ind = random.randrange(2,240)
  ind = random.randrange(2,315)
  url = ('https://api.tumblr.com/v2/blog/c0ldf1recsgo.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}').format(str(ind))
  print(url)
  reponse = requests.get(url)
  json_data = json.loads(reponse.text)
  try:
    a = json_data['response']['posts'][0]['body']
  except:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return result
  # result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
  # return result
  res = ""
  check = False
  for i in range(len(a)):
    if a[i] == 'h' and a[i+1] == 't' and a[i+2] == 't' and a[i+3] == 'p' and a[i-5] == 's' and a[i-7] == 'g' and a[i-8] == 'm':
      check = True
    if a[i] == 'j' and a[i+1] == 'p' and a[i+2] == 'g':
      check = False
      res += 'jpg' 
      return res
    elif a[i] == 'p' and a[i+1] == 'n' and a[i+2] == 'g':
      check = False
      res += 'png' 
      return res
    if check == True:
      res += a[i]
  return res


def get_food_image():
  key = os.getenv('TUMBLR_KEY')
  url = 'https://api.tumblr.com/v2/blog/foodfuck.net/posts?api_key=' + key + '&type=photo&limit=1&offset={0}'
  ind = random.randrange(2,40475)
  reponse = requests.get(url.format(str(ind)))
  json_data = json.loads(reponse.text)
  result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]

  return result


def get_nsfw():
  key = os.getenv('TUMBLR_KEY')
  url = 'https://api.tumblr.com/v2/blog/jsc-dorian-gray.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}'
  ind = random.randrange(1,43987)
  reponse = requests.get(url.format(str(ind)))
  json_data = json.loads(reponse.text)
  result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]

  return result

class Image(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(aliases=['xinh', 'gai', 'simp'])
    @cooldown(1, 3, BucketType.user)
    async def girl(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            xinh = get_girl_image()
            embedVar = discord.Embed(description=" ", color=0xd14949)
            embedVar.set_author(name=ctx.author.display_name + " thích ngắm gái", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=xinh)
            await ctx.channel.send(embed=embedVar)
            print('gai xinh')


    @commands.command(aliases=['man', 'handsome', 'boy', 'zai'])
    @cooldown(1, 3, BucketType.user)
    async def trai(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            xinh = get_boy_image()
            # print(xinh)
            embedVar = discord.Embed(description=" ", color=0xd14949)
            embedVar.set_author(name=ctx.author.display_name + " thích ngắm zai :\\", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=xinh)
            await ctx.channel.send(embed=embedVar)
            print('trai dep')


    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def food(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            img = get_food_image()
            embedVar = discord.Embed(description=" ", color=0xfc9803)
            embedVar.set_author(name=ctx.author.display_name + " đang đói lắm rồi", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=img)
            await ctx.channel.send(embed=embedVar)
            print('sent food image')


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def unsfw(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            img = get_nsfw()
            embedVar = discord.Embed(description=" ", color=0xff00f7)
            embedVar.set_author(name=ctx.author.display_name + " is so bad", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=img)
            await ctx.channel.send(embed=embedVar)
            print('sent nsfw')

def setup(client):
    client.add_cog(Image(client))
