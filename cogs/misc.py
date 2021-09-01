# pylint: disable=relative-beyond-top-level
import random
import json
import pytz
import os
import re
import requests
from datetime import datetime
from typing import Optional

from googlesearch import search
# from bs4 import BeautifulSoup
import urllib.request as r


from .func import converter as conv

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://blah-blah-blah")

db = cluster['discord']['data']

# def get_prefix():
#     prefixid = db.find_one({"id": 'prefix'})
#     prefix = prefixid['value']
#     return prefix

SHIP_TEXT = ["target_a thích target_b rất nhiều", "target_b lao đến bên target_a, target_b ôm lấy target_a và nói khẽ với target_a rằng: *iu cậu*", "Hãy nói yêu target_b đi target_a", "Bỗng một ngày, target_a chợt nhận ra con tim mình yếu mềm, target_b đã đi đến bên target_a, trao cho target_a một cái ôm nồng ấm và nói rằng: *Mãi bên nhau bạn nhó*", "Trứng rán cần mỡ, bắp cần bơ, yêu không cần cớ, target_b cần target_a cơ."]

def gen_ship_text(target_a, target_b, shiptext):
    context = random.choice(shiptext)
    text = context.replace("target_a", target_a)
    text = text.replace("target_b", target_b)
    return text


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
	numw = [
	    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
	    'zero'
	]
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


def deg2dir(deg):
	dir = ''
	if deg >= 337.5 and deg <= 22.5:
		dir = 'Bắc'
	elif deg >= 292.5 and deg <= 337.5:
		dir = 'Tây Bắc'
	elif deg >= 247.5 and deg <= 292.5:
		dir = 'Tây'
	elif deg >= 202.5 and deg <= 247.5:
		dir = 'Tây Nam'
	elif deg >= 157.5 and deg <= 202.5:
		dir = 'Nam'
	elif deg >= 112.5 and deg <= 157.5:
		dir = 'Đông Nam'
	elif deg >= 67.5 and deg <= 112.5:
		dir = 'Đông'
	elif deg >= 22.5 and deg <= 67.5:
		dir = 'Đông Bắc'
	return dir


def convert_timestamp_in_datetime_utc(timestamp_received):
    dt_naive_utc = datetime.utcfromtimestamp(timestamp_received)
    return dt_naive_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))


def translateWeather(des):
	dic = {'few clouds': 'Trời ít mây', 'clear sky': 'Trời trong sạch', 'scattered clouds':'Mây rải rác', 'broken clouds':'mây rải rác', 'shower rain':'Có mưa rào rải rác vài nơi', 'rain':'Có thể có mưa', 'thunderstorm':'Có thể có sấm chớp', 'snow':'Có tuyết nè, ra chơi thôi', 'mist':'Sương mù dày đặt', 'overcast clouds':'Trời âm u'}
	
	if des in dic.keys():
		return dic[des]
	else:
		return des


# def google_scrape(url):
#     thepage = r.urlopen(url)
#     soup = BeautifulSoup(thepage, "html.parser")
#     return soup.title.text


# Function to validate
# hexadecimal color code .
def isValidHexaCode(str):
    # Regex to check valid
    # hexadecimal color code.
    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if(str == None):
        return False

    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False


def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def check_if_it_is_me(ctx):
    return ctx.message.author.id == 394520281814925313


RGB_SCALE = 255
CMYK_SCALE = 100

def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        # black
        return 0, 0, 0, CMYK_SCALE
    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE
    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy
    # rescale to the range [0,CMYK_SCALE]
    return c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE


mes = ["Gì mậy?", "Gì tag t?", "Có gì hong em", "Sao cưng"]
MAX_COLOR = 16777215

class Misc(commands.Cog):
	def __init__(self, client):
		self.client = client

	# Events
	async def cog_before_invoke(self, ctx: commands.Context):
		if check_if_it_is_me(ctx):
			return ctx.command.reset_cooldown(ctx)

	@commands.Cog.listener()
	async def on_message(self, ctx):
		mention = str(self.client.user.id)
		# print(mention)
		if str(mention) in ctx.content:
			await ctx.channel.send(random.choice(mes))

	# Commands
	@commands.command()
	async def server(self, ctx):
		embed = discord.Embed(description="", color=discord.Color.random())
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.set_image(url=ctx.guild.icon_url)
		await ctx.send(embed=embed)


	@commands.command(aliases=['ava'])
	@cooldown(1, 3, BucketType.user)
	async def avatar(self, ctx, *, member: Optional[conv.FuzzyMember] = None):
		print(ctx.author.id)
		member = member or ctx.author
		embed = discord.Embed(description=ctx.author.display_name +
							' muốn xem ảnh của bạn',
							color=discord.Color.random())
		embed.title = str(member)
		embed.set_image(url=str(member.avatar_url).replace('webp', 'png'))
		embed.timestamp = datetime.now().astimezone()

		mesg = await ctx.send(embed=embed)

		await mesg.add_reaction("❌")
		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == '❌' and reaction.message == mesg
		reaction, user = await self.client.wait_for('reaction_add', check=check)
		await mesg.delete()

		print('sent avatar')


	@commands.command(aliases=['m', 'cal', 'tinh', 'calculate', 'math'])
	@cooldown(1, 5, BucketType.user)
	async def _math(self, ctx, *args):

		if not args:
			return
		else:
			m = ' '.join(args)
			if not any(c.isalpha() for c in m):
			# code = compile(m, "<string>", "eval")
				try:
					code = compile(m, "<string>", "eval")
					res = eval(code)
					await ctx.send(f"Kết quả: {res}")
				except:
					await ctx.send(':question: | Phép tính có vấn đề rồi.')
			else:
				# do nothing
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


	@commands.command(aliases=['wea'])
	@cooldown(1, 8, BucketType.user)
	async def weather(self, ctx, *, location='ho chi minh'):
		print(ctx.author.id, 'weathering')
		location = location.replace(' ', '+')
		# print(location)
		key = os.getenv('WEATHER')
		url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric'
		data = json.loads(requests.get(url).content)
		
		if data['cod'] == '404':
			# print('City not found.')
			embed = discord.Embed(title='Thành phố không tồn tại.', description='Vui lòng xem lại tên thành phố.', color=discord.Color.teal())
			await ctx.send(embed=embed)
		else:
			# pprint(data)
			embed = discord.Embed(title=data['name'], description=translateWeather(data['weather'][0]['description']), color=discord.Color.teal())
			embed.add_field(name=':thermometer:  Nhiệt độ', value=f"{data['main']['temp']}°C  (cảm giác như {data['main']['feels_like']}°C)", inline=False)
			embed.add_field(name=':sweat_drops:  Độ ẩm', value=f"{data['main']['humidity']} %", inline=False)
			embed.add_field(name=':dash:  Gió', value=f"Hướng {deg2dir(data['wind']['deg'])}: {data['wind']['speed']} m/s", inline=False)
			sunrise = convert_timestamp_in_datetime_utc(data['sys']['sunrise'])
			sunset = convert_timestamp_in_datetime_utc(data['sys']['sunset'])
			embed.add_field(name=':sunrise:   Mặt trời mọc', value=sunrise.strftime("%d-%m-%Y, %H:%M:%S"), inline=False)
			embed.add_field(name=':city_sunset:  Mặt trời lặn', value=sunset.strftime("%d-%m-%Y, %H:%M:%S"), inline=False)
			await ctx.send(embed=embed)


	@commands.command(aliases=['gg'])
	@cooldown(1, 120, BucketType.user)
	async def google(self, ctx, *args):
		# if(str(ctx.author.id) == '699970879144329366'):
		# 	await ctx.send(f"ShinGay à, không cho chơi nhé. Hihi")
		# 	return
		print(ctx.author.id)
		print('google search')
		# user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/94.0.202 Chrome/88.0.4324.202 Safari/537.36'
		# user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
		user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
		if not args:
			query = 'google'
			for url in search(query, tld="com", lang='vi', num=1, stop=1, pause=0, user_agent=user_agent):
				await ctx.send(f"<:google:879366862373285928> Kết quả cho *{query}*:\n" + url.replace("m.youtube", "youtube"))
				return
				# try:
				# 	a = google_scrape(url)
				# 	await ctx.send(f"Kết quả cho *{query}*:\n**{a}**\n" + url)
				# except:
				# 	await ctx.send(f"Kết quả cho *{query}*:\n" + url)
		else:
			query = " ".join(args)
			for url in search(query, tld="com", lang='vi', num=1, stop=1, pause=0, user_agent=user_agent):
				await ctx.send(f"<:google:879366862373285928> Kết quả cho *{query}*:\n" + url.replace("m.youtube", "youtube"))
				if not url:
					new_url = f"https://www.google.com/search?client=safari&rls=x64&q={'+'.join(args)}&ie=UTF-8&oe=UTF-8"
					await ctx.send(f"<:google:879366862373285928> Kết quả cho *{query}*:\n" + new_url)
					return
				# try:
				# 	a = google_scrape(url)
				# 	await ctx.send(f"Kết quả cho *{query}*:\n**{a}**\n" + url)
				# except:
				# 	await ctx.send(f"Kết quả cho *{query}*:\n" + url)


	@commands.command(aliases=['idols'])
	@cooldown(1, 10, BucketType.user)
	async def idol(self, ctx):
		role_name = 'idol'
		role = discord.utils.find( lambda r: r.name == role_name, ctx.message.guild.roles)
		des = 'Danh sách cho ' + role.mention + '\n'
		for user in ctx.message.guild.members:
			if role in user.roles:
				des += user.mention + ' - ' + user.name + '\n'

		role_name = 'idol hội chợ'
		role = discord.utils.find( lambda r: r.name == role_name, ctx.message.guild.roles)
		des += 'Danh sách cho ' + role.mention + '\n'
		for user in ctx.message.guild.members:
			if role in user.roles:
				des += user.mention + ' - ' + user.name + '\n'

		embedVar = discord.Embed(description=des, color=discord.colour.Color.green())
		await ctx.send(embed = embedVar)


	@commands.command(aliases=['ghep'])
	@cooldown(1,15, BucketType.user)
	async def ship(self, ctx, *args):
		if not args:
			await ctx.send("Cần phải có tên ai đó mới ship được nhé")
		elif ('|' not in args) or (len(args) < 3):
			embed = discord.Embed(title='Sai cú pháp',
			description='Cú pháp đúng phải là `[prefix]ship` `[target_a]` | `[target_b]`',
			color=discord.colour.Color.red())
			await ctx.send(embed=embed)
		else:
			allargs = ' '.join(args)
			targets= allargs.split(' | ')
			if len(targets) > 1 and len(targets) < 3:
				context = gen_ship_text(targets[0], targets[1], SHIP_TEXT)
				await ctx.send(context)
			else:
				embed = discord.Embed(title='Sai cú pháp',
					description='Cú pháp đúng phải là `[prefix]ship` `[target_a]` | `[target_b]`',
					color=discord.colour.Color.red())
				await ctx.send(embed=embed)


	@commands.command(aliases=['color'])
	@cooldown(1, 5, BucketType.user)
	async def colors(self, ctx, *color):
		if not color:
			await ctx.channel.send("Không có gì cả")
			return
		else:
			code = color[0]
		if '#' not in code and isInt(code):
			if int(code) > MAX_COLOR or int(code) < 0:
				await ctx.channel.send("Mã màu không hợp lệ")
				return
			else:
				val = int(code)
				hex_code = '{0:06X}'.format(val)  
				rgb_code = f'`{int(hex_code[0:2], 16)}`, `{int(hex_code[2:4], 16)}`, `{int(hex_code[4:6], 16)}`'
				c, y, m, k = rgb_to_cmyk(int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16))
				cymk_code = f'`{c}%`, `{y}%`, `{m}%`, `{k}%`'
				des = f"**HEX:**  `#{hex_code}`\n**RGB:**  {rgb_code}\n**INT:**  `{code}`\n**CYMK:**  {cymk_code}"
				url = f'https://singlecolorimage.com/get/{hex_code}/200x200'
				embed = discord.Embed(title=f'Color #{hex_code}', description=des, color=discord.Color.default())
				embed.set_thumbnail(url=url) 
				await ctx.channel.send(embed=embed)
		elif '#' in code and isValidHexaCode(code):
			hex_code = code[1:]
			int_code = int(code[1:], 16)
			rgb_code = f'`{int(hex_code[0:2], 16)}`, `{int(hex_code[2:4], 16)}`, `{int(hex_code[4:6], 16)}`'
			c, y, m, k = rgb_to_cmyk(int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16))
			cymk_code = f'`{c}%`, `{y}%`, `{m}%`, `{k}%`'
			des = f"**HEX:**  `#{hex_code}`\n**RGB:**  {rgb_code}\n**INT:**  `{int_code}`\n**CYMK:**  {cymk_code}"
			url = f'https://singlecolorimage.com/get/{hex_code}/200x200'
			embed = discord.Embed(title=f'Color #{hex_code}', description=des, color=discord.Color.default())
			embed.set_thumbnail(url=url) 
			await ctx.channel.send(embed=embed)
		elif '0x' in code and isValidHexaCode(code):
			hex_code = code[2:]
			int_code = int(code[2:], 16)
			rgb_code = f'`{int(hex_code[0:2], 16)}`, `{int(hex_code[2:4], 16)}`, `{int(hex_code[4:6], 16)}`'
			c, y, m, k = rgb_to_cmyk(int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16))
			cymk_code = f'`{c}%`, `{y}%`, `{m}%`, `{k}%`'
			des = f"**HEX:**  `#{hex_code}`\n**RGB:**  {rgb_code}\n**INT:**  `{int_code}`\n**CYMK:**  {cymk_code}"
			url = f'https://singlecolorimage.com/get/{hex_code}/200x200'
			embed = discord.Embed(title=f'Color #{hex_code}', description=des, color=discord.Color.default())
			embed.set_thumbnail(url=url) 
			await ctx.channel.send(embed=embed)
		elif ',' in code:
			# full_code = (''.join(code)).split(',')
			full_code = code.split(',')
			if (len(full_code) == 3):
				r_code = full_code[0]
				g_code = full_code[1]
				b_code = full_code[2]
				hex_code = ''
				int_code = 0
				try:
					hex_code = '%02x%02x%02x' % (int(r_code), int(g_code), int(b_code))
					int_code = int(hex_code, 16)
				except:
					await ctx.channel.send("Mã màu không hợp lệ")
					return
				rgb_code = f'`{r_code}`, `{g_code}`, `{b_code}`'
				c, y, m, k = rgb_to_cmyk(int(r_code), int(g_code), int(b_code))
				cymk_code = f'`{round(c, 2)}%`, `{round(y, 2)}%`, `{round(m, 2)}%`, `{round(k, 2)}%`'
				des = f"**HEX:**  `#{hex_code}`\n**RGB:**  {rgb_code}\n**INT:**  `{int_code}`\n**CYMK:**  {cymk_code}"
				url = f'https://singlecolorimage.com/get/{hex_code}/200x200'
				embed = discord.Embed(title=f'Color #{hex_code}', description=des, color=discord.Color.default())
				embed.set_thumbnail(url=url) 
				await ctx.channel.send(embed=embed)
			else:
				await ctx.channel.send("Mã màu không hợp lệ")
				return
		else:
			await ctx.channel.send("Mã màu không hợp lệ")
			return


def setup(client):
	client.add_cog(Misc(client))
