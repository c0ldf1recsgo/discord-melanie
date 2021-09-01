import typing
from pymongo import MongoClient

import random

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord_slash import cog_ext, SlashContext

bot_channel = [706457437405708288, 814344317882597406]
# bot_channel_test = 814344317882597406
talk_channel = [797018066928009249, 705598305857437696, 761065872613703680, 705277306536591420, 706001347887104051, 706004773282906154, 706108774401703956, 707151882694688768, 706826942288232479, 705284188324102245, 712288193453490266, 719502190367997953, 814344317882597406]

cluster = MongoClient("mongodb+srv://blah-blah-blah")

levelling = cluster['discord']['levelsystem']

class Level(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._cd = commands.CooldownMapping.from_cooldown(1, 45.0, commands.BucketType.member)

    
    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channel:
            ratelimit = self.get_ratelimit(message)
            if ratelimit is None:
                stats = levelling.find_one({"id": message.author.id})
                if not message.author.bot:
                    if stats is None:
                        newuser = {"id": message.author.id, "xp": 100, "noti":1}
                        levelling.insert_one(newuser)
                    else:
                        old_xp = stats["xp"]
                        old_lvl = 0
                        while True:
                            if old_xp < ((50*(old_lvl**2)) + (50*(old_lvl-1)) + 50):
                                break
                            old_lvl += 1
                        xp = stats["xp"] + random.randint(4,8)
                        levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
                        lvl = 0
                        while True:
                            if xp < ((50*(lvl**2)) + (50*(lvl-1)) + 50):
                                break
                            lvl += 1
                        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)) + 50)
                        # if xp == 0:
                        # print(old_lvl, lvl)
                        noti = stats["noti"]
                        if old_lvl < lvl and noti == 1:
                            _channel = self.client.get_channel(706457437405708288)
                            await _channel.send(f"Chúc mừng {message.author.mention}! Bạn vừa đạt **Cấp {lvl-1}** :diamond_shape_with_a_dot_inside:!")
    

    @commands.command(aliases=['lvl'])
    @cooldown(1, 5, BucketType.user)
    async def level(self, ctx, member:typing.Optional[discord.Member]=None):
        print(ctx.author.id)
        print('sent level')
        if ctx.channel.id in bot_channel:
            member = member or ctx.author
            stats = levelling.find_one({"id": member.id})
            if stats is None:
                embed = discord.Embed(description="Cần gửi tin nhắn ở Mục Kênh Chat trước nhé.") 
                await ctx.send(embed=embed)  
            else:
                xp = stats["xp"]
                lvl = 0
                while True:
                    if xp < ((50*(lvl**2)) + (50*lvl)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
                # boxes = int((xp/(200*((1/2) * lvl))) * 20)
                float_boxes = (xp/(200*((1/2) * lvl))) * 10
                ranking = levelling.find().sort("xp", -1)
                i=1
                temprank = 0
                for x in ranking:
                    if str(member.id) == str(x['id']):
                        temprank = i
                        break
                    else:
                        i+=1
                embed = discord.Embed(title=f"Cấp độ của {member.name}", color=discord.Color.blue())
                embed.add_field(name="Tên", value=member.mention, inline=True)
                embed.add_field(name="Cấp", value=lvl-1, inline=True)
                embed.add_field(name="Hạng", value=temprank, inline=True)
                embed.add_field(name="XP", value=f'{xp}/{int(200*((1/2)*lvl))}', inline=True)
                if (float_boxes % 1) < 0.5:
                  embed.add_field(name="Tiến trình:", value=int(float_boxes) * ":full_moon:" + (10-int(float_boxes)) * ":new_moon:", inline=False)
                else:
                  embed.add_field(name="Tiến trình:", value=int(float_boxes) * ":full_moon:"+ ':last_quarter_moon:' + (10-int(float_boxes)) * ":new_moon:", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)


    @commands.command(aliases=['levels', 'rank'])
    @cooldown(1, 5, BucketType.user)
    async def leaderboard(self, ctx, *args):
        print(ctx.author.id)
        print('sent leaderboard')
        if (ctx.channel.id) in bot_channel:
            if not args:
                ranking = levelling.find().sort("xp", -1)
                i=1
                embed = discord.Embed(title="Xếp hạng", color=discord.Color.purple())
                for x in ranking:
                    try:
                        temp = ctx.guild.get_member(x["id"])
                        tempxp = x["xp"]
                        if tempxp >= 10000:
                            tmp = tempxp/1000
                            embed.add_field(name=f"{i}: {temp.name}", value =f"Total XP: {round(tmp,1)}k", inline=False)
                        else:
                            embed.add_field(name=f"{i}: {temp.name}", value =f"Total XP: {tempxp}", inline=False)
                        i += 1
                    except:
                        pass
                    if i == 11:
                        break
            elif args[0].isnumeric() and int(args[0]) >= 15:    
                ranking = levelling.find().sort("xp", -1)
                i=1
                embed = discord.Embed(title="Xếp hạng", color=discord.Color.purple())
                for x in ranking:
                    try:
                        temp = ctx.guild.get_member(x["id"])
                        tempxp = x["xp"]
                        if tempxp >= 10000:
                            tmp = tempxp/1000
                            embed.add_field(name=f"{i}: {temp.name}", value =f"Total XP: {round(tmp,1)}k", inline=False)
                        else:
                            embed.add_field(name=f"{i}: {temp.name}", value =f"Total XP: {tempxp}", inline=False)
                        i += 1
                    except:
                        pass
                    if i == 16:
                        break
            

            _msg = await ctx.send(embed=embed)
            await _msg.add_reaction("🤘")
            def check(reaction, user):
                return user == ctx.author and reaction.message == _msg

            reaction = None

            while True:
                if str(reaction) == '🤘':
                    await _msg.delete()
                
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
                    await _msg.remove_reaction(reaction, user)
                except:
                    break
            

    @commands.command(aliases=['levelupd', 'lvlupd'])
    async def levelupdisable(self, ctx, *args):
        if not args:
            stats = levelling.find_one({"id": ctx.author.id})
            noti = stats["noti"]
            if noti == 1:
                levelling.update_one({"id":ctx.author.id}, {"$set":{"noti":0}})
                await ctx.send('Đã tắt thông báo lên cấp. Bật lại bằng lệnh `levelupenable` nhé.')
            else:
                await ctx.send('Thông báo lên cấp đã tắt. Bật lại bằng lệnh `levelupenable` nhé.')
        else:
            pass


    @commands.command(aliases=['levelupe', 'lvlupe'])
    async def levelupenable(self, ctx, *args):
        if not args:
            stats = levelling.find_one({"id": ctx.author.id})
            noti = stats["noti"]
            if noti == 0:
                levelling.update_one({"id":ctx.author.id}, {"$set":{"noti":1}})
                await ctx.send('Đã bật thông báo lên cấp. Tắt đi bằng lệnh `levelupdisable` nhé.')
            else:
                await ctx.send('Thông báo lên cấp đã bật sẵn. Tắt đi bằng lệnh `levelupdisable` nhé.')
        else:
            pass


    @cog_ext.cog_slash(name="lvldisable", description="Tắt thông báo lên cấp")
    async def _levelupdisable(self, ctx: SlashContext):
        stats = levelling.find_one({"id": ctx.author.id})
        noti = stats["noti"]
        if noti == 1:
            levelling.update_one({"id":ctx.author.id}, {"$set":{"noti":0}})
            await ctx.send('Đã tắt thông báo lên cấp. Bật lại bằng lệnh `levelupenable` nhé.')
        else:
            await ctx.send('Thông báo lên cấp đã tắt. Bật lại bằng lệnh `levelupenable` nhé.')


    @cog_ext.cog_slash(name="lvlenable", description="Bật thông báo lên cấp")
    async def _levelupenable(self, ctx: SlashContext):
        stats = levelling.find_one({"id": ctx.author.id})
        noti = stats["noti"]
        if noti == 0:
            levelling.update_one({"id":ctx.author.id}, {"$set":{"noti":1}})
            await ctx.send('Đã bật thông báo lên cấp. Tắt đi bằng lệnh `levelupdisable` nhé.')
        else:
            await ctx.send('Thông báo lên cấp đã bật sẵn. Tắt đi bằng lệnh `levelupdisable` nhé.')


    @commands.command()
    @commands.is_owner()
    async def addxp(self, ctx, member:typing.Optional[discord.Member]=None, *, xp_add=0):
        if not member:
            pass
        elif not xp_add:
            pass
        else:
            print(member.id)
            stats = levelling.find_one({"id": member.id})
            xp = stats["xp"] + xp_add
            levelling.update_one({"id":member.id}, {"$set":{"xp":xp}})
            await ctx.send(f'Added {xp_add} to user {member.id}')

    
    @commands.command()
    @commands.is_owner()
    async def subxp(self, ctx, member:typing.Optional[discord.Member]=None, *, xp_sup=0):
        if not member:
            pass
        elif not xp_sup:
            pass
        else:
            print(member.id)
            stats = levelling.find_one({"id": member.id})
            xp = stats["xp"] - xp_sup
            levelling.update_one({"id":member.id}, {"$set":{"xp":xp}})
            await ctx.send(f'Removed {xp_sup} exp from {member}')



def setup(client):
    client.add_cog(Level(client))
