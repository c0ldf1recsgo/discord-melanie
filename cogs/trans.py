# pylint: disable=relative-beyond-top-level
import googletrans
from typing import Optional

from .func import translate

from discord.ext import commands

BULLET = ' • '
INVISIBLE = '‎'
NUMBER_EMOTES = [':zero', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':ten:']

class Trans(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.translator = googletrans.Translator()

    @commands.command(aliases=['trans', 'tr', 'translate'])
    async def translator(self, ctx, src2dest:Optional[translate.Src2Dest]='auto>vi', *, text=None):
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

def setup(client):
    client.add_cog(Trans(client))
