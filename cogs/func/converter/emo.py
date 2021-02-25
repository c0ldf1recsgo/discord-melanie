import discord

from discord.ext import commands

class NitroEmojiConverter(commands.PartialEmojiConverter):
    async def convert(self, ctx, arg):
        no_colon = arg.replace(':', '')
        emoji = discord.utils.get(ctx.bot.emojis, name=no_colon)
        if not emoji:
            try: emoji = await super().convert(ctx, arg)
            except: emoji = no_colon
        return emoji

emoji_converter = NitroEmojiConverter()
async def convert(ctx, arg):
    return await emoji_converter.convert(ctx, arg)