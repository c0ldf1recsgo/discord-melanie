from typing import Optional
from datetime import datetime
import json

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType


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
                with open('./cogs/prefixes.json', 'r') as f:
                    prefixes = json.load(f)
                prefixes['prefix'] = new_prefix

                with open('./cogs/prefixes.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
                    
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
            embed.add_field(name='Version:', value='`1.3.2a`', inline=False)
            
            await ctx.send(embed=embed)
        else:
            pass

def setup(client):
    client.add_cog(Setting(client))
