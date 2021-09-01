# pylint: disable=relative-beyond-top-level
# pylint: disable=unused-variable
# Inspired by https://github.com/DleanJean

import typing
import io
from .func import timeedit
from .func import utils

import discord
from discord.ext import commands

SAVE_LIMIT = 15
DELETED = 'deleted'
EDITED = 'edited'

def get_extra(msg):
    extra = get_attachment_links(msg)
    for i in msg.embeds:
        num = str(i+1) if len(msg.embeds) > 1 else str(0)
        embed = f'**[**{num}**]**'
        extra += [embed]
    return ' '.join(extra)

def get_attachment_links(msg, text='File'):
    links = []
    count = len(msg.attachments)
    for i, a in enumerate(msg.attachments):
        num = str(i+1) if count > 1 else ''
        link = f'[[{text}{num}]]({a.proxy_url})'
        links += [link]
    return links

def get_time_display(m, state):
    message_time = m.edited_at if state == EDITED and m.edited_at else m.created_at
    display_format = timeedit.HOUR if timeedit.is_today(message_time) else timeedit.DAY_HOUR
    message_time = timeedit.to_ict(message_time, display_format)
    return message_time

class ChannelLog:
    def __init__(self):
        self.deleted = []
        self.edited = []
    
    def get_list(self, state):
        return getattr(self, state)[-SAVE_LIMIT:]
    
    def log(self, state, message):
        msgs = self.get_list(state)
        msgs.append(message)
        setattr(self, state, msgs)
    
    def log_deleted(self, message): self.log(DELETED, message)
    def log_edited(self, message): self.log(EDITED, message)

    def get_last(self, state, index):
        try:
            return self.get_list(state)[-index]
        except:
            return None

class Spy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel_logs = {}
        self.backup_files = {}
    
    async def send_message_in_embed(self, ctx, channel, state, index):
        channel = channel or ctx.channel
        if index > SAVE_LIMIT:
            await ctx.send("Bạn chỉ snipe được tối đa 15 tin nhắn thôi nhó.")
            return
        msg = self.get_last_message(channel, state, index)

        embed = self.create_empty_embed(channel, state)
        files = []
        if msg:
            await self.embed_message_log(embed, msg, state, channel)
            files = await self.get_backup_files(msg, embed)

        mesg = await ctx.send(embed=embed, files=files)

        if msg and msg.embeds:
            mesg = await ctx.send(embed=msg.embeds[0])

        await mesg.add_reaction("🗑️")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🗑️' and reaction.message == mesg
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await mesg.delete()
    
    def get_last_message(self, channel, state, index):
        log = self.channel_logs.get(channel.id)
        msg = log.get_last(state, index) if log else None
        return msg

    def create_empty_embed(self, channel, state):
        embed = discord.Embed(description='', color=discord.Color.red())
        if state == 'deleted':
            embed.description = 'Không có tin nhắn nào bị xóa.'
        else:
            embed.description = 'Không có tin nhắn nào được sửa.'
        embed.set_author(name='Tại #' + channel.name)
        return embed
    
    async def embed_message_log(self, embed, msg, state, channel):
        embed.set_author(name=str(msg.author), icon_url=msg.author.avatar_url)
        embed.description = msg.content or msg.system_content or ''
        embed.timestamp = msg.created_at
        if state == 'deleted':
            embed.set_footer(text=f'Đã xóa tại #{channel.name}')
        else:
            embed.set_footer(text=f'Đã sửa tại #{channel.name}')
        
        if not msg.attachments: return

        url = msg.attachments[0].proxy_url
        embed.set_image(url=url)

        links = get_attachment_links(msg, 'Link')
        embed.description += '\n' + ' '.join(links)

    async def get_backup_files(self, msg, embed):
        accessible = embed.image and await utils.download(embed.image.url, utils.READ)
        multiple_files = len(msg.attachments) > 1
        if accessible and not multiple_files: return []

        files = self.backup_files.get(msg.id, {})
        files = [discord.File(io.BytesIO(data), name) for name, data in files.items()]
        if files:
            embed.set_image(url='')
        return files

    async def send_log_in_embed(self, ctx, channel, state):
        log = self.channel_logs.get(channel.id)
        embed = self.create_empty_embed(channel, state)
        self.embed_channel_logs(embed, log, state)

        mesg = await ctx.send(embed=embed)

        await mesg.add_reaction("🗑️")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🗑️' and reaction.message == mesg
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await mesg.delete()

    def embed_channel_logs(self, embed, channel_log, state):
        if not channel_log: return

        prev_msg = None
        msgs = []
        logged_msgs = channel_log.get_list(state)

        for i, m in enumerate(logged_msgs):
            extra = get_extra(m)
            time = get_time_display(m, state)

            # snipe_index = min(len(logged_msgs), 10) - i
            # msg = f'**{snipe_index}:** {msg}'
            if len(m.content) > 1024:
                msg = f'`{time}`: {m.content[:15]} ..... {m.content[-15:]} {extra}'
            else:
                msg = f'`{time}`: {m.content} {extra}'
            author_first_msg = not prev_msg or prev_msg.author != m.author
            if author_first_msg:
                # next_msg_same_author = i + 1 < len(logged_msgs) and logged_msgs[i+1].author == m.author
                # sep = '\n' if next_msg_same_author else ' '
                # msg = f'{m.author.mention}{sep}{msg}'
                msg = f'{m.author.mention}\n{msg}'
            msgs += [msg]

            prev_msg = m
        
        if msgs:
            

            embed.description = '\n'.join(msgs)

    def get_or_create_log(self, channel):
        if channel.id not in self.channel_logs:
            self.channel_logs[channel.id] = ChannelLog()
        return self.channel_logs[channel.id]

    # Commands
    @commands.command(hidden=True, aliases=['repe'])
    @commands.guild_only()
    # repeatedit
    async def rep(self, ctx, channel:typing.Optional[discord.TextChannel], i=1):
        channel = channel or ctx.channel
        msg = self.get_last_message(channel, EDITED, i)
        if msg:
            mesg = await ctx.send(msg.content, embed=msg.embeds[0] if msg.embeds else None)
        else:
            mesg = await ctx.send(embed=self.create_empty_embed(channel, EDITED))

        await mesg.add_reaction("🗑️")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🗑️' and reaction.message == mesg
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await mesg.delete()
    
    @commands.command(aliases=['spy'])
    @commands.guild_only()
    async def snipe(self, ctx, channel:typing.Optional[discord.TextChannel], i=1):
        print(ctx.author.id)
        print('sent snipe')
        await self.send_message_in_embed(ctx, channel, DELETED, i)
    
    @commands.command(aliases=['editsnipe', 'spyedit', 'spye'])
    @commands.guild_only()
    async def snipedit(self, ctx, channel:typing.Optional[discord.TextChannel], i=1):
        print(ctx.author.id)
        print('sent edited')
        await self.send_message_in_embed(ctx, channel, EDITED, i)
    
    @commands.command(aliases=['unkolsh', 'spyl', 'snipel', 'spylog'])
    @commands.guild_only()
    async def snipelog(self, ctx, channel:discord.TextChannel=None):
        print(ctx.author.id)
        print('sent spylog')
        await self.send_log_in_embed(ctx, channel or ctx.channel, DELETED)
    
    @commands.command(aliases=['editl'])
    @commands.guild_only()
    async def editlog(self, ctx, channel:discord.TextChannel=None):
        print(ctx.author.id)
        print('sent editlog')
        await self.send_log_in_embed(ctx, channel or ctx.channel, EDITED)
    
    # Event
    @commands.Cog.listener()
    async def on_message(self, msg):
        files = { a.filename: await a.read() for a in msg.attachments }
        if files:
            self.backup_files[msg.id] = files

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if not msg.guild or msg.author == self.client.user: return
        self.get_or_create_log(msg.channel).log_deleted(msg)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.author == self.client.user: return
        self.get_or_create_log(before.channel).log_edited(before)
    
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, msgs):
        for m in msgs:
            self.get_or_create_log(m.channel).log_deleted(m)


def setup(bot):
    bot.add_cog(Spy(bot))
