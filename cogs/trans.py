import googletrans
from typing import Optional

from .func import translate

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://blah-blah-blah")

collection = cluster['discord']['dict']

BULLET = ' • '
INVISIBLE = '‎'
NUMBER_EMOTES = [':zero', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':ten:']

class Trans(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.translator = googletrans.Translator()

    @commands.command(aliases=['trans', 'tr'])
    @cooldown(1, 5, BucketType.user)
    async def translate(self, ctx, src2dest:Optional[translate.Src2Dest]='auto>hcmus', *, text=None):
        print(ctx.author.id, 'translate')
        if not text:
            last_message = await ctx.history(limit=1, before=ctx.message).flatten()
            text = last_message[0].clean_content or translate.NO_TEXT
        embed = translate.translate(src2dest, text)
        await ctx.send(embed=embed)


    @commands.command(aliases=['langs', 'tls'])
    async def translatelangs(self, ctx):
        output = '**Các ngôn ngữ được hỗ trợ**:\n'
        output += BULLET.join([f'`{code}`' for code, lang in googletrans.LANGUAGES.items()])
        msg = await ctx.send(output)
        await msg.add_reaction("✅")
        def check(reaction, user):
            return user == ctx.author
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await msg.delete()


    @commands.command(aliases=['addtr'])
    @commands.is_owner()
    async def addtrans(self, ctx, *args):
        if len(args) < 1:
            await ctx.send('No input arguments')
            return
        msg = ' '.join(args)
        if ' | ' not in msg:
            await ctx.send('Wrong input arguments')
            return
        key = msg.split(' | ')[0]
        value = msg.split(' | ')[1]
        db = collection.find_one({key: {"$exists": True}})
        if db != None:
            await ctx.send('Đã tồn tại')
        else:
            db = collection.update_one({"id":'dict'}, {"$set":{key:value}})
            await ctx.send(f'Đã thêm **{key}**: {value}')

def setup(client):
    client.add_cog(Trans(client))
