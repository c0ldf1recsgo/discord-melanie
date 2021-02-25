
import re

import discord
from discord.ext import commands
from googletrans import LANGCODES, LANGUAGES, Translator

GOOGLE_TRANSLATE = 'Google'
TRANSLATE_URL = 'https://translate.google.com/'
INVALID_LANG_CODE = '`{}`: Không hỗ trợ ngôn ngữ này hoặc sai code language'
NO_TEXT = 'Không có mẫu tin nào để chuyển'
SUPPORTED_LANGS = { 'auto': 'Automatic', **LANGUAGES, **LANGCODES}

EMOJI_REGEX = '(<a*(:[^:\s]+:)\d+>)'
CUSTOM_DICT = {
    'c0ldf1re': 'the best',
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
    print(dest, src)
    translated = translator.translate(text, dest=dest, src=src)
    translated_text = translated.text
    for word, meaning in CUSTOM_DICT.items():
        translated_text = translated_text.replace(word, meaning)

    embed = discord.Embed(description=f'Trứng: {text}\nZịt: {translated_text}', color=discord.Color.random())
    embed.set_author(name=GOOGLE_TRANSLATE, url=TRANSLATE_URL)
    embed.set_footer(text=f'Từ {translated.src} sang {translated.dest}')

    return embed