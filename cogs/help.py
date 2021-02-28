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
            "Dưới đây là những command cơ bản để sử dụng bot.\nĐể xem chi tiết nhất `{0}help [command]`"
            .format(prefix),
            color=0x00ff00)
            embedVar.add_field(
            name=":slight_smile: Chào, an ủi, trù ẻo", value="`hi`, `hello` | `sad`, `huhu` | `vui`, `haha`", inline=False)
            embedVar.add_field(
            name=":game_die: Trò chơi",
            value="`8ball`, `random`, `guess`, `loto`, `blackjack`",
            inline=False)
            embedVar.add_field(
            name=":credit_card: Chứng minh nhân dân", value="`cmnd`, `birthday`, `who`", inline=False)
            embedVar.add_field(
            name=":camera: Xem ảnh trai/gái hoặc đồ ăn", value="`boy`, `girl`, `food`", inline=False)
            embedVar.add_field(
            name=":hugging: Hành động", value="`slap`, `kiss`, `hug`, `pat`", inline=False)
            embedVar.add_field(
            name=":clown: Misc", value="`avatar`, `snipe`, `quote`, `math`, `currency`, `translate`", inline=False)
            embedVar.add_field(
            name=":wrench: Settings", value="`ping`, `prefix`, `nickname`", inline=False)
            embedVar.add_field(
            name=":military_medal: Levels and ranking", value="`level`, `lvl` | `leaderboard`, `rank`", inline=False)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['hello', 'hi', 'chao', 'bonjour', 'hola']:
            embedVar = discord.Embed(
            title="Chào", 
            description="Lệnh: `{0}hello` \n Aliases: `hello`,`hi`, `chao`, `bonjour`, `hola`\nXem `{0}help cmnd` để đặt tên và mình sẽ gọi bạn bằng cho lần chào sau nhé.".format(prefix), 
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['buon', 'sad', 'depressed', 'unhappy', 'upset', 'tramcam', 'huhu']:
            embedVar = discord.Embed(
            title="An ủi", 
            description="Lệnh: `{0}huhu`\n- Aliases: `buon`, `sad`, `depressed`, `unhappy`, `upset`, `tramcam`, `huhu`\n\nTrù ẻo: `{0}haha`\n\nXem danh sách các câu chúc được người dùng thêm vào: `{0}allchuc`".format(prefix), 
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['fun', 'vui', 'hanhphuc', 'lol', 'haha', 'happy', 'smile', 'hihi', 'hehe']:
            embedVar = discord.Embed(
            title="Trù ẻo:", 
            description="Lệnh: `{0}haha`\n- Aliases: `fun`, `vui`, `hanhphuc`, `cuoi`, `lol`, `haha`, `happy`, `smile`, `hihi`, `hehe`\n\nXem danh sách các câu trù được người dùng thêm vào: `{0}alltru`".format(prefix), 
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['tientri', 'yesno', 'quest', '8ball', '8b', 'h']:
            embedVar = discord.Embed(
            title="Bạn hỏi tôi trả lời",
            description="Nhập câu hỏi có không (yes/no) bất kì sau lệnh  `{0}8ball` và chờ câu trả lời từ tôi nhé.\nAliases: `tientri`, `yesno`, `quest`, `8ball`, `8b`, `h`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['rand', 'random', 'num']:
            embedVar = discord.Embed(
            title="Con số may mắn",
            description="Nhập các số nguyên vào sau lệnh `{0}random`:\n- Số trong đoạn từ a đến b hoặc b đến a: `{0}random` `[a]` `[b]`\n- Số trong đoạn từ 0 đến a: `{0}random` `[a]`\nAliases: `rand`, `random`, `num`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['doan', 'randlist', 'which', 'choose', 'guess', 'g']:
            embedVar = discord.Embed(
            title="Quyết định quan trọng",
            description="Nhập lệnh `{0}guess` `[lựa chọn 1]` `|` `[lựa chọn 2]` và xem kết quả nhé. Có thể thêm nhiều lựa chọn, ngăn cách các lựa chọn bằng dấu `|`.\nAliases: `doan`, `randlist`, `which`, `choose`, `guess`, `g`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['m', 'cal', 'calculate', 'tinh']:
            embedVar = discord.Embed(
            title="Siêu trí tuệ",
            description="Nhập phép tính sau lệnh `{0}math` và xem tôi tính nhanh thế nào nhé.\nAliases: `m`, `cal`, `calculate`, `tinh`.\nDùng các dấu `+ - * /` chứ đừng dùng *cộng trừ nhân chia* nhé. :(\n\n**Loto:**\n Nhập `{0}help lt` hoặc `{0}help loto` để xem chi tiết hơn nhé.\n\n**Xì zách:**\n Nhập `{0}help bj` hoặc `{0}help blackjack` để xem chi tiết hơn nhé.".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['cmnd', 'allcmnd']:
            embedVar = discord.Embed(
            title="Đăng ký lý lịch",
            description="- Đăng ký một cái tên thật đẹp để mình có thể biết bạn là ai. Dùng lệnh `{0}cmnd [tên bạn muốn được gọi]`.\n- Kiểm tra tên mình có trong danh sách không: `{0}allcmnd`\n- Sửa tên riêng: `{0}cmndedit [tên bạn muốn được gọi]`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['bd', 'birthday', 'bde', 'bdedit', 'birthdayedit']:
            embedVar = discord.Embed(
            title="Đăng ký sinh nhật",
            description="Đăng ký ngày sinh để được chúc mừng vào ngày sinh nhật nhé :heart:. Dùng lệnh `{0}birthday [dd/mm]`.\nAliases: `bd`\n- Kiểm tra xem mình đã đăng ký sinh nhật chưa: `{0}birthday`\nAliases: `bd`\n- Sửa sinh nhật: `{0}birthdayedit [dd/mm]`\nAliases: `bde`, `bdedit`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['bd', 'birthday', 'bde', 'bdedit', 'birthdayedit']:
            embedVar = discord.Embed(
            title="Thông tin cá nhân:",
            description="Xem thông tin cá nhân: `{0}who`. Có thể thêm @tag sau câu lệnh.\nAliases: `whos`, `whois`, `info`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['girl', 'xinh', 'simp', 'gai', 'trai', 'zai', 'boy', 'handsome', 'man', 'food']:
            embedVar = discord.Embed(
            title="Xem ảnh gái xinh hoặc đồ ăn",
            description="- Xem ảnh gái xinh: `{0}girl`.\nAliases: `girl`, `xinh`, `simp`, `gai`\n\n- Xem ảnh trai: `{0}trai`.\nAliases: `trai`, `zai`, `boy`, `handsome`, `man`\n\n- Xem ảnh đồ ăn: `{0}food`.".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['slap','kiss', 'hug', 'pat']:
            embedVar = discord.Embed(
            title="Hành động",
            description="- Gửi các hành động gif: `{0}[action]`.\nAliases: `slap`,`kiss`, `hug`, `pat`\n\nCó thể tag người khác bằng lệnh `{0}[action]` + `[@user]`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['avatar', 'ava']:
            embedVar = discord.Embed(
            title="Xem avatar",
            description="- Của bản thân: `{0}avatar`.\n- Của người khác: `{0}avatar` + `[@user]`\nAliases: `avatar`, `ava`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['quote', 'quotes', 'inspire', 'q']:
            embedVar = discord.Embed(
            title="Xem câu nói bất kì",
            description="Lệnh: `{0}quote`.\nAliases: `quote`, `quotes`, `inspire`, `q`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['say', 's', 'sayemo', 'se']:
            embedVar = discord.Embed(
            title="Bot sủa",
            description="**Thường:** `{0}say`.\nAliases: `s`\n\n**Bot sủa bằng emoji:** `{0}sayemo`.\nAliases: `se`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['currency', 'cur']:
            embedVar = discord.Embed(
            title="Chuyển đổi tiền tệ",
            description="Lệnh: `{0}currency [số tiền] [trước] [sau]`.\nAliases: `cur`\n\n**Dịch:** `{0}translate [lang1]>[lang2] [trước] [sau]`.\nAliases: `tr`, `trans`".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['currency', 'cur']:
            embedVar = discord.Embed(
            title="Dịch ngôn ngữ",
            description="**Dịch:** `{0}translate [lang1]>[lang2] [trước] [sau]`.\nAliases: `tr`, `trans`\n\nKhi không có `[lang1]>[lang2]` sẽ tự động dịch sang tiếng Việt.".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['ping', 'prefix', 'nick']:
            embedVar = discord.Embed(
            title="Cài đặt, tùy biến",
            description="- Ping: `{0}ping`.\n\n- Sửa prefix: `{0}prefix [new_prefix]`\n\n- Sửa nickname: `{0}nick @tag [new_nickname]`\nChỉ sửa được nickname của bản thân nhưng phải tag bản thân vào nhé :))))".format(prefix),
            color=0x00ff00)
            msg = await ctx.channel.send(embed=embedVar)
        elif args[0] in ['level', 'lvl', 'leaderboard', 'rank', 'levels', 'levelupdisable', 'levelupd', 'lvlupd', 'levelupenable', 'levelupe', 'lvlupe']:
            embedVar = discord.Embed(
            title="Levels and Ranking",
            description="- Tắt/bật thông báo lên cấp: `{0}levelupdisable`|`levelupd`|`lvlupd`, `{0}levelupenable`|`levelupe`|`lvlupe`\n\n- Kiểm tra cấp độ: `{0}level`.\nAliases: `lvl`\n\n- Xem top xếp hạng: `{0}rank`\nAliases: `leaderboard`, `levels`\n\n***Lưu ý:*** Hai lệnh trên chỉ được thực hiện tại kênh  #🔥-spam-bot-🤖 .Hệ thống sẽ chỉ tính điểm với thời gian giữa các tin nhắn vừa đủ nên spam sẽ không được tính. Đồng thời chỉ các kênh trong mục **【Kênh Chat】** mới được công nhận.".format(prefix),
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
        elif args[0] in ['spy', 'snipe']:
            embedVar = discord.Embed(
            title="Xem tin đã xóa",
            description="- Dùng lệnh:  `{0}snipe`.\nAliases: `spy`\n\n- Xem danh sách các tin đã xóa gần nhất:  `{0}snipelog`.\nAliases: `snipel`, `snlog`, `spylog`, `spyl`".format(prefix),
            color=0x34ebae)
            msg = await ctx.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
            title="Hướng dẫn sử dụng BOT",
            description=
            "Lệnh này không tồn tại hoặc không đúng, vui lòng kiểm tra lại.\nĐể xem chi tiết nhất `{0}help [command]`\n"
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
