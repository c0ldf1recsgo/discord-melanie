from discord.ext import commands

SEPS = ['/', '-']

class DOB:
    def __init__(self, numbers, sep='-'):
        self.numbers = list(map(int, numbers))
        self.sep = sep

    def __str__(self):
        return self.sep.join(map(str, self.numbers))

def to_dob(s):
    for sep in SEPS:
        dob = s.split(sep)
        if len(dob) == 3:
            return DOB(dob, sep)
    raise commands.BadArgument('`dob` must be `DD/MM/YYYY` or `DD-MM-YYYY`.')


GENDERS = ['M', 'F']
MALE, FEMALE = 1, 2

def to_gender(s):
    s = s[0].upper()
    if s in GENDERS:
        return GENDERS.index(s) + 1
    if s == 'W':
        return FEMALE
    raise commands.BadArgument('`gender` must be `M/F/Male/Female/Men/Women`')

def get_gender_emote(gender):
    return '♂' if gender == MALE else '♀️'