# pylint: disable=relative-beyond-top-level
import re
from datetime import datetime
from typing import Optional
import urllib.request as r
import json

from replit import db

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

def conv_vn(text):
  patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
  }
  output = text
  for regex, replace in patterns.items():
    output = re.sub(regex, replace, output)
    output = re.sub(regex.upper(), replace.upper(), output)
  return output

def conv_emo(vntext):
  num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
  numw = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero']
  text = conv_vn(vntext)
  new_list = []
  for i in list(text):
    if i.isalpha():
      new_list.append(':regional_indicator_' + i.lower() + ': ')
    elif i.isnumeric():
      new_list.append(':' + numw[num.index(i)] + ': ')
    elif i == ' ':
      new_list.append(i + i + i + i + i)
    else:
      return 'Không thể chuyển ký tự đặc biệt hoặc emoji'
  return ''.join(new_list)

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def conv_cur(rate, _to, _from):
  return (rate *  _from /  _to)

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Events
    

    # Commands
    @commands.command(aliases=['m', 'cal', 'tinh', 'calculate', 'math'])
    @cooldown(1, 3, BucketType.user)
    async def _math(self, ctx, *args):
        print(ctx.author.id)
        if not args:
            await ctx.channel.send("Gì đây -.-")
            pass
        else:
            m = ' '.join(args)
            code = compile(m, "<string>", "eval")
            try:
                print(eval(code))
                await ctx.channel.send(eval(code))
            except:
                await ctx.channel.send('Phép tính có vấn đề rồi.')
        print('calculate')

    @commands.command(aliases=['ihcmus', 'melanie'])
    @cooldown(1, 3, BucketType.user)
    async def bot(self, ctx, *args):
        print(ctx.author.id)
        # id = '797016488280064032'
        if not args:
            me = await self.client.fetch_user('797016488280064032')
            created_str = 'January 08 2021 at 08:18'
            joined_str = 'January 11 2021 at 08:04'
            created = datetime.strptime(created_str, '%B %d %Y at %H:%M')
            joined = datetime.strptime(joined_str, '%B %d %Y at %H:%M')
            today = datetime.now()
            bd = today - created
            jd = today - joined
            embed = discord.Embed(title='Tôi là Melanie', description='Tên khai sanh: iHCMUS@6172', color=discord.Color.purple())
            
            embed.set_thumbnail(url=me.avatar_url) 
            embed.add_field(name=f'Ngày sanh: {bd.days} ngày tuổi', value=created_str, inline=False)
            embed.add_field(name=f'Tham gia {ctx.message.guild.name}: {jd.days} ngày', value=joined_str, inline=False)
            embed.add_field(name='Version:', value='`1.2.2a`', inline=False)
            
            await ctx.send(embed=embed)
        else:
            pass


    @commands.command(aliases=['se'])
    @cooldown(1, 5, BucketType.user)
    async def sayemo(self, ctx, *args):
      print(ctx.author.id)
      if ctx.author == self.client.user:
        return
      await ctx.message.delete()
      if not args:
        await ctx.channel.send("Ơ thế tôi phải nói gì bây giờ.")
      else:
        mes = ' '.join(args)
        await ctx.channel.send(conv_emo(mes))
      print('say somethings')


    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def say(self, ctx, *args):
      print(ctx.author.id)
      if ctx.author == self.client.user:
        return
      await ctx.message.delete()
      if not args:
        await ctx.channel.send("Ơ thế tôi phải nói gì bây giờ.")
      else:
        await ctx.channel.send(' '.join(args))
      print('say somethings')
    
    
    @commands.command(aliases=['cur'])
    async def currency(self, ctx, *args):
      print(ctx.author.id)
      print('money exchange')
      json_url = "https://api.exchangeratesapi.io/latest?base=USD"
      response = r.urlopen(json_url)
      data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
      array = data['rates']
      x = list(array)
      USD= array.get(x[26])
      country = ["CAD", "HKD", "ISK", "PHP", "DKK", "HUF", "CZK", "GBP", "RON", "SEK", "IDR", "INR", "BRL", "RUB", "HRK", "JPY", "THB", "CHF", "EUR", "MYR", "BGN", "TRY", "CNY", "NOK", "NZD", "ZAR", "USD", "MXN", "SGD", "AUD", "ILS", "KRW", "PLN", "VND"]
      
      if not args:
        await ctx.send('1 USD = 23017.45 VND.')
      elif not (args[0].isnumeric() or isfloat(args[0])):
        await ctx.send('Cần nhập số tiền vào.')
      elif len(args) < 3:
        await ctx.send(f"Cần nhập đơn vị tiền vào sau lệnh. VD: `{db['prefix'][0]}cur [số tiền]` `USD` `VND`")
      elif args[1].upper() == 'VND':
        usdpervnd = 0.000043
        try:
          money = conv_cur((usdpervnd)*float(args[0]), USD, array.get(x[country.index(args[2].upper())]))
        except:
          money = conv_cur((usdpervnd)*int(args[0]), USD, array.get(x[country.index(args[2].upper())]))
        await ctx.send(f"It's {round(money, 2)}")
      elif args[2].upper() == 'VND':
        vndperusd = 23016.97
        try:
          money = conv_cur(float(args[0]), array.get(x[country.index(args[1].upper())]), USD)
          after = money * vndperusd
        except:
          money = conv_cur(int(args[0]), array.get(x[country.index(args[1].upper())]), USD)
          after = money * vndperusd
        await ctx.send(f"It's {round(after,2)}")
      elif (args[1].upper() not in country) or (args[2].upper() not in country):
        await ctx.send("Chưa hỗ trợ chuyển đổi loại tiền tệ này nhé. Xem lệnh `curs` để xem danh sách loại tiền được hỗ trợ.")
      else:
        try:
          money = conv_cur(float(args[0]), array.get(x[country.index(args[1].upper())]), array.get(x[country.index(args[2].upper())]))
          await ctx.send(f"It's {round(money, 2)}")
        except:
          money = conv_cur(int(args[0]), array.get(x[country.index(args[1].uper())]), array.get(x[country.index(args[2].upper())]))
          await ctx.send(f"It's {round(money, 2)}")

    @commands.command(aliases=['curs'])
    async def currencies(self, ctx, *args):
        print(ctx.author.id)
        print('sent currencies')
        if not args:
          des = "CAD: Canadian Dolla\nHKD: Hong Kong Dollar\nISK: Krona from Iceland\nPHP: Peso Philippines\nDKK: Danish Krone\nHUF: Forint from Hungary\nCZK: Czech Koruna\nGBP: Pound Sterling\nRON: Romanian Leu\nSEK: Sweden Krona\nIDR: Rupiah Indog\nINR: Rupee India\nBRL: Real Brasil\nRUB: Russian Ruble\nHRK: Croatia Kuna\nJPY: Japanese Yen\nTHB: Thais Baht\nCHF: Liechtentsein Franc\nEUR: European\nMYR: Ringgit Malaysia\nBGN: Bulgarian Lev\nTRY: Turkish lira\nCNY: Renminbi Yuan\nNOK: Norwegian Krone\nNZD: New Zealand Dollar\nZAR: South African Rand\nUSD: Biden Dollar\nMXN: Mexican Peso\nSGD: Singapore Dollar\nAUD: Vân Dollar\nILS: Israeli New Shekel\nKRW: S.Korea Won\nPLN: Polish złoty\nVND: Best currency"
          embed = discord.Embed(title='Loại tiền tệ được hỗ trợ', description=des, color=discord.Color.random())
          msg = await ctx.send(embed=embed)
          await msg .add_reaction("🗑️")

        def check(reaction, user):
            return user == ctx.author

        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await msg.delete()

def setup(client):
    client.add_cog(Misc(client))