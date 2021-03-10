# aos stands for Always On Services
from datetime import datetime
import pytz
import random

from discord.ext import commands, tasks

# def get_prefix():
#     with open('./cogs/prefixes.json', 'r') as f:
#         prefix = json.load(f)
#     return prefix['prefix']

class AOS(commands.Cog):

    def __init__(self, client):
        self.client = client
       

    @commands.Cog.listener()
    async def on_ready(self):
      self.hpbd.start()
      self.good_morning.start()
      
      
    @tasks.loop(seconds=86400)
    async def good_morning(self):
      dow = {'Mon': 'Thứ Hai', 'Tue': 'Thứ Ba', 'Wed':'Thứ Tư', 'Thu': 'Thứ Năm', 'Fri': 'Thứ Sáu', 'Sat': 'Thứ Bảy', 'Sun': 'Chủ Nhật'}
      t = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%a')
      d = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%d')
      m = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%m')
      y = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%Y')
      h = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%H')
      channel = self.client.get_channel(705598305857437696)
      # 797018066928009249 705598305857437696
      # await channel.send("test")
      if (int(h) >= 5 and int(h) <= 7):
        await channel.send(f'Buổi sáng vui vẻ nhé các bạn yêu :heart:.\nHôm nay là {dow[t]}, ngày {d} tháng {m} năm {y}')
        print('sent morning')


    @tasks.loop(seconds=86400)
    async def hpbd(self):
      bdquote = ['Bạn là một người bạn rất dễ thương! Chúc cho mọi sự như ý sẽ đến với bạn! Happy birthday to You! :partying_face:', 'Nhân dịp sinh nhật bạn nhé, chúc bạn luôn vui vẻ, thuận buồm xuôi gió trong công việc và hạnh phúc trong tình duyên. :partying_face:', 'Happy Birthday! Chúc bạn sinh nhật đầy ấm áp yêu thương và tiếng cười, thêm tuổi, thêm hạnh phúc, thêm nhiều niềm vui nhé. :partying_face:', 'Chúc bạn tuổi mới tiền vô như nước sức khỏe dồi dào. Sinh nhật vui vẻ. :partying_face:', 'Chẳng biết nói gì cả, chỉ biết chúc mừng sinh nhật bạn thôi :heart:, partytime :partying_face: :pinching_hand: :tada: ']

      allab = db['bd']
      a = []
      b = []
      for i in allab:
        a.append(i.split(' - ')[0])
        b.append(i.split(' - ')[1])
      today = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%d/%m')
      # print(f'Today is {today}')
      if today in b:
        channel = self.client.get_channel(705598305857437696)
        for i in range(len(b)):
          if today == b[i]:
            index = i
            # 797018066928009249 705598305857437696
            await channel.send(f'Đoán xem, hôm nay là sinh nhật của <@{a[index]}>\n' + random.choice(bdquote))
            print('sent happy bd')


def setup(client):
    client.add_cog(AOS(client))
