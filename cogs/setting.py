from typing import Optional

from replit import db

import discord
from discord.ext import commands

class Setting(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command()
    async def ping(self, ctx, *args):
        print(ctx.author.id)
        print('sent ping')
        if ctx.author == self.client.user:
            return
        if not args:
            await ctx.send('Pong! Replied in {0}ms'.format(round(self.client.latency * 1000)))


    @commands.command(aliases=['prefix'])
    async def prefixedit(self, ctx, *args):
        new_prefix = ' '.join(args)
        print(ctx.author.id)
        print('change prefix')
        if not args:
            await ctx.send('Vui lòng nhập prefix bạn muốn vào.')
        else:
            role = discord.utils.get(ctx.guild.roles, name="Moderator")
            role2 = discord.utils.get(ctx.guild.roles, name="Administrator")
            role3 = discord.utils.get(ctx.guild.roles, name="Owner")
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                # with open('./cogs/prefixes.json', 'r') as f:
                #     prefixes = json.load(f)
                # prefixes['prefix'] = new_prefix

                # with open('./cogs/prefixes.json', 'w') as f:
                #     json.dump(prefixes, f, indent=4)
                db['prefix'] = [new_prefix]
                    
                await ctx.send(f'Prefix đã được đổi thành `{new_prefix}`')
            else:
                await ctx.send('Bạn làm gì có quyền sửa prefix hihi.')


    @commands.command(aliases=['nickname'])
    async def nick(self, ctx, member: Optional[discord.Member]=None, *args):
        print(ctx.author.id)
        if not args:
            await ctx.send('Điền thêm tên vào nhó.')
            print('Changed nick name failed')
        else:
            if (str(ctx.author) != str(member)):
                role = discord.utils.get(ctx.guild.roles, name="Moderator")
                role2 = discord.utils.get(ctx.guild.roles, name="Administrator")
                role3 = discord.utils.get(ctx.guild.roles, name="Owner")
                if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                    try:
                        nick = ' '.join(args)
                        await member.edit(nick=nick)
                        await ctx.send(f'Nickname của {member} đã được đổi thành {nick}')
                        print('Changed nick name')
                    except:
                        await ctx.send('I need permission to Manage Nicknames.')
                        print('Changed nick name failed')
                else:
                    await ctx.send('Bạn không có quyền đổi nickname của người khác.')
                    print('Changed nick name failed')
            else:
                try:
                    nick = ' '.join(args)
                    await member.edit(nick=nick)
                    await ctx.send(f'Nickname của {member.mention} đã được đổi thành {nick}')
                    print('Changed nick name')
                except:
                    await ctx.send('I need permission to Manage Nicknames.')
                    print('Changed nick name failed')

def setup(client):
    client.add_cog(Setting(client))