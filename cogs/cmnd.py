from typing import Optional
from datetime import datetime
from discord.ext.commands.core import bot_has_permissions
import pytz

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from .func import converter as conv

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://blah-blah-blah")

db = cluster['discord']['data']


def get_prefix():
    prefixid = db.find_one({"id": 'prefix'})
    prefix = prefixid['value']
    return prefix


def get_user_id():
    useridid = db.find_one({"id": 'user_id'})
    userid = useridid['value']
    return userid


def get_user_name():
    usernameid = db.find_one({"id": 'user_name'})
    username = usernameid['value']
    return username


def add_user(uid, uname):
    useridid = db.find_one({"id": 'user_id'})
    userid = useridid['value']
    usernameid = db.find_one({"id": 'user_name'})
    username = usernameid['value']

    userid.append(str(uid))
    username.append(str(uname))

    db.update_one({"id":'user_id'}, {"$set":{"value":userid}})
    db.update_one({"id":'user_name'}, {"$set":{"value":username}})


def edit_user(uid, uname):
    useridid = db.find_one({"id": 'user_id'})
    userid = useridid['value']
    usernameid = db.find_one({"id": 'user_name'})
    username = usernameid['value']

    username[userid.index(uid)] = uname
    db.update_one({"id":'user_name'}, {"$set":{"value":username}})


def get_bd():
    bdid = db.find_one({"id": 'bd'})
    bd = bdid['value']
    return bd


def add_bd(idbd):
    bdid = db.find_one({"id": 'bd'})
    bd = bdid['value']

    bd.append(idbd)
    db.update_one({"id":'bd'}, {"$set":{"value":bd}})


def edit_bd(index, idbd):
    bdid = db.find_one({"id": 'bd'})
    bd = bdid['value']

    bd[index] = idbd
    db.update_one({"id":'bd'}, {"$set":{"value":bd}})


prefix = get_prefix()[0]
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
        id_list = get_user_id()
        temp =  get_user_name()
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
          return user == ctx.author and reaction.message == messages

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
      list_id = get_user_id()
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
          add_user(str(ctx.author.id), name)
          print('dang ky cmnd thanh cong')
          await ctx.send('Đăng kí CMND thành công <3')
      print('dang ky cmnd')


    @commands.command(aliases=['cmnde'])
    @cooldown(1, 3, BucketType.user)
    async def cmndedit(self, ctx, *args):
      if ctx.author == self.client.user:
        return
      print(ctx.author.id)
      list_id = get_user_id()
      if (str(ctx.author.id) not in list_id):
        await ctx.send(
          'Ôi không! Bạn chưa đăng ký tên mà, đăng ký rồi hãy chỉnh sửa nhé. `{0}cmnd`'.format(prefix)
        )
      else:
        if not args:
          await ctx.send('Nhập thêm tên mà bạn muốn tôi gọi vào sau cú pháp `{0}cmndedit` bạn nhé'.format(prefix))
        else:
          name = ' '.join(args)
          edit_user(str(ctx.author.id), name)
          print('thay doi cmnd thanh cong')
          await ctx.send(f'Đã sửa đổi tên CMND sang {name}')


    @commands.command(aliases=['bd'])
    async def birthday(self, ctx, *args):
      print(ctx.author.id)
      allab = get_bd()
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
        if str(ctx.author.id) not in a:
          mess = ' '.join(args)
          try:
            datetime_object = datetime.strptime(mess, '%d/%m')
            bd = datetime_object.strftime('%d/%m')
            add_bd(str(ctx.author.id) + ' - ' + bd)
            allab.append(str(ctx.author.id) + ' - ' + bd)
            await ctx.send("Đăng ký sinh nhật thành công.")
          except:
            if '29' in mess and '02' in mess:
              datetime_object = datetime.strptime('29/02/2012', '%d/%m/%Y')
              bd = datetime_object.strftime('%d/%m')
              allab.append(str(ctx.author.id) + ' - ' + bd)
              add_bd(str(ctx.author.id) + ' - ' + bd)
              await ctx.send("Đăng ký sinh nhật thành công.")
            else:
              await ctx.send("Sai cú pháp. Vui lòng đăng ký theo lệnh: `{0}birthday` `dd/mm` bạn nhé.".format(prefix))
        else:
          await ctx.send(f"Bạn đã đăng ký sinh nhật ngày: {b[a.index(str(ctx.author.id))]}")
      print('reg birthday')


    @commands.command(aliases=['bde', 'bdedit'])
    async def birthdayedit(self, ctx, *args):
      print(ctx.author.id)
      allab = get_bd()
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
            edit_bd(index, str(ctx.author.id) + ' - ' + bd)
            await ctx.send("Sửa đổi sinh nhật thành công.")
          except:
            if '29' in mess and '02' in mess:
              datetime_object = datetime.strptime('29/02/2012', '%d/%m/%Y')
              bd = datetime_object.strftime('%d/%m')
              index = a.index(str(ctx.author.id))
              b[index] = bd
              allab[index] = str(ctx.author.id) + ' - ' + bd
              edit_bd(index, str(ctx.author.id) + ' - ' + bd)
              await ctx.send("Sửa đổi sinh nhật thành công.")
            else:
              await ctx.send("Sai cú pháp. Vui lòng đăng ký theo lệnh: `{0}birthdayedit` `dd/mm` bạn nhé.".format(prefix))
      print('edit birthday')


    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def hpbd(self, ctx, *args):
        if not args:
            allab = get_bd()
            a = []
            b = []
            for i in allab:
                a.append(i.split(' - ')[0])
                b.append(i.split(' - ')[1])
            l = []
            today = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%d/%m")
            today_date = datetime.strptime(today, "%d/%m")
            for i in range(len(b)):
                l.append((datetime.strptime(b[i], "%d/%m")-today_date).days)

            nearest = min([i for i in l if i > 0])
            if 0 in l:
                usr = await self.client.fetch_user(a[l.index(0)])
                await ctx.send(f'Đoán xem, hôm nay là sinh nhật của {usr.mention}\n')
                for i in range(len(l)):
                    if l[i] == nearest:
                        nr_id = a[i]
                        nr_bd = b[i]
                        usr = await self.client.fetch_user(nr_id)
                        await ctx.send(f'Ngoài ra, sắp tới là sinh nhật của {usr.name} vào ***{nr_bd}*** (còn {nearest} ngày)\n')
            else:
                for i in range(len(l)):
                    if l[i] == nearest:
                        nr_id = a[i]
                        nr_bd = b[i]
                        usr = await self.client.fetch_user(nr_id)
                        await ctx.send(f'Sinh nhật gần nhất là của {usr.name} vào ***{nr_bd}*** (còn {nearest} ngày)\n')
        elif args[0] in '123456781011':
            allab = get_bd()
            a = []
            b = []
            names = []
            bods = []
            for i in allab:
                a.append(i.split(' - ')[0])
                b.append(i.split(' - ')[1])
            for i in range(len(b)):
                if int(b[i][-2:]) == int(args[0]):
                    names.append(a[i])
                    bods.append(b[i])
                # print(bods)
            b = (list(dict.fromkeys(bods)))
            b.sort()
            a = []
            for i in range(len(bods)):
                a.append({'name': names[i], 'bod':bods[i]})
            
            def myFunc(e):
                return e['bod']

            a.sort(key=myFunc)

            embed = discord.Embed(title=f'Sinh nhật tháng {args[0]}', description=f'Danh sách những người có sinh nhật tháng {args[0]}', color=discord.Color.blue())

            for i in range(len(b)):
                value = ''
                for j in range(len(a)):
                    if b[i] == a[j]['bod']:
                        if value == '':
                            usr = await self.client.fetch_user(a[j]['name'])
                            value += usr.name
                        else:
                            usr = await self.client.fetch_user(a[j]['name'])
                            value += ', ' + usr.name
                embed.add_field(name=b[i], value=value, inline=False)

            mesg = await ctx.send(embed=embed)

            await mesg.add_reaction("🗑️")
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '🗑️' and reaction.message == mesg
            reaction, user = await self.client.wait_for('reaction_add', check=check)
            await mesg.delete()


    @commands.command(aliases=["who", 'whois', 'info'])
    @cooldown(1, 3, BucketType.user)
    async def whos(self, ctx, *, member: Optional[conv.FuzzyMember]=None):
        print(ctx.author.id)
        print('sent whos')

        list_id = get_user_id()
        list_name = get_user_name()
        allab = get_bd()
        a = []
        b = []
        for i in allab:
            a.append(i.split(' - ')[0])
            b.append(i.split(' - ')[1])

        member = member or ctx.author
        roles = [role for role in member.roles[1:]]
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
        embed.add_field(name="Roles:", value=" ".join([role.mention for role in roles]))
        embed.add_field(name='Tag:', value=member)
        mesg = await ctx.send(embed=embed)

        await mesg.add_reaction("❌")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '❌' and reaction.message == mesg
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await mesg.delete()


    @cog_ext.cog_slash(name="who", description="Xem thông tin ai đó",
    options=[
        create_option(
            name='user',
            description='Chọn một người',
            required=False,
            option_type=6,
        )
    ])
    async def _whos(self, ctx, user:str=None):
        member=None
        if not user:
            member = ctx.guild.get_member(ctx.author.id)
        else:
            member = ctx.guild.get_member(user.id)
            # await ctx.send(str(user.id))
            # print(member)

        list_id = get_user_id()
        list_name = get_user_name()
        allab = get_bd()
        a = []
        b = []
        for i in allab:
            a.append(i.split(' - ')[0])
            b.append(i.split(' - ')[1])

        # member = member or ctx.author
        roles = [role for role in member.roles[1:]]
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
        embed.add_field(name=f'Tham gia {ctx.guild.name}:', value=joined_at, inline=False)
        embed.add_field(name='CMND:', value=name)
        embed.add_field(name='CMND số:', value=str(member.id))
        if str(member.id) not in a:
            bd = 'Chưa đăng ký ngày sinh.'
            embed.add_field(name='Sanh thần:', value=bd)
        else:
            bd = datetime.strptime(b[a.index(str(member.id))],'%d/%m')
            embed.add_field(name='Sanh thần:', value=bd.strftime('Ngày %d tháng %m năm gì kệ'))
        if len(roles) >= 1:
            embed.add_field(name="Roles:", value=" ".join([role.mention for role in roles]))
        else:
            embed.add_field(name="Roles:", value="Không có")
        embed.add_field(name='Tag:', value=member)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(CMND(client))
