from typing import Optional
from datetime import datetime

from replit import db

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

prefix = db['prefix'][0]
class CMND(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ids', 'users', 'cmnds'])
    @cooldown(1, 5, BucketType.user)
    async def allcmnd(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      if not args:
        print(ctx.author.id)
        print('sent all users')
        id_list = db['user_id']
        temp =  db['user_name']
        list_name = temp[1:]
        n=15
        b = [list_name[i*n : (i+1)*n] for i in range((len(list_name) + n - 1) // n)]
        count = 1
        n_pages = int(len(list_name)/n) + 1
        pages = []
        for i in range(n_pages):
            des = ''
            for j in b[i]:
                des += f'**{str(count)}**. <@!{id_list[count]}> {j}\n'
                count += 1
            single_page = discord.Embed(
              title='Danh sách những người tôi biết <3',
              description = des,
              colour = discord.Colour.blue())
            single_page.set_footer(text='Page {0}/{1}'.format(i+1, n_pages))
            pages.append(single_page)
        messages = await ctx.send(embed = pages[0])
        await messages.add_reaction('◀')
        await messages.add_reaction('▶')
        await messages.add_reaction("🗑️")
        def check(reaction, user):
          return user == ctx.author

        i = 0
        reaction = None

        while True:
          if str(reaction) == '🗑️':
              await messages.delete()
          elif str(reaction) == '◀':
              if i > 0:
                  i -= 1
                  await messages.edit(embed = pages[i])
          elif str(reaction) == '▶':
              if i < (len(pages) - 1):
                  i += 1
                  await messages.edit(embed = pages[i])
          
          try:
              reaction, user = await self.client.wait_for('reaction_add', timeout = 30.0, check = check)
              await messages.remove_reaction(reaction, user)
          except:
              break


    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def cmnd(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      print(ctx.author.id)
      list_id = db['user_id']
      list_name = db['user_name']
      # print(list(zip(list_id, list_name)))
      if (str(ctx.author.id) == '394520281814925313'):
        await ctx.send(
          'Thin yêu dấu, bạn không cần phải đăng ký CMND làm gì đâu nè. :D'
        )
      elif (str(ctx.author.id) in list_id):
        await ctx.send(
          'Ôi không! Tôi biết bạn là ai mà, bạn không cần đăng ký lại đâu he.'
        )
      else:
        if not args:
          await ctx.send('Nhập thêm tên mà bạn muốn tôi gọi vào sau cú pháp `{0}cmnd` bạn nhé'.format(prefix))
            
        else:
          name = ' '.join(args)
          list_id.append(str(ctx.author.id))
          list_name.append(name)
          db['user_id'] = list_id
          db['user_name'] = list_name
          print('dang ky cmnd thanh cong')
          await ctx.send('Đăng kí CMND thành công <3')
      print('dang ky cmnd')


    @commands.command(aliases=['cmnde'])
    @cooldown(1, 3, BucketType.user)
    async def cmndedit(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      print(ctx.author.id)
      list_id = db['user_id']
      list_name = db['user_name']
      # print(list(zip(list_id, list_name)))
      if (str(ctx.author.id) not in list_id):
        await ctx.send(
          'Ôi không! Bạn chưa đăng ký tên mà, đăng ký rồi hãy chỉnh sửa nhé. `{0}cmnd`'.format(prefix)
        )
      else:
        if not args:
          await ctx.send('Nhập thêm tên mà bạn muốn tôi gọi vào sau cú pháp `{0}cmndedit` bạn nhé'.format(prefix))
        else:
          name = ' '.join(args)
          list_name[list_id.index(str(ctx.author.id))] = name
          db['user_id'] = list_id
          db['user_name'] = list_name
          print('thay doi cmnd thanh cong')
          await ctx.send(f'Đã sửa đổi tên CMND sang {name}')


    @commands.command(aliases=['bd'])
    async def birthday(self, ctx, *args):
      print(ctx.author.id)
      allab = db['bd']
      a = []
      b = []
      for i in allab:
        a.append(i.split(' - ')[0])
        b.append(i.split(' - ')[1])
      if not args:
        if str(ctx.author.id) not in a:
          await ctx.send("Bạn chưa đăng ký sinh nhật. Vui lòng đăng ký theo lệnh: `{0}birthday` `dd/mm` bạn nhé.".format(prefix))
        else:
          await ctx.send(f"Bạn đã đăng ký sinh nhật ngày: {b[a.index(str(ctx.author.id))]}")
      else:
        mess = ' '.join(args)
        try:
          datetime_object = datetime.strptime(mess, '%d/%m')
          bd = datetime_object.strftime('%d/%m')
          allab.append(str(ctx.author.id) + ' - ' + bd)
          db['bd'] = allab
          await ctx.send("Đăng ký sinh nhật thành công.")
        except:
          if '29' in mess and '02' in mess:
            datetime_object = datetime.strptime('29/02/2012', '%d/%m/%Y')
            bd = datetime_object.strftime('%d/%m')
            allab.append(str(ctx.author.id) + ' - ' + bd)
            db['bd'] = allab
            await ctx.send("Đăng ký sinh nhật thành công.")
          else:
            await ctx.send("Sai cú pháp. Vui lòng đăng ký theo lệnh: `{0}birthday` `dd/mm` bạn nhé.".format(prefix))
      print('reg birthday')


    @commands.command(aliases=['bde', 'bdedit'])
    async def birthdayedit(self, ctx, *args):
      print(ctx.author.id)
      allab = db['bd']
      a = []
      b = []
      for i in allab:
        a.append(i.split(' - ')[0])
        b.append(i.split(' - ')[1])
      if not args:
        await ctx.send("Vui lòng nhập ngày tháng theo định dạng `dd/mm` sau câu lệnh `{0}birthdayedit`")
      else:
        if str(ctx.author.id) not in a:
          await ctx.send("Bạn chưa đăng ký sinh nhật. Vui lòng đăng ký theo lệnh: `{0}birthday` `dd/mm` bạn nhé.".format(prefix))
        else:
          mess = ' '.join(args)
          try:
            datetime_object = datetime.strptime(mess, '%d/%m')
            bd = datetime_object.strftime('%d/%m')
            index = a.index(str(ctx.author.id))
            b[index] = bd
            allab[index] = str(ctx.author.id) + ' - ' + bd
            db['bd'] = allab
            await ctx.send("Sửa đổi sinh nhật thành công.")
          except:
            if '29' in mess and '02' in mess:
              datetime_object = datetime.strptime('29/02/2012', '%d/%m/%Y')
              bd = datetime_object.strftime('%d/%m')
              index = a.index(str(ctx.author.id))
              b[index] = bd
              allab[index] = str(ctx.author.id) + ' - ' + bd
              db['bd'] = allab
              await ctx.send("Sửa đổi sinh nhật thành công.")
            else:
              await ctx.send("Sai cú pháp. Vui lòng đăng ký theo lệnh: `{0}birthdayedit` `dd/mm` bạn nhé.".format(prefix))
      print('edit birthday')


    @commands.command(aliases=["who", 'whois', 'info'])
    @cooldown(1, 3, BucketType.user)
    async def whos(self, ctx, *, member: Optional[discord.Member]=None):
      print(ctx.author.id)
      print('sent whos')

      list_id = db['user_id']
      list_name = db['user_name']
      allab = db['bd']
      a = []
      b = []
      for i in allab:
        a.append(i.split(' - ')[0])
        b.append(i.split(' - ')[1])

      member = member or ctx.author
      name = ''
      bd = ''
      if str(member.id) not in list_id:
        name = 'Chưa đăng ký CMND.'
      else:
        name = list_name[list_id.index(str(member.id))]
      

      created_at = member.created_at.strftime('%B %d %Y at %H:%M')
      joined = member.joined_at
      today = datetime.now()
      d = today - joined
      embed = discord.Embed(description=member.mention + f' đã tham gia {d.days} ngày', color=discord.Color.purple())
      joined_at = joined.strftime('%B %d %Y at %H:%M')
      
      embed.set_thumbnail(url=member.avatar_url) 
      embed.add_field(name='Tạo tài khoản:', value=created_at, inline=False)
      embed.add_field(name=f'Tham gia {ctx.message.guild.name}:', value=joined_at, inline=False)
      embed.add_field(name='CMND:', value=name)
      embed.add_field(name='CMND số:', value=member.id)
      if str(member.id) not in a:
        bd = 'Chưa đăng ký ngày sinh.'
        embed.add_field(name='Sanh thần:', value=bd)
      else:
        bd = datetime.strptime(b[a.index(str(member.id))],'%d/%m')
        embed.add_field(name='Sanh thần:', value=bd.strftime('Ngày %d tháng %m năm gì kệ'))
      embed.add_field(name='AKA:', value=member)
      await ctx.send(embed=embed)

def setup(client):
    client.add_cog(CMND(client))