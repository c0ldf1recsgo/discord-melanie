# pylint: disable=relative-beyond-top-level
import random

from replit import db

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

def get_chuc():
    return db['cau_chuc']

def get_tru():
    return db['cau_tru']

def update_cau_chuc(cau_chuc_message):
  if ('cau_chuc' in db.keys()):
    cau_chuc = db['cau_chuc']
    cau_chuc.append(cau_chuc_message)
    db['cau_chuc'] = cau_chuc
  else:
    db['cau_chuc'] = [cau_chuc_message]

def delete_cau_chuc(index):
  list_cau_chuc = db['cau_chuc']
  if len(list_cau_chuc) >= index:
      del list_cau_chuc[index - 1]
  db['cau_chuc'] = list_cau_chuc

def update_cau_tru(cau_tru_message):
  if ('cau_tru' in db.keys()):
    cau_tru = db['cau_tru']
    cau_tru.append(cau_tru_message)
    db['cau_tru'] = cau_tru
  else:
    db['cau_tru'] = [cau_tru_message]

def delete_cau_tru(index):
  list_cau_tru = db['cau_tru']
  if len(list_cau_tru) >= index:
      del list_cau_tru[index - 1]
  db['cau_tru'] = list_cau_tru

prefix = db['prefix'][0]
class Talk(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['buon', 'depressed', 'unhappy', 'upset', 'tramcam', 'huhu'])
    @cooldown(1, 3, BucketType.user)
    async def sad(self, ctx, *args):
        if ctx.author == self.client.user:
            return
        if not args:
            cau_chuc = [
            'Đừng bỏ cuộc nhé. Giông bão sẽ sớm qua đi và trời sẽ lại tươi xanh. Hãy là cái đầu lạnh với tinh thần thép và mọi chuyện rồi sẽ ổn.',
            'Cố lên, bạn có thể làm được mà. Tôi sẽ luôn bên cạnh hỗ trợ, giúp đỡ bạn bằng hết khả năng của mình. Cuộc đời của bạn thì bạn hãy tự tin “dám nghĩ dám làm”. Sai thì sửa.',
            'Cố hết sức mình đi, tôi biết bạn sẽ làm được. Đây là thế giới của hành động và thử thách, không phải thế giới của sự lười biếng và hèn nhát.',
            'Đời có bao nhiêu đâu mà buồn, hãy vững tin và quên đi tất cả. Cuộc sống có vô vàng những điều tốt đẹp đang chờ bạn phía trước, vui vẻ đón nhận bạn sẽ thấy thật hạnh phúc và bình yên.',
            'Cho dù bạn mất đi tất cả nhưng bạn vẫn còn tương lai phía trước. Tôi tin bạn sẽ thành công, cuộc đời của mình bạn hãy tự quyết định.',
            'Thất bại là mẹ thành công. Không có con đường nào trải đầy hoa hồng, phải có chông gai, có vấp ngã mới trưởng thành.',
            'Bạn đi đúng hướng rồi đó. Bạn sắp nhận được quả ngọt rồi, mình sẽ đồng hành cùng bạn dù phía trước có nhiều giông bão.',
            'Buồn làm gì cho đời thêm khổ, khóc làm chi cho khổ cuộc đời, chán làm chi cho tương lai đen tối, hãy vững tin và mạnh mẽ đối diện với khó khăn.',
            'Mạnh mẽ lên vì mọi thứ rồi sẽ tốt đẹp lên thôi, sau cơn mưa trời lại sáng mà.',
            'Thành công sẽ không bao giờ từ chối những con người dám nghĩ dám làm. Tôi tin bạn sẽ làm được tốt hơn thế.'
            ]
            options = get_chuc()
            options = options + cau_chuc
            print(ctx.author.id)
            await ctx.channel.send(random.choice(options))
            print('sent cau chuc')
        else:
            ctx.command.reset_cooldown(ctx)

    @commands.command(aliases=['vui', 'hanhphuc', 'cuoi', 'lol', 'haha', 'happy', 'smile', 'hehe', 'hihi'])
    @cooldown(1, 3, BucketType.user)
    async def fun(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        cau_tru = [
          'Ơ, da dạo này lắm mụn thế?', 'Vẫn chưa có người yêu à?', 'Sao gầy thế, đói ăn à?',
          'Lâu không gặp, mày tăng bao cân rồi nhìn đẫy đà quá', 'Đồ Ế!' , 'Cuộc vui nào rồi cũng sẽ có lúc tàn, đừng vội mừng.', 'Cười đi khi còn có thể, sau này chẳng còn cười được đâu.'
        ]
        options = db['cau_tru']
        options = options + cau_tru
        print(ctx.author.id)
        await ctx.channel.send(random.choice(options))
        print('sent cau tru')
      else:
        ctx.command.reset_cooldown(ctx)

    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def chuc(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        print(ctx.author.id)
        await ctx.channel.send('Vui lòng nhập lời chúc sau lệnh `{0}chuc`'.format(prefix))
        print('them cau chuc (empty)')
      else:
        print(ctx.author.id)
        cau_chuc_moi = ' '.join(args)
        update_cau_chuc(cau_chuc_moi)
        await ctx.channel.send(ctx.author.display_name + ' đã thêm lời chúc mới :D\n' + cau_chuc_moi)
        print('them cau chuc thanh cong')


    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def tru(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        print(ctx.author.id)
        await ctx.channel.send('Vui lòng nhập câu trù sau lệnh `{0}tru`'.format(prefix))
        print('them cau tru (empty)')
      else:
        print(ctx.author.id)
        cau_tru_moi = ' '.join(args)
        update_cau_tru(cau_tru_moi)
        await ctx.channel.send(ctx.author.display_name + ' đã thêm lời hay ý đẹp mới :D\n' + cau_tru_moi)
        print('them cau tru thanh cong')


    @commands.command(aliases=['dchuc'])
    @cooldown(1, 5, BucketType.user)
    async def xoachuc(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        print(ctx.author.id)
        await ctx.channel.send('Vui lòng nhập số thứ tự câu chúc sau lệnh `{0}xoachuc`'.format(prefix))
        print('xoa cau chuc(empty)')
      elif args[0].isnumeric():
        print(ctx.author.id)
        if 'cau_chuc' in db.keys():
          if(int(args[0]) <= len(db['cau_chuc'])):
            index = int(args[0])
            delete_cau_chuc(index)
            await ctx.channel.send('Đã xóa lời chúc :(')
            print('xoa cau chuc thanh cong')
          else:
            await ctx.channel.send('Không có câu chúc nào có số thứ tự này')
            print('xoa cau chuc fail')


    @commands.command(aliases=['dtru'])
    @cooldown(1, 5, BucketType.user)
    async def xoatru(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        print(ctx.author.id)
        await ctx.channel.send('Vui lòng nhập số thứ tự câu trù sau lệnh `{0}xoatru`'.format(prefix))
        print('xoa cau tru(empty)')
      elif args[0].isnumeric():
        print(ctx.author.id)
        if 'cau_tru' in db.keys():
          if(int(args[0]) <= len(db['cau_tru'])):
            index = int(args[0])
            delete_cau_tru(index)
            await ctx.channel.send('Đã xóa câu trù :(')
            print('xoa cau tru thanh cong')
          else:
            await ctx.channel.send('Không có câu trù nào có số thứ tự này')
            print('xoa cau tru fail')


    @commands.command(aliases=['ac'])
    @cooldown(1, 5, BucketType.user)
    async def allchuc(self, ctx, *args):
      if ctx.author == self.client.user or len(args) > 0:
        return

      print(ctx.author.id)
      print('danh sach chuc')
      list_cau_chuc = db['cau_chuc']
      if len(list_cau_chuc) > 0:
        n=8
        b = [list_cau_chuc[i*n : (i+1)*n] for i in range((len(list_cau_chuc) + n - 1) // n)]

        count = 1
        if ((len(list_cau_chuc) % n) == 0):
          n_pages = int(len(list_cau_chuc)/n)
        else:
          n_pages = int(len(list_cau_chuc)/n) + 1
        pages = []
        print(n_pages)
        for i in range(n_pages):
          des = ''
          for j in b[i]:
            des += '**' + str(count) + '**. ' + j + '\n'
            count += 1
          single_page = discord.Embed(
            title='Danh sách các câu chúc',
            description = "Dưới đây là những câu chúc được người dùng thêm vào.\nĐể thêm câu chúc nhập `{0}chuc [câu-chúc]`\nĐể xóa câu chúc nhập `{0}xoachuc [số-thứ-tự-câu-chúc]`\n\n".format(prefix) + des,
            colour = discord.Colour.green())
          single_page.set_footer(text='Page {0}/{1}'.format(i+1, n_pages))
          pages.append(single_page)
        messages = await ctx.channel.send(embed = pages[0])
        await messages.add_reaction('◀')
        await messages.add_reaction('▶')

        def check(reaction, user):
          return user == ctx.author

        i = 0
        reaction = None

        while True:
          if str(reaction) == '◀':
            if i > 0:
              i -= 1
              await messages.edit(embed = pages[i])
          elif str(reaction) == '▶':
            if i < (len(pages) - 1):
              i += 1
              await messages.edit(embed = pages[i])
          else:
            pass
          
          try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
            await messages.remove_reaction(reaction, user)
          except:
            break
      else:
        embedVar = discord.Embed(
            title="Danh sách các câu chúc từ người dùng",
            description= "Chưa có câu chúc nào cả :( Hãy thêm đi nhé.", color=0x00ff00)
        await ctx.channel.send(embed = embedVar)


    @commands.command(aliases=['at'])
    @cooldown(1, 5, BucketType.user)
    async def alltru(self, ctx, *args):
      if ctx.author == self.client.user or len(args) > 0:
        return
      print(ctx.author.id)
      print('danh sach tru')
      list_cau_tru = db['cau_tru']
      if len(list_cau_tru) > 0:
        n=8
        b = [list_cau_tru[i*n : (i+1)*n] for i in range((len(list_cau_tru) + n - 1) // n)]

        count = 1
        if ((len(list_cau_tru) % n) == 0):
          n_pages = int(len(list_cau_tru)/n)
        else:
          n_pages = int(len(list_cau_tru)/n) + 1
        pages = []
        for i in range(n_pages):
          des = ''
          for j in b[i]:
            des += '**' + str(count) + '**. ' + j + '\n'
            count += 1
          single_page = discord.Embed(
            title='Danh sách những lời hay ý đẹp',
            description = "Dưới đây là những lời hay ý tốt được người dùng thêm vào.\nĐể thêm câu trù nhập `{0}tru [câu-trù]`\nĐể xóa câu trù nhập `{0}xoatru [số-thứ-tự-câu-trù]`\n\n".format(prefix) + des,
            colour = discord.Colour.magenta())
          single_page.set_footer(text='Page {0}/{1}'.format(i+1, n_pages))
          pages.append(single_page)
        messages = await ctx.channel.send(embed = pages[0])
        await messages.add_reaction('◀')
        await messages.add_reaction('▶')

        def check(reaction, user):
          return user == ctx.author

        i = 0
        reaction = None

        while True:
          if str(reaction) == '◀':
            if i > 0:
              i -= 1
              await messages.edit(embed = pages[i])
          elif str(reaction) == '▶':
            if i < (len(pages) - 1):
              i += 1
              await messages.edit(embed = pages[i])
          else:
            pass
          
          try:
            reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
            await messages.remove_reaction(reaction, user)
          except:
            break


    @commands.command(aliases=['hi', 'chao', 'bonjour', 'hola'])
    @cooldown(1, 3, BucketType.user)
    async def hello(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        list_id = db['user_id']
        list_name = db['user_name']
        group = tuple(zip(list_id, list_name))
        cau_chao = [
          'Chào bạn {0} xinh đẹp nhó.', 'Xin chào bạn {0} yêu dấu.',
          'Chào {0}, chúc bạn một ngày tốt lành nè.',
          'Ai vậy ai vậy, ồ đó là {0} đúng không nào, xin chào nhó.'
        ]
        print(ctx.author.id)
        if (str(ctx.author.id) == '394520281814925313'):
          await ctx.channel.send('Xin chào ngài Thin điên :D')
        elif (str(ctx.author.id) in list_id):
          for i in group:
            if (i[0] == str(ctx.author.id)):
              await ctx.channel.send(random.choice(cau_chao).format(i[1]))
        else:
          await ctx.channel.send('Xin chào, mình là iHCMUS, con bot lạc quan yêu đời nhất của Server H C M U S')
        print('sent hello')
      else:
        ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(Talk(client))