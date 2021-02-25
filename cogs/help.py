from replit import db

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

def get_prefix():
    return db['prefix'][0]

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command()
    @cooldown(1, 1, BucketType.user)
    async def help(self, ctx, *args):
        prefix = get_prefix()
        if ctx.author == self.client.user:
            return
        print(ctx.author.id)
        print('sent help')
        if not args:
            embedVar = discord.Embed(
            title="Hướng dẫn sử dụng BOT",
            description=
            "Dưới đây là những command cơ bản để sử dụng bot. Để xem chi tiết nhất `{0}help [number]`"
            .format(prefix),
            color=0x00ff00)
            embedVar.add_field(
            name="1. Chào, an ủi, trù ẻo", value="hi, hello | sad, huhu | vui, haha", inline=False)
            embedVar.add_field(
            name="2. Trò chơi",
            value="8ball, random, guess, loto, blackjack",
            inline=False)
            embedVar.add_field(
            name="3. Chứng minh nhân dân", value="Đăng ký tên, birthday, kiểm tra thông tin", inline=False)
            embedVar.add_field(
            name="4. Xem ảnh trai/gái hoặc đồ ăn", value="Trai xinh, gái đẹp và đồ ăn ngon", inline=False)
            embedVar.add_field(
            name="5. Hành động", value="slap, kiss, hug, pat", inline=False)
            embedVar.add_field(
            name="6. Misc", value="quote, math, currency", inline=False)
            embedVar.add_field(
            name="7. Settings", value="ping, prefix, nickname", inline=False)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(1) or args[0] == 'hello':
            embedVar = discord.Embed(
            title="Chào, an ủi, trù ẻo", 
            description="Dùng lệnh `{0}hello` \n Aliases: `hello`,`hi`, `chao`, `bonjour`, `hola`\nXem `{0}help 5` để đặt tên và mình sẽ gọi bạn bằng cho lần chào sau nhé.\n\nAn ủi: `{0}huhu`\n- Aliases: `buon`, `sad`, `depressed`, `unhappy`, `upset`, `tramcam`, `huhu`\n\nTrù ẻo: `{0}haha`\n- Aliases: `fun`, `vui`, `hanhphuc`, `cuoi`, `lol`, `haha`, `happy`, `smile`, `hihi`, `hehe`\n\nXem danh sách các câu chúc/trù được người dùng thêm vào: `{0}allchuc` hoặc `{0}alltru`".format(prefix), 
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(2) or args[0] == 'game':
            embedVar = discord.Embed(
            title="Trò chơi giải trí",
            description="**Bạn hỏi tôi trả lời:**\nNhập câu hỏi có không (yes/no) bất kì sau lệnh  `{0}8ball` và chờ câu trả lời từ tôi nhé.\nAliases: `tientri`, `yesno`, `quest`, `8ball`, `8b`, `h`\n\n**Con số may mắn:**\nNhập các số nguyên vào sau lệnh `{0}random`:\n- Số trong đoạn từ a đến b hoặc b đến a: `{0}random` `[a]` `[b]`\n- Số trong đoạn từ 0 đến a: `{0}random` `[a]`\nAliases: `rand`, `random`, `num`\n\n**Quyết định quan trọng:**\nNhập lệnh `{0}guess` `[lựa chọn 1]` `|` `[lựa chọn 2]` và xem kết quả nhé. Có thể thêm nhiều lựa chọn, ngăn cách các lựa chọn bằng dấu `|`.\nAliases: `doan`, `randlist`, `which`, `choose`, `rl`, `g`\n\n **Siêu trí tuệ:**\nNhập phép tính sau lệnh `{0}math` và xem tôi tính nhanh thế nào nhé.\nAliases: `m`, `cal`, `calculate`, `tinh`.\nDùng các dấu `+ - * /` chứ đừng dùng *cộng trừ nhân chia* nhé. :(\n\n**Loto:**\n Nhập `{0}help lt` hoặc `{0}help loto` để xem chi tiết hơn nhé.\n\n**Xì zách:**\n Nhập `{0}help bj` hoặc `{0}help blackjack` để xem chi tiết hơn nhé.".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(3):
            embedVar = discord.Embed(
            title="Đăng ký lý lịch",
            description="1. Đăng ký một cái tên thật đẹp để mình có thể biết bạn là ai. Dùng lệnh `{0}cmnd [tên bạn muốn được gọi]`.\nKiểm tra tên mình có trong danh sách không: `{0}allcmnd`\n\n2. Đăng ký luôn cái ngày sinh để được chúc mừng vào ngày sinh nhật nhé :heart:. Dùng lệnh `{0}birthday [dd/mm]`.\nAliases: `bd`\n- Kiểm tra xem mình đã đăng ký sinh nhật chưa: `{0}birthday`\nAliases: `bd`\n- Sửa sinh nhật hoặc tên riêng: `{0}birthdayedit [dd/mm]` hoặc `{0}cmndedit [tên bạn muốn được gọi]`\nAliases: `bde`, `bdedit`\n\n- Xem thông tin cá nhân: `{0}who`. Có thể thêm @tag sau câu lệnh.\nAliases: `whos`, `whois`, `info`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(4):
            embedVar = discord.Embed(
            title="Xem ảnh gái xinh và đồ ăn",
            description="- Xem ảnh gái xinh: `{0}girl`.\nAliases: `girl`, `xinh`, `simp`, `gai`\n\n- Xem ảnh trai: `{0}trai`.\nAliases: `trai`, `zai`, `boy`, `handsome`, `man`\n\n- Xem ảnh đồ ăn: `{0}food`.".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(5) or args[0] == 'action':
            embedVar = discord.Embed(
            title="Hành động",
            description="- Gửi các hành động gif: `{0}[action]`.\nAliases: `slap`,`kiss`, `hug`, `pat`\n\nCó thể tag người khác bằng lệnh `{0}[action]` + `[@user]`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(6) or args[0] == 'misc':
            embedVar = discord.Embed(
            title="Miscellaneous",
            description="**Xem câu nói bất kì:** `{0}quote`.\nAliases: `quote`, `quotes`, `inspire`, `q`\n\n**Bot sủa:** `{0}say`.\nAliases: `s`\n\n**Bot sủa bằng emoji:** `{0}sayemo`.\nAliases: `se`\n\n**Chuyển đổi tiền tệ:** `{0}currency [số tiền] [trước] [sau]`.\nAliases: `cur`\n\n".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] == str(7) or args[0] == 'settings':
            embedVar = discord.Embed(
            title="Settings",
            description="- Ping: `{0}ping`.\n\n- Sửa prefix: `{0}prefix [new_prefix]`\n\n- Sửa nickname: `{0}nick @tag [new_nickname]`\nChỉ sửa được nickname của bản thân nhưng phải tag bản thân vào nhé :))))".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['lt', 'loto']:
            embedVar = discord.Embed(
            title="Trò chơi LôTô",
            description="Bắt đầu trò chơi trước rồi mới được thực hiện các chức năng khác nhé. Vui chơi lành mạnh nào. \n\n- Bắt đầu trò chơi bằng lệnh:  `{0}lotostart`.\nAliases: `lotos`, `ltstart`, `lts`\n\n- Quay số:  `{0}loto`.\nAliases: `lt`\n\n- Kiểm tra kết quả:  `{0}lotocheck` `a b c d e`\nAliases: `lotoc`, `ltc`, `ltcheck`\n\n- Xem các số đã quay:  `{0}lotoall`\nAliases: `lotoa`, `lta`, `ltall`\n\n- Kết thúc và xóa toàn bộ:  `{0}lotoend`\nAliases: `lotoe`, `lte`, `ltend`".format(prefix),
            color=0x34ebae)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['bj', 'blackjack']:
            embedVar = discord.Embed(
            title="Trò chơi Xì Zách",
            description="`{0}blackjack` hoặc `{0}bj` để xem tiếp hướng dẫn. :yaya:".format(prefix),
            color=0x34ebae)
            msg = await ctx.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
            title="Hướng dẫn sử dụng BOT",
            description=
            "Để xem chi tiết nhất `{0}help [number]`\nNumber trong khoảng từ 1 đến 7."
            .format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)

        await msg.add_reaction("🗑️")
        def check(reaction, user):
            return user == ctx.author
        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await msg.delete()


def setup(client):
    client.add_cog(Help(client))