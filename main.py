import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from pymongo import MongoClient

import secrets
from login import Connect

#secrets format:
"""
token = str
reader = str -mongodb uri eg mongodb://user:password@ip:port/dbname?authSource=authdb
writer = str -mongodb uri
goodIDs = list of int -[int, int]
"""

bot = commands.Bot(command_prefix='.', description="A personal library database", case_insensitive=True)

if __name__ == "__main__":
    bot.cog_list=['cogs.find', 'cogs.examples', 'cogs.write']
    for cog in bot.cog_list:
        bot.load_extension(cog)

@bot.event
async def on_ready():
    print("Logged in. \n\nGuild list:")
    for guild in bot.guilds:
        print(guild.name)

#prevent bot from joining non-authorized guilds
@bot.event
async def on_guild_join(guild):
    if guild.id not in secrets.goodIDs:
        await guild.leave()

@bot.command(name="test")
async def test(ctx):
    message = await ctx.send("React!")
    # checkMark = bot.get_emoji(839142440266104852)
    messagebot = await message.add_reaction("✅")
    def check(reaction, user):
        return message.id == messagebot.id and user != message.author and str(reaction.emoji) == '✅'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Too long!")
    else:
        # recentMsgs = await ctx.history(limit=1).flatten()
        # msg = recentMsgs[0]
        # if msg.id == message.id:
        await ctx.send("Done!")




@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency, 2)} seconds.")


bot.run(secrets.token)
