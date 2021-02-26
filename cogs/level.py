import typing
from pymongo import MongoClient

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

bot_channel = [706457437405708288, 814344317882597406]
# bot_channel_test = 814344317882597406
talk_channel = [797018066928009249, 705598305857437696, 761065872613703680, 705277306536591420, 706001347887104051, 706004773282906154, 706108774401703956, 707151882694688768, 706826942288232479, 705284188324102245, 712288193453490266, 719502190367997953]

cluster = MongoClient("mongodb+srv://melanie:c0ldf1re@bot.bvo7z.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster['discord']['levelsystem']

class Level(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._cd = commands.CooldownMapping.from_cooldown(1, 6.0, commands.BucketType.member)

    
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
                        newuser = {"id": message.author.id, "xp": 100}
                        levelling.insert_one(newuser)
                    else:
                        xp = stats["xp"] + 5
                        levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
                        lvl = 0
                        while True:
                            if xp < ((50*(lvl**2)) + (50*(lvl-1))):
                                break
                            lvl += 1
                        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
                        if xp == 0:
                            _channel = self.client.get_channel(814344317882597406)
                            await _channel.send(f"Chúc mừng {message.author.mention}! Bạn vừa đạt **Cấp {lvl}** :diamond_shape_with_a_dot_inside:!")
    

    @commands.command(aliases=['lvl'])
    @cooldown(1, 5, BucketType.user)
    async def level(self, ctx):
        print(ctx.author.id)
        print('sent level')
        if ctx.channel.id in bot_channel:
            stats = levelling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(description="You haven't sent any messages.")    
                await ctx.send(embed=embed)  
            else:
                xp = stats["xp"]
                lvl = 0
                while True:
                    if xp < ((50*(lvl**2)) + (50*lvl)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl))) * 20)
                ranking = levelling.find().sort("xp", -1)
                i=1
                temprank = 0
                for x in ranking:
                  if str(ctx.author.id) == str(x['id']):
                    temprank = i
                    break
                  else:
                    i+=1
                embed = discord.Embed(title=f"Cấp độ của {ctx.author.name}", color=discord.Color.blue())
                embed.add_field(name="Tên", value=ctx.author.mention, inline=True)
                embed.add_field(name="Cấp", value=lvl-1, inline=True)
                embed.add_field(name="Hạng", value=temprank, inline=True)
                embed.add_field(name="XP", value=f'{xp}/{int(200*((1/2)*lvl))}', inline=True)
                embed.add_field(name="Tiến trình:", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

      
    @commands.command(aliases=['levels', 'rank'])
    @cooldown(1, 5, BucketType.user)
    async def leaderboard(self, ctx):
        print(ctx.author.id)
        print('sent leaderboard')
        if (ctx.channel.id) in bot_channel:
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
            _msg = await ctx.send(embed=embed)
            await _msg.add_reaction("🤘")
            def check(reaction, user):
                return user == ctx.author
            reaction, user = await self.client.wait_for('reaction_add', check=check)
            await _msg.delete()
            

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
          print(f'Added {xp_add} to user {member.id}')



def setup(client):
    client.add_cog(Level(client))