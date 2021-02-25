import json
import requests

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


def get_quote():
  reponse = requests.get('http://zenquotes.io/api/random')
  json_data = json.loads(reponse.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


class Quote(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Events

    # Commands
    @commands.command(aliases=['quotes', 'inspire', 'q'])
    @cooldown(1, 3, BucketType.user)
    async def quote(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            print(ctx.author.id)
            quote = get_quote()
            await ctx.channel.send(quote)
            print('sent quotes')
        else:
            ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(Quote(client))