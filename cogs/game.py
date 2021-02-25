# pylint: disable=relative-beyond-top-level
import random
import asyncio

from replit import db

import discord
from discord import DMChannel
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

def create_desk():
  cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
  suits = [' :spades:', ' :clubs:', ' :diamonds:', ' :hearts:']
  desk = []
  for i in cards:
    for j in suits:
      desk.append(i + j)
  random.shuffle(desk)
  return desk

prefix = db['prefix'][0]
players = []
desk = []
cards = []
turn = 0

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


    @commands.command(aliases=['bjj', 'bjjoin'])
    async def blackjackjoin(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj join')
      global players
      if str(ctx.author.id) not in players:
        status = db['bjs'][0]
        if status == 'end' or status == 'lobby':
          pid = str(ctx.author.id)
          status = 'lobby'
          db['bjs'] = [status]
          players.append(pid)
          await ctx.channel.send('<@!' + pid + '> vừa tham gia.')
        else:
          await ctx.channel.send('Không thể tham gia vì trò chơi đã được bắt đầu.')
      else:
          await ctx.channel.send('Bạn đã tham gia rồi mà.')


    @commands.command(aliases=['bju', 'bjunjoin'])
    async def blackjackunjoin(ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj unjoin')
      global players
      if str(ctx.author.id) in players:
        status = db['bjs'][0]
        if status == 'lobby':
          pid = str(ctx.author.id)
          players.remove(pid)
          await ctx.channel.send('<@!' + pid + '> vừa thoát ra.')
        else:
          await ctx.channel.send('Không thể thoát ra vì trò chơi đã được bắt đầu.')
      else:
        await ctx.channel.send('Bạn làm gì đã ở trong phòng chơi đâu.')


    @commands.command(aliases=['bjs', 'bjstart'])
    async def blackjackstart(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj start')
      global players
      if str(ctx.author.id) not in players:
        await ctx.channel.send('Bạn không có trong danh sách người chơi nên không thể bắt đầu trò chơi.')
        return
      status = db['bjs'][0]
      if status == 'lobby':
        status = 'start'
        db['bjs'] = [status]
        global desk
        desk = create_desk()
        for i in range(len(players)):
          card = []
          card.append(desk.pop())
          card.append(desk.pop())
          user = await self.client.fetch_user(players[i])
          await DMChannel.send(user, f'**Your cards:**\n{card[0]} {card[1]}')
          cards.append(card)
        des = '**Thứ tự người chơi:**\n'
        for i in range(len(players)):
          user = await self.client.fetch_user(players[i])
          name = user.display_name
          des += f'**{i+1}.** {name}\n'
        embed = discord.Embed(title='Trò chơi đã được bắt đầu.', description=des, color=discord.Color.purple())
        await ctx.send(embed=embed)
        user = await self.client.fetch_user(players[turn])
        await ctx.channel.send('Lượt của ' + user.mention)
      elif status == 'start':
        await ctx.channel.send('Trò chơi đã bắt đầu mất rồi.')
      else:       
        await ctx.channel.send('Không thể bắt đầu vì không có người chơi.')


    @commands.command(aliases=['bjd', 'bjdraw'])
    async def blackjackdraw(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj draw')
      global players
      if str(ctx.author.id) not in players:
        await ctx.channel.send('Bạn không có trong danh sách người chơi nên không thể bốc bài.')
        return
      status = db['bjs'][0]
      if status == 'start' and str(ctx.author.id) == players[turn]:
        cards[turn].append(desk.pop())
        c = ''
        for i in range(len(cards[turn])):
          c += cards[turn][i] + '  '
        user = await self.client.fetch_user(players[turn])
        await DMChannel.send(user, f'**Your cards:**\n{c}')
        await ctx.channel.send(f'{user} Vừa bốc một lá.')
      else:
        await ctx.channel.send('Chưa thể sử dụng được lệnh này hoặc chưa đến lượt của bạn.')


    @commands.command(aliases=['bjsd', 'bjstopd'])
    async def blackjackstopdraw(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj stopdraw')
      global players
      if str(ctx.author.id) not in players:
        await ctx.channel.send('Bạn không có trong danh sách người chơi nên không thể làm gì.')
        return
      status = db['bjs'][0]
      global turn
      global cards
      if status == 'start' and str(ctx.author.id) == players[turn]:
        if turn == len(players) - 1:
          user = await self.client.fetch_user(players[turn])
          await ctx.channel.send(f'{user} đã dừng lượt')
          embed = discord.Embed(description='Kết thúc.', color=discord.Color.purple())
          for i in range(len(players)):
            user = await self.client.fetch_user(players[i])
            c = ''
            for j in range(len(cards[i])):
              c += cards[i][j] + '  '
            embed.add_field(name=user.display_name, value=c, inline=False)
          await ctx.channel.send(embed=embed)
          global desk
          cards = []
          desk = []
          turn = 0
          status = 'lobby'
          db['bjs'] = [status]
          await ctx.channel.send('Ván đấu đã được tạo lại, có thể tham gia thêm.')
        else:
          user = await self.client.fetch_user(players[turn])
          await ctx.channel.send(f'{user} đã dừng lượt')
          turn += 1
          user = await self.client.fetch_user(players[turn])
          await ctx.channel.send('Lượt của ' + user.mention)
      else:
        await ctx.channel.send('Chưa thể sử dụng được lệnh này hoặc chưa đến lượt của bạn.')


    @commands.command(aliases=['bjrs', 'bjrestart'])
    async def blackjackrestart(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj restart')
      global players
      if str(ctx.author.id) not in players:
        await ctx.channel.send('Bạn không có trong danh sách người chơi nên không thể phá đâu nhé.')
        return
      status = db['bjs'][0]
      if status == 'start':
        global cards
        global desk
        global turn
        cards = []
        desk = []
        turn = 0
        status = 'lobby'
        db['bjs'] = [status]
        await ctx.channel.send('Ván đấu đã được tạo lại, có thể tham gia thêm.')
      else:
        await ctx.channel.send('Bắt đầu game trước khi restart nó nhé.')


    @commands.command(aliases=['bje', 'bjend'])
    async def blackjackend(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj restart')
      global cards
      global desk
      global players
      global turn
      if str(ctx.author.id) not in players:
        await ctx.channel.send('Bạn không có trong danh sách người chơi nên không thể phá đâu nhé.')
        return
      status = db['bjs'][0]
      if status == 'lobby':
        players = []
        cards = []
        desk = []
        turn = 0
        status = 'end'
        db['bjs'] = [status]
        await ctx.channel.send('Trò chơi đã kết thúc hoàn toàn.')
      else:
        await ctx.channel.send('Kết thúc ván đấu trước khi kết thúc trò chơi nhé.')


    @commands.command(aliases=['bjc', 'bjcheck'])
    async def blackjackcheck(self, ctx, *args):
      if not('blackjack' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
        return
      print(ctx.author.id)        
      print('bj check')
      # print(players)
      des = ''
      for i in range(len(players)):
        user = await self.client.fetch_user(players[i])
        name = user.display_name
        des += f'**{i+1}.** {name}\n'
      embed = discord.Embed(title='Danh sách người chơi:', description=des, color=discord.Color.purple())
      await ctx.send(embed=embed)


    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx, *args):
      if not args:
        embedVar = discord.Embed(
          title="Xin lỗi vì đã dắt bạn đi hơi xa so với hướng dẫn :)",
          description="**Trò chơi Xì Zách.**\n*Các lưu ý:*\n- Không thể tham gia hoặc thoát ra khi trò chơi đã bắt đầu.\n- Trước khi khởi tạo hoặc bắt đầu ván, hãy tham khảo ý kiến người chơi khác", color=0x34ebae)
        embedVar.add_field(name='1. Tham gia', value='- `{0}blackjackjoin` hoặc `{0}bjj` để tham gia phòng chơi'.format(prefix), inline=False)
        embedVar.add_field(name='2. Kiểm tra tham gia', value='- `{0}blackjackcheck` hoặc `{0}bjc` để xem mình đã tham gia phòng chơi chưa'.format(prefix), inline=False)
        embedVar.add_field(name='3. Bắt đầu trò chơi', value='- `{0}blackjackstart` hoặc `{0}bjs` để bắt đầu chơi. Nhận bài và chờ đến lượt chơi.'.format(prefix), inline=False)
        embedVar.add_field(name='4. Bốc hoặc dừng', value='- `{0}blackjackdraw` hoặc `{0}bjd` để bốc bài khi đến lượt.\n- `{0}blackjackstopdraw` hoặc `{0}bjsd` để dừng bốc bài khi đến lượt. Khi bạn là người cuối cùng thì trò chơi sẽ tự động khởi tạo lại.'.format(prefix), inline=False)
        embedVar.add_field(name='5. Khi muốn chơi lại khi trò chơi chưa dừng', value='`- {0}blackjackrestart` hoặc `{0}bjrs` để khởi tạo lại. Bạn vẫn sẽ trong phòng chơi.'.format(prefix), inline=False)
        embedVar.add_field(name='6. Dừng hoàn toàn trò chơi', value='`- {0}blackjackend` hoặc `{0}bje` để dừng hoàn toàn khi không ai muốn chơi nữa.'.format(prefix), inline=False)
        embedVar.add_field(name='7. Rời phòng', value='`- {0}blackjackunjoin` hoặc `{0}bju` để thoát khỏi phòng.'.format(prefix), inline=False)
        await ctx.channel.send(embed=embedVar)


    @commands.command(aliases=['lts', 'lotos', 'ltstart'])
    @cooldown(1, 1, BucketType.user)
    async def lotostart(self, ctx, *args):
      print(ctx.author.id)
      if not('loto' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
      else:
        if not args:
          started = db['lotos'][0]
          if started == False:
            nums = [*range(1, 91, 1)]
            random.shuffle(nums)
            db['loto'] = nums
            started = True
            db['lotos'] = [started]
            await ctx.channel.send('Trò chơi bắt đầu')
          else:
            await ctx.channel.send('Trò chơi đã bắt đầu rồi.')
      print('loto start')


    @commands.command(aliases=['lt'])
    @cooldown(1, 1, BucketType.user)
    async def loto(self, ctx, *args):
      print(ctx.author.id)
      if not('loto' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
      else:
        if not args:
          started = db['lotos'][0]
          if started == False:
            await ctx.channel.send('Vui lòng bắt đầu game bằng lệnh `{0}lotostart` trước.'.format(prefix))
          else:
            nums = db['loto']
            added = db['lotoc']
            index = nums.pop()
            added.append(index)
            db['lotoc'] = added
            db['loto'] = nums
            await ctx.channel.send('**' + str(index) + '**')
      print('loto random')


    @commands.command(aliases=['ltc', 'ltcheck', 'lotoc'])
    @cooldown(1, 1, BucketType.user)
    async def lotocheck(self, ctx, *args):
      print(ctx.author.id)
      if not('loto' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
      else:
        if not args:
          await ctx.channel.send('Vui lòng nhập 5 số theo dạng: `a b c d e` sau lệnh `{0}lotocheck`'.format(prefix))
        elif len(args) < 5 or len(args) > 5:
          await ctx.channel.send('Vui lòng nhập đủ 5 số.')
        else:
          started = db['lotos'][0]
          if started == False:
            await ctx.channel.send('Trò chơi chưa được bắt đầu, hãy bắt đầu game bằng lệnh `{0}lotostart` trước'.format(prefix))
          else:
            done = False
            nums = db['lotoc']
            print(nums)
            print(args)
            try:
              for i in args:
                if int(i) in nums:
                  done = True
                else:
                  done = False
                  break
            except:
              await ctx.channel.send('Vui lòng kiểm tra lại cú pháp. Chỉ được nhập số thôi nhé')
            if done == True:
              await ctx.channel.send('Kết quả hợp lệ. Bạn có thể kết thúc bằng lệnh `{0}ltend`'.format(prefix))
            else:
              await ctx.channel.send('Kết quả không hợp lệ. Đừng gian lận nhé.')
      print('loto check')

    
    @commands.command(aliases=['lte', 'ltend', 'lotoe'])
    @cooldown(1, 1, BucketType.user)
    async def lotoend(self, ctx, *args):
      print(ctx.author.id)
      if not('loto' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
      else:
        if not args:
          started = db['lotos'][0]
          if started == False:
            await ctx.channel.send('Trò chơi chưa được bắt đầu, hãy bắt đầu game bằng lệnh `{0}lotostart` trước'.format(prefix))
          else:
            db['lotoc'] = []
            started = False
            db['lotos'] = [started]
            await ctx.channel.send('Trò chơi đã được kết thúc')
      print('loto ended')


    @commands.command(aliases=['lta', 'ltall', 'lotoa'])
    @cooldown(1, 1, BucketType.user)
    async def lotoall(self, ctx, *args):
      print(ctx.author.id)
      if not('loto' in ctx.channel.name):
        await ctx.channel.send('Không thể dùng lệnh ở channel này.')
      else:
        if not args:
          started = db['lotos'][0]
          if started == False:
            await ctx.channel.send('Trò chơi chưa được bắt đầu, hãy bắt đầu game bằng lệnh `{0}lotostart` trước'.format(prefix))
          else:
            nums = db['lotoc']
            await ctx.channel.send(nums)
            await ctx.channel.send('\nTổng cộng có: {0} lần quay'.format(len(nums)))

      print('loto all')


def setup(client):
    client.add_cog(Talk(client))