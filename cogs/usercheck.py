import discord

import secrets


def usercheck(user):
    if user in secrets.goodUsers:
        return True
    else:
        return False
        
