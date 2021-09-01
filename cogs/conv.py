# pylint: disable=unused-variable

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import json
import urllib.request as r

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://blah-blah-blah")

db = cluster['discord']['data']

def get_prefix():
    prefixid = db.find_one({"id": 'prefix'})
    prefix = prefixid['value']
    return prefix

def convert_len(val, unit_in, unit_out):
    SI = {'mm':1000, 'cm':100, 'm':1.0, 'km':0.001, 'dm':10, 'nm':1000000000, 'mi':0.000621371, 'yd':1.09361296, 'ft':3.2808388799999997, 'in':39.370066559999997935}
    try:
        return round(val*SI[unit_out]/SI[unit_in], 6)
    except:
        return 'n/a'

def convert_area(val, unit_in, unit_out):
    SI = {'mm2':1000000, 'cm2':10000, 'm2':1.0, 'km2':0.000001, 'mi2':0.0000003861022, 'yd2':1.19599, 'ft2':10.76391, 'in2':1550.003, 'ha':0.0001}
    try:
        return round(val*SI[unit_out]/SI[unit_in], 6)
    except:
        return 'n/a'

def convert_weight(val, unit_in, unit_out):
    SI = {'g':1000, 't':0.001, 'kg':1.0, 'ta':0.01, 'yen':0.1, 'mg':1000000, 'lb':2.20462, 'oz':35.2739199982575}
    try:
        return round(val*SI[unit_out]/SI[unit_in], 6)
    except:
        return 'n/a'

def convert_speed(val, unit_in, unit_out):
    SI = {'mps':1.0, 'kph':3.6, 'mph':2.23694, 'ftps':3.2808453346457, 'kps':0.001}
    try:
        return round((val*SI[unit_out]/SI[unit_in]), 6)
    except:
        return 'n/a'

def convert_time(val, unit_in, unit_out):
    SI = {'min':1440, 'hr':24, 'sec':86400, 'ms':86400000, 'day':1, 'wk':0.142857, 'mon':0.032876643423, 'yrs':0.0027397232876831892345, 'hour':24, 'hours':24, 'week':0.142857, 'years':0.0027397232876831892345, 'year':0.0027397232876831892345, 'month':0.032876643423}
    try:
        return round(val*SI[unit_out]/SI[unit_in], 6)
    except:
        return 'n/a'

def convert_temp(val, unit_in, unit_out):
    if unit_in.lower() == 'c' and unit_out.lower() == 'f':
        return round(((val * (9/5)) + 32), 2)
    elif unit_in.lower() == 'f' and unit_out.lower() == 'c':
        return round(((val - 32) * (5/9)), 2)
    elif unit_in.lower() == 'f' and unit_out.lower() == 'k':
        return round( ((val - 32) * (5/9) + 273.15), 2 )
    elif unit_in.lower() == 'k' and unit_out.lower() == 'f':
        return round(((val - 273.15) * (9/5) + 32), 2)
    elif unit_in.lower() == 'c' and unit_out.lower() == 'k':
        return round((val + 273.15), 2)
    elif unit_in.lower() == 'k' and unit_out.lower() == 'c':
        return round((val - 273.15), 2)
    else:
        return 'n/a'

def convert_data(val, unit_in, unit_out):
    bit = 'n/a'
    if unit_in.lower() ==unit_out.lower():
        return val
    if unit_in.lower() == 'dec':
        try:
            val = int(val)
        except:
            return 'n/a'
        if unit_out.lower() == 'bin':
            bit = str(bin(val))[2:]
        elif unit_out.lower() == 'hex':
            bit = str(hex(val))[2:]
        elif unit_out.lower() == 'oct':
            bit = str(oct(val))[2:]
    elif unit_in.lower() == 'bin':
        if unit_out.lower() == 'dec':
            try:
                bit = str(int(str(val), 2))
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số nhị phân.'
        if unit_out.lower() == 'hex':
            try:
                bit = str(hex(int(str(val), 2))[2:])
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số nhị phân.'
        if unit_out.lower() == 'oct':
            try:
                bit = str(oct(int(str(val), 2))[2:])
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số nhị phân.'
    elif unit_in.lower() == 'hex':
        if unit_out.lower() == 'dec':
            try:
                bit = str(int(str(val), 16))
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số thập lục phân.'
        if unit_out.lower() == 'bin':
            try:
                bit = str(bin(int(str(val), 16))[2:])
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số thập lục phân.'
        if unit_out.lower() == 'oct':
            try:
                bit = str(oct(int(str(val), 16))[2:])
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số thập lục phân.'
    elif unit_in.lower() == 'oct':
        if unit_out.lower() == 'dec':
            try:
                bit = str(int(str(val), 8))
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số bát phân.'
        if unit_out.lower() == 'bin':
            try:
                bit = str(bin(int(str(val), 8))[2:])
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số bát phân.'
        if unit_out.lower() == 'hex':
            try:
                bit = str(hex(int(str(val), 8))[2:])
            except:
                bit = 'Kiểm tra lại nào, đây không phải là số bát phân.'

    return bit


def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def conv_cur(rate, _to, _from):
	return (rate * _from / _to)

class Convert(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['conv'])
    @cooldown(1, 5, BucketType.user)
    async def convert(self, ctx, *args):
        print(ctx.author)
        print('convert')
        if not args:
            pass
        elif len(args) != 3:
            await ctx.send('Sai cú pháp rồi. Xem lại lệnh `help convert` nhé')
        elif '>' not in args[1]:
            await ctx.send('Để đổi đơn vị thì cần biết đó là đơn vị gì mới đổi được chứ đồ khùng này.')
        elif args[1].count('>') > 1:
            await ctx.send('Tính trêu tôi à. Sai cú pháp rồi.')
        elif args[0].lower() != 'data':
            if isInt(args[2]) or isFloat(args[2]):
                if args[1][0] == '>' or args[1][-1] == '>':
                    await ctx.send('Phải là [cái-gì-đó-1]>[cái-gì-đó-2] mới đúng nghe chưa.')
                    return
                else:
                    src = args[1].split('>')[0]
                    dest = args[1].split('>')[1]
                    val = float(args[2])
                    res = 'n/a'
                    if args[0].lower() == 'len' or args[0].lower() == 'lenght':
                        res = convert_len(val, src, dest)
                    elif args[0].lower() == 'area':
                        res = convert_speed(val, src, dest)
                    elif args[0].lower() == 'speed' or args[0].lower() == 'spd':
                        res = convert_speed(val, src, dest)
                    elif args[0].lower() == 'time':
                        res = convert_time(val, src, dest)
                    elif args[0].lower() == 'weight' or args[0].lower() == 'wei':
                        res = convert_weight(val, src, dest)
                    elif args[0].lower() == 'temp':
                        res = convert_temp(val, src, dest)
                    else:
                        await ctx.send('Loại đo lường không tồn tại. :/') 
                        return
                    if res == 'n/a':
                        await ctx.send('Đơn đo lường không tồn tại hoặc đơn vị không thuộc loại này. :/') 
                        return
                    await ctx.send(f'**Kết quả:** {val}`{src}` = {res}`{dest}`.') 
            else:
                await ctx.send('Chuyển đổi thì cần phải là số nghe chưa.')
                return
        elif args[0].lower() == 'data':
            if '.' in args[2]:
                await ctx.send('Hiện tại mình chưa học xử lý số float. Để sau bạn nhé.')
                return
            if args[1][0] == '>' or args[1][-1] == '>':
                await ctx.send('Phải là [cái-gì-đó-1]>[cái-gì-đó-2] mới đúng nghe chưa.')
                return
            else:
                src = args[1].split('>')[0]
                dest = args[1].split('>')[1]
                val = args[2]
                res = convert_data(val, src, dest)
                if res == 'n/a':
                    await ctx.send('Đơn vị này không phải là dạng dataType nhé.')
                    return
                await ctx.send(f'**Kết quả:** {val} `({src})` = {res} `({dest})`.')
        else:
            await ctx.send('Chắc lại sai cú pháp gì đó rồi.')


    @commands.command(aliases=['units'])
    @cooldown(1, 5, BucketType.user)
    async def unit(self, ctx):
        embed = discord.Embed(title="Các đơn vị được hỗ trợ", color=0x00ff00)
        embed.add_field(name='Độ dài (len, lenght)', value='mm , cm , m , km , dm , nm , mi , yd , ft , in', inline=False)
        embed.add_field(name='Diện tích (area)', value='mm2 , cm2 , m2 , km2 , mi2 , yd2 , ft2 , in2, ha', inline=False)
        embed.add_field(name='Cân nặng (wei, weight)', value='t , ta , yen , kg , g , mg , lb , oz', inline=False)
        embed.add_field(name='Vận tốc/Tốc độ (speed, spd)', value='mps , mph , kps , kph , ftps', inline=False)
        embed.add_field(name='Thời gian (time)', value='day , mon , yrs , wk , hrs , min , sec , ms', inline=False)
        embed.add_field(name='Nhiệt độ (temp)', value='c (celsius) , f (fahrenheit) , k (kelvin)', inline=False)
        embed.add_field(name='Kiểu dữ liệu (data)', value='hex (10), bin (2), dec (16), oct (8)', inline=False)
        # embed.add_field(name='Thời gian', value='Đang phát triển', inline=False)
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("✅")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅' and reaction.message == msg
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await msg.delete()


    @commands.command(aliases=['cur'])
    @cooldown(1, 5, BucketType.user)
    async def currency(self, ctx, *args):
        print(ctx.author.id)
        print('money exchange')
        json_url = "http://api.exchangeratesapi.io/v1/latest?access_key=74d31b7c6928a5fcd4c6739d182945f3&format=1"
        response = r.urlopen(json_url)
        data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        array = data['rates']

        if not args or len(args) > 3:
            await ctx.send('Sai cú pháp ròi.')
        elif len(args) == 1:
            if args[0].isnumeric() or isFloat(args[0]):
                src = 'USD'
                dest = 'VND'
                money = round(conv_cur(float(args[0]), array[src.upper()], array[dest.upper()]))
                embed = discord.Embed(title="💵 Bạn đang chuyển đổi tiền tệ", description=f'`{src.upper()}`:  {"{0:,}".format(float(args[0]))}\n`{dest.upper()}`:  {"{0:,}".format(money)}', color=discord.Color.random())
                await ctx.send(embed=embed)
            else:
                await ctx.send('Để đổi tiền thì cần nhập vào loại tiền hoặc số tiền cần đổi hiểu chưa, xem hướng dẫn đi man.')
        elif len(args) == 2 and '>' not in args[0]:
            await ctx.send('Để đổi tiền thì cần nhập vào loại tiền cần đổi sang loại tiền nào hiểu chưa, xem hướng dẫn đi man.')
        elif len(args) < 2:
            await ctx.send(f"Cần nhập đơn vị tiền vào sau lệnh. VD: `{get_prefix()[0]}cur [số tiền]` `USD` `VND`")
        elif not (args[1].isnumeric() or isFloat(args[1])):
            await ctx.send('Số tiền phải là kiểu *int* hoặc *float*.')
        else:
            src = args[0].split('>')[0]
            dest = args[0].split('>')[1]
            if dest == '':
                dest = 'VND'
            if src == '':
                src = 'USD'
            if (str(src).upper() not in array) or (str(dest).upper() not in array):
                await ctx.send(
                    "Chưa hỗ trợ chuyển đổi loại tiền tệ này nhé. Xem lệnh `curs` để xem danh sách loại tiền được hỗ trợ."
                )
            else:
                money = round(conv_cur(float(args[1]), array[src.upper()], array[dest.upper()]))
                embed = discord.Embed(title="💵 Bạn đang chuyển đổi tiền tệ", description=f'`{src.upper()}`:  {"{0:,}".format(float(args[1]))}\n`{dest.upper()}`:  {"{0:,}".format(money)}', color=discord.Color.random())
                await ctx.send(embed=embed)


    @commands.command(aliases=['curs'])
    @cooldown(1, 5, BucketType.user)
    async def currencies(self, ctx, *args):
        print(ctx.author.id)
        print('sent currencies')
        if not args:
            des = "Nhiều lắm không kể hết được nên hãy dùng google để tìm xem nhớ <3. Hoặc vào link này:\nhttps://exchangeratesapi.io/currencies/"
            embed = discord.Embed(title='Loại tiền tệ được hỗ trợ',
                                description=des,
                                color=discord.Color.random())
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("🗑️")

        def check(reaction, user):
            return user == ctx.author

        reaction, user = await self.client.wait_for('reaction_add',
                                                    check=check)
        await msg.delete()


def setup(client):
    client.add_cog(Convert(client))
