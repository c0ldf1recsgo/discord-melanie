import difflib
import typing
from unidecode import unidecode

import discord
from discord.ext import commands

DEFAULT_MATCHING = 0.1

class FuzzyMemberConverter(commands.MemberConverter):
    def __init__(self, *, matching=DEFAULT_MATCHING):
        self.matching = matching
    
    async def convert(self, ctx, argument):
        try:
            member = await super().convert(ctx, argument)
        except:
            member = find_member(ctx, argument, self.matching)
            if member:
                return member
            raise

FuzzyMember = typing.Union[discord.Member, FuzzyMemberConverter]

ROLE_SCORE_WEIGHT = 0.05
MATCH_RETURNS = 10
WHOLE_WORD_POINTS = 0.25

def find_member(context, input_name, matching=DEFAULT_MATCHING, contains_all_only=True):
    input_name = input_name.lower()
    members = context.guild.members
    members = [m for m in members if input_in_possible_names(m, input_name)]
    
    members_by_name = {}
    for m in members:
        members_by_name[m.name.lower()] = m
        if m.name != m.display_name:
            members_by_name[m.display_name.lower()] = m
    close_matches = difflib.get_close_matches(input_name, members_by_name, MATCH_RETURNS, matching)
    
    def score_member(member_name):
        similarity = match_ratio(input_name, member_name)
        include_score = WHOLE_WORD_POINTS if input_name in member_name or member_name in input_name else 0

        member = members_by_name[member_name]
        role_score = score_member_role(context.guild, member)
        weighted_role_score = role_score * ROLE_SCORE_WEIGHT
        total_score = similarity + weighted_role_score + include_score

        return total_score

    close_matches.sort(key=lambda name: score_member(name), reverse=True)

    member = None
    if close_matches:
        name = close_matches[0]
        member = members_by_name[name]
    
    return member


def input_in_possible_names(member, input_name):
    member_name = unidecode(member.name.lower())
    display_name = unidecode(member.display_name.lower())
    input_name = unidecode(input_name)
    input_in_username = contains_the_other(member_name, input_name)
    input_in_display_name = contains_the_other(display_name, input_name) if member_name != display_name else False
    return input_in_username or input_in_display_name

def contains_the_other(a, b):
    return contains_all_chars(a, b) or contains_all_chars(b, a)

def contains_all_chars(a, b):
    return all(char in b for char in a)

def match_ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def score_member_role(guild, member):
    role_count = len(guild.roles)
    role_score = [role.position / role_count for role in member.roles]
    return sum(role_score)