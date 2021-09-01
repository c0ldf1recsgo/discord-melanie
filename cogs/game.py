# pylint: disable=relative-beyond-top-level
import random
import asyncio
# import json

import discord
from discord import DMChannel
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class Talk(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['tientri', 'quest', 'yesno', '8ball', 'hoi', '8b', 'h'])
    @cooldown(1, 5, BucketType.user)
    async def _8ball(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        print(ctx.author.id)
        if not args:
            await ctx.send('Hãy nhập câu hỏi có/không (yes/no) sau lệnh bạn nhé.')
        else:
            quest = ' '.join(args)
            async with ctx.typing():
                await asyncio.sleep(2)
            answers = [
            "Chắc chắn là thế.",
            "Nó chắc chắn là như vậy.",
            "Đúng vậy, không nghi ngờ gì.",
            "Vâng, chắc chắn.",
            "Hãy tin là có.",
            "Như tớ thấy, đúng là thế.",
            "Rất có thể.",
            "Khá là có triển vọng.",
            "Không rõ lắm, hỏi lại xem nào.",
            "Tớ nghĩ tớ sẽ không trả lời đâu lew lew.",
            "Chả hiểu gì hết, không trả lời.",
            "Hỏi lại xem nào.",
            "Đừng trông chờ vào nó.",
            "Câu trả lời của tớ là KHÔNG.",
            "Các giác quan mách bảo rằng: KHÔNG KHÔNG và KHÔNG.",
            "Trông chẳng ổn chút nào.",
            "Điều đó đáng nghi lắm.",
            "Nghe buồn cười thế.",
            "Ối nghe mắc cười quá, thật là hài hước.",
            "Thánh chôn, hề chúa, cậu làm tớ cười ra nước mắt rồi này.",
            "Ờ.",
            "Khùng hả.",
            "Em đẹp lắm :shame:", 
            "Cậu đẹp như người yêu cũ của tớ vậy :shame:",
            "Ngủ đi hỏi hỏi cái giề :tuchoihieu:",
            "Hỏi gì nghe trầm cảm quá.",
            "Tự nghĩ ra câu trả lời đi nhé."
            ]
            if ('hay' in quest):
                ans = ['Yes', 'No', 'Có', 'Không', 'Qui', 'Non', 'Sí']
                await ctx.send(random.choice(ans))
            else:
                await ctx.send('- {0}'.format(random.choice(answers)))
        print('sent 8ball')

    @commands.command(aliases=['random', 'num'])
    @cooldown(1, 3, BucketType.user)
    async def rand(self, ctx, *args):
        print(ctx.author.id)
        if not args:
            await ctx.send('Ờ.....nhập số gì đó đi chứ.')
        elif args[0].isnumeric():
            if len(args) == 1:
                if  int(args[0]) == 0:
                    await ctx.send('Ai lại random con số 0 riêng mình nó thế này.')
                else:
                    num = random.randrange(int(args[0]))
                    await ctx.send('Con gì đây con số gì đây. ĐÓ LÀ: ' + str(num))
            elif args[1].isnumeric():
                a = int(args[0])
                b = int(args[1])
                if a < b:
                    num = random.randint(a, b)
                    await ctx.send('Con gì đây con số gì đây. ĐÓ LÀ: ' + str(num))
                elif b < a:
                    num = random.randint(b, a)
                    await ctx.send('Con gì đây con số gì đây. ĐÓ LÀ: ' + str(num))
                else:
                    await ctx.send('Hai số phải khác nhau chứ đồ ngốc')
            else:
                await ctx.send('Tui random số nguyên maà trờiiiii :(')
        else:
            await ctx.send('Tui random số nguyên maà, cho tui cái giới hạn bằng một con số nào đó đi chứ hầy. :(')
        print('sent random')


    @commands.command(aliases=['doan', 'which', 'randlist', 'choose', 'rl', 'g'])
    @cooldown(1, 3, BucketType.user)
    async def guess(self, ctx, *args):
        print(ctx.author.id)
        if not args:
            await ctx.send('Có gì đâu mà đoán....')
        else:
            idea = ['Có lẽ là :\n', 'Chắc là:\n', 'Hmmm :\n']
            allargs = ' '.join(args)
            splitted = allargs.split(' | ')
            if len(splitted) > 1:
                await ctx.send(random.choice(idea) + '**' + random.choice(splitted) + '**')
            else:
                await ctx.send('Cần ít nhất 2 lựa chọn nhé.\n')
        print('sent guess')

def setup(client):
    client.add_cog(Talk(client))
