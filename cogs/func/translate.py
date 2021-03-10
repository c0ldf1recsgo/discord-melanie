import random
import re

import discord
from discord.ext import commands
from googletrans import LANGCODES, LANGUAGES, Translator

GOOGLE_TRANSLATE = ['Google bảo rằng', 'Dù sao thì', 'Cuộc đời này thật lắm éo le', 'Lời nói chẳng mất tiền mua', 'Được dịch bởi Guốc Le', 'Dù đúng dù sai']
TRANSLATE_URL = 'https://translate.google.com/'
INVALID_LANG_CODE = '`{}`: Không hỗ trợ ngôn ngữ này hoặc sai code language'
NO_TEXT = 'Không có mẫu tin nào để chuyển'
SUPPORTED_LANGS = { 'auto': 'Automatic', **LANGUAGES, **LANGCODES}

EMOJI_REGEX = '(<a*(:[^:\s]+:)\d+>)'
CUSTOM_DICT = {
    'c0ldf1re': 'the best',
    'trlz': 'thì ra là zậy',
    'mctd': 'mọc CHÂN trên đầu',
    'thr': 'toi hieu roi',
    'tch': 'toi chua hieu',
    'gumball': 'zyzy\'s',
    'zyzy': 'gumball\'s',
    'bomman': 'úi zời ơi dễ vãi L0L',
    'minh nghi': 'ny ny',
    '01i': 'không một ai, không ai cả, không ai muốn nghe, muốn hiểu tôi nói gì cả',
    'trần dần': 'tiên tri vũ trụ vô địch',
    'huấn rose': 'không nàm mà đòi có ăn thì có mà ăn đầu bò, ăn mứt',
    'btd': 'bao thì đi',
    'btđ': 'bao thì đi',
    'kd': 'khùm đean'
}

translator = Translator()

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def Src2Dest(s):
    src2dest = s.split('>')
    if len(src2dest) != 2:
        raise commands.BadArgument('Vui lòng nhập đúng định dạng `[trước]>[sau]`.')
    
    src, dest = src2dest
    src = src or 'auto'
    dest = dest or 'en'
    return '>'.join([src, dest])

def translate(src2dest, text):
    global translator

    emojis_to_clean = re.findall(EMOJI_REGEX, text)
    for full, clean in emojis_to_clean:
        text = text.replace(full, clean)

    src2dest = src2dest.split('>')
    for lang in src2dest:
        if lang and lang not in SUPPORTED_LANGS:
            raise commands.BadArgument(INVALID_LANG_CODE.format(lang))
    src, dest = src2dest

    translated = dotdict({ 
        'text': 'Google Translate đã ngủm!',
        'src': '...',
        'dest': '...',
    })
    # for i in range(10):
    #     try:
    #         translated = translator.translate(text, dest=dest, src=src)
    #         break
    #     except AttributeError as e:
    #         translator = Translator()
    # translated = translator.translate(text, dest=dest, src=src)
    translator = Translator()
    print(text)
    # print(dest, src)
    translated = translator.translate(text, dest=dest, src=src)
    translated_text = translated.text
    for word, meaning in CUSTOM_DICT.items():
        translated_text = translated_text.replace(word, meaning)

    embed = discord.Embed(description=f'Từ: {text}\nCũng thành: {translated_text}', color=discord.Color.random())
    embed.set_author(name=random.choice(GOOGLE_TRANSLATE), url=TRANSLATE_URL)
    embed.set_footer(text=f'Từ {translated.src} sang {translated.dest}')

    return embed
