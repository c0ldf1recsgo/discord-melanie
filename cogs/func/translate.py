# pylint: disable=anomalous-backslash-in-string

import random
import re

import discord
from discord.ext import commands
from googletrans import LANGCODES, LANGUAGES, Translator

from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://blah-blah-blah")

collection = cluster['discord']['dict']

# GOOGLE_TRANSLATE = ['Google bảo rằng', 'Dù sao thì', 'Cuộc đời này thật lắm éo le', 'Lời nói chẳng mất tiền mua', 'Được dịch bởi Guốc Le', 'Dù đúng dù sai']
GOOGLE_TRANSLATE = ['GOOGLE TRANSLATE', 'FROM GOOGLE WITH LOVE']
TRANSLATE_URL = 'https://translate.google.com/'
INVALID_LANG_CODE = '`{}`: Không hỗ trợ ngôn ngữ này hoặc sai code language'
NO_TEXT = 'Không có mẫu tin nào để chuyển'
SUPPORTED_LANGS = { 'auto': 'Automatic', **LANGUAGES, **LANGCODES, 'hcmus': 'hcmus'}

EMOJI_REGEX = '(<a*(:[^:\s]+:)\d+>)'
# CUSTOM_DICT = {
#     'c0ldf1re': 'the best',
#     'trlz': 'thì ra là zậy',
#     'mctd': 'mọc CHÂN trên đầu',
#     'thr': 'toi hieu roi',
#     'tch': 'toi chua hieu',
#     'zyzy': "everyone's",
#     'bomman': 'úi zời ơi dễ vãi L0L',
#     'minh nghi': 'ny ny',
#     '01i': 'không một ai, không ai cả, không ai muốn nghe, muốn hiểu tôi nói gì cả',
#     'trần dần': 'tiên tri vũ trụ vô địch',
#     'huấn rose': 'không nàm mà đòi có ăn thì có mà ăn đầu bò, ăn mứt',
#     'btd': 'bao thì đi',
#     'btđ': 'bao thì đi',
#     'kd': 'khùm đean',
#     'g0': 'game khong',
#     'n3t': 'ba hoang giuong chieu',
#     'cdxl': 'con đĩa xào lăn',
#     'scd': 'sao cụng đượt',
#     'bckd': 'bao cung khong di'
# }

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
    dest = dest or 'vi'
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
    translator = Translator()
    print(text)

    key_list = list(LANGCODES.keys())
    val_list = list(LANGCODES.values())
    # position = val_list.index('vi')
    # print(key_list[position].capitalize())

    db = collection.find_one({text.lower(): {"$exists": True}})
    if db != None and text.lower() not in ['id', '_id'] and dest == 'hcmus':
    # if text.lower() in CUSTOM_DICT.keys() and dest == 'hcmus':
        translated_text = db[text.lower()]
        # translated_text = CUSTOM_DICT.get(text.lower())
        embed = discord.Embed(description=f'Dịch:  `{text}`\nThành:  `{translated_text}`', color=discord.Color.random())
        embed.set_author(name='Từ điển H C M U S')
        embed.set_footer(text=f'Ngôn ngữ ngoài hành lang')
    elif dest == 'hcmus':
        translated = translator.translate(text, dest='vi', src=src)
        if translated.src == 'vi' and translated.dest == 'vi':
            translated = translator.translate(text, dest='en', src='vi')
        translated_text = translated.text
        embed = discord.Embed(description=f'Dịch:  `{text}`\nThành:  `{translated_text}`', color=discord.Color.random())
        embed.set_author(name=random.choice(GOOGLE_TRANSLATE), url=TRANSLATE_URL, icon_url='https://www.xanjero.com/wp-content/uploads/2019/07/Google-Translate-app-camera-update.png')
        position = val_list.index(translated.src)
        position_d = val_list.index(translated.dest)
        embed.set_footer(text=f'Từ {translated.src} ({key_list[position].capitalize()}) sang {translated.dest} ({key_list[position_d].capitalize()})')
    else:
        translated = translator.translate(text, dest=dest, src=src)
        translated_text = translated.text
        embed = discord.Embed(description=f'Dịch:  `{text}`\nThành:  `{translated_text}`', color=discord.Color.random())
        embed.set_author(name=random.choice(GOOGLE_TRANSLATE), url=TRANSLATE_URL, icon_url='https://www.xanjero.com/wp-content/uploads/2019/07/Google-Translate-app-camera-update.png')
        position = val_list.index(translated.src)
        position_d = val_list.index(translated.dest)
        embed.set_footer(text=f'Từ {translated.src} ({key_list[position].capitalize()}) sang {translated.dest} ({key_list[position_d].capitalize()})')

    return embed
