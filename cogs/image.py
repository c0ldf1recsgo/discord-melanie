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


def get_girl_total():
  key = os.getenv('TUMBLR_KEY')
  url = ('https://api.tumblr.com/v2/blog/c0ldf1recsgo.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset=1')
  reponse = requests.get(url)
  json_data = json.loads(reponse.text)

  a = json_data['response']['blog']['total_posts']
  return a


def get_girl_image():
  total = get_girl_total()
  key = os.getenv('TUMBLR_KEY')
  ind = random.randrange(0, total)
  url = ('https://api.tumblr.com/v2/blog/c0ldf1recsgo.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}').format(str(ind))
  print(url)
  reponse = requests.get(url)
  json_data = json.loads(reponse.text)
  try:
    a = json_data['response']['posts'][0]['body']
  except:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return [result, ind]
  res = ""
  check = False
  for i in range(len(a)):
    if a[i] == 'h' and a[i+1] == 't' and a[i+2] == 't' and a[i+3] == 'p' and a[i-5] == 's' and a[i-7] == 'g' and a[i-8] == 'm':
      check = True
    if a[i] == 'j' and a[i+1] == 'p' and a[i+2] == 'g':
      check = False
      res += 'jpg' 
      return [res, ind]
    elif a[i] == 'p' and a[i+1] == 'n' and a[i+2] == 'g':
      check = False
      res += 'png' 
      return [res, ind]
    if check == True:
      res += a[i]
  return [res, ind]


def get_girl_image_2():
  key = os.getenv('TUMBLR_KEY')
  ind = random.randrange(0, 1547)
  url = ('http://api.tumblr.com/v2/blog/asia-beauty-collection.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}').format(str(ind))
  print(url)
  reponse = requests.get(url)
  json_data = json.loads(reponse.text)
  try:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return result
  except:
    a = json_data['response']['posts'][0]['body']
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
  urls = [
    'https://api.tumblr.com/v2/blog/foodfuck.net/posts?api_key=' + key + '&type=photo&limit=1&offset={0}', 
    'https://api.tumblr.com/v2/blog/fyeahvietnamesefood-blog.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}',
    'https://api.tumblr.com/v2/blog/daily-deliciousness.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}']
  url = random.choice(urls)
  ind = random.randrange(2,40475)
  if 'fyeah' in url:
    ind = random.randrange(1,204)
  elif 'daily' in url:
    ind = random.randrange(1,13649)
  
  reponse = requests.get(url.format(str(ind)))
  json_data = json.loads(reponse.text)
  # result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]

  try:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return result
  except:
    a = json_data['response']['posts'][0]['body']
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


def get_nsfw():
  key = os.getenv('TUMBLR_KEY')
  url = 'https://api.tumblr.com/v2/blog/neko-no-oto.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}'
  ind = random.randrange(1,1329)
  reponse = requests.get(url.format(str(ind)))
  json_data = json.loads(reponse.text)
  # result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]

  try:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return result
  except:
    a = json_data['response']['posts'][0]['body']
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


def get_dog():
  key = os.getenv('TUMBLR_KEY')
  urls = [
    'https://api.tumblr.com/v2/blog/siberiianblog.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}',
    'https://api.tumblr.com/v2/blog/scampthecorgi.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}',
    'https://api.tumblr.com/v2/blog/endless-puppies.tumblr.com/posts?api_key=' + key + '&type=photo&limit=1&offset={0}'
    ]
  url = random.choice(urls)
  ind = random.randrange(1,951)
  if 'scampthecorgi' in url:
    ind = random.randrange(1,1441)
  elif 'endless' in url:
    ind = random.randrange(1,3119)
  reponse = requests.get(url.format(str(ind)))
  json_data = json.loads(reponse.text)
  # result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]

  try:
    result = json_data['response']['posts'][0]["photos"][0]["original_size"]["url"]
    return result
  except:
    a = json_data['response']['posts'][0]['body']
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


def check_if_it_is_me(ctx):
    return ctx.message.author.id == 394520281814925313

class Image(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    async def cog_before_invoke(self, ctx: commands.Context):
      if check_if_it_is_me(ctx):
        return ctx.command.reset_cooldown(ctx)

    # Commands
    @commands.command(aliases=['xinh', 'gai', 'simp'])
    @cooldown(1, 10, BucketType.user)
    async def girl(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            i = random.randrange(0,4)
            if check_if_it_is_me(ctx):
              i = 1
            else:
              pass
            if i == 2:
                print(ctx.author.id)
                embedVar = discord.Embed(description="Nhưng không có cô gái nào xuất hiện cả.", color=0xd14949)
                embedVar.set_author(name=ctx.author.display_name + " thích ngắm gái", icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embedVar)
                print('gai xinh')
            else:
                print(ctx.author.id)
                total = get_girl_total()
                link = get_girl_image()
                xinh = link[0]
                idx = link[1]
                embedVar = discord.Embed(description=" ", color=0xd14949)
                embedVar.set_author(name=ctx.author.display_name + " thích ngắm gái", icon_url=ctx.author.avatar_url)
                embedVar.set_image(url=xinh)
                embedVar.set_footer(text=f'Ảnh {idx + 1}/{total-1}')
                await ctx.channel.send(embed=embedVar)
                print('gai xinh')

    @commands.command(aliases=['xinh2', 'gai2', 'simp2'])
    @cooldown(1, 8, BucketType.user)
    async def girl2(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            i = random.randrange(0,4)
            if check_if_it_is_me(ctx):
              i = 1
            else:
              pass
            if i == 2:
                print(ctx.author.id)
                embedVar = discord.Embed(description="Nhưng không có cô gái nào xuất hiện cả.", color=0xd14949)
                embedVar.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embedVar)
                print('gai xinh')
            else:
                print(ctx.author.id)
                link = get_girl_image_2()
                embedVar = discord.Embed(description=" ", color=0xd14949)
                embedVar.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embedVar.set_image(url=link)
                await ctx.channel.send(embed=embedVar)
                print('gai xinh')


    @commands.command(aliases=['man', 'handsome', 'boy', 'zai'])
    @cooldown(1, 5, BucketType.user)
    async def trai(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            # xinh = get_boy_image()
            # print(xinh)
            embedVar = discord.Embed(description="Xin lỗi nhưng chẳng có chàng trai nào cho bạn đâu.", color=0xd14949)
            embedVar.set_author(name=ctx.author.display_name + " thích ngắm zai :\\", icon_url=ctx.author.avatar_url)
            # embedVar.set_image(url=xinh)
            await ctx.channel.send(embed=embedVar)
            print('trai dep')


    @commands.command()
    @cooldown(1, 5, BucketType.user)
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


    @commands.command(aliases=['cat', 'meo'])
    @cooldown(1, 10, BucketType.user)
    async def nsfw(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            img = get_nsfw()
            embedVar = discord.Embed(description=" ", color=0xff00f7)
            embedVar.set_author(name=ctx.author.display_name + " hư quá", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=img)
            await ctx.channel.send(embed=embedVar)
            print('sent nsfw')


    @commands.command(aliases=['cho', 'cun'])
    @cooldown(1, 10, BucketType.user)
    async def dog(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            img = get_dog()
            embedVar = discord.Embed(description=" ", color=0xff00f7)
            embedVar.set_author(name=ctx.author.display_name + " say gâu gâu", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=img)
            await ctx.channel.send(embed=embedVar)
            print('sent dog')


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def phone(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            img = 'https://source.unsplash.com/random/800x0/?iphone'
            reponse = requests.get(img)
            url = reponse.url
            embedVar = discord.Embed(description=" ", color=0xff00f7)
            embedVar.set_author(name=ctx.author.display_name + " get into an innovation", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=url)
            mesg = await ctx.channel.send(embed=embedVar)

            await mesg.add_reaction("❌")
            def check(reaction, user):
              return user == ctx.author and str(reaction.emoji) == '❌' and reaction.message == mesg
            reaction, user = await self.client.wait_for('reaction_add', check=check)
            await mesg.delete()


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def pad(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            img = 'https://source.unsplash.com/random/800x0/?ipad'
            reponse = requests.get(img)
            url = reponse.url
            embedVar = discord.Embed(description=" ", color=0xff00f7)
            embedVar.set_author(name=ctx.author.display_name + " get into an innovation", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=url)
            mesg = await ctx.channel.send(embed=embedVar)

            await mesg.add_reaction("❌")
            def check(reaction, user):
              return user == ctx.author and str(reaction.emoji) == '❌' and reaction.message == mesg
            reaction, user = await self.client.wait_for('reaction_add', check=check)
            await mesg.delete()


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def mage(self, ctx, *args):
        blacklist = ['sex', 'lingerie', 'sensual', 'sexsual']
        if ctx.author == self.client.user:
            return
        if not args:
            return
        elif args[0] not in blacklist:
            img = f'https://source.unsplash.com/random/800x0/?{args[0]}'
            reponse = requests.get(img)
            url = reponse.url
            embedVar = discord.Embed(description=" ", color=0xff00f7)
            embedVar.set_author(name=ctx.author.display_name + f" muốn xem {args[0]}", icon_url=ctx.author.avatar_url)
            embedVar.set_image(url=url)
            mesg = await ctx.channel.send(embed=embedVar)

            await mesg.add_reaction("❌")
            def check(reaction, user):
              return user == ctx.author and str(reaction.emoji) == '❌' and reaction.message == mesg
            reaction, user = await self.client.wait_for('reaction_add', check=check)
            await mesg.delete()


def setup(client):
    client.add_cog(Image(client))
