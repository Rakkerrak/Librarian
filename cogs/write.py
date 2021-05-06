import json
import asyncio

import discord
from discord.ext import commands
from pymongo import MongoClient

from login import Connect
import cogs.embedder as embedder



def validator(newEntry):
    pass
    # #this is just a  check. newJSON is a string, which is not the type pymongo uses for input
    #
    #
    # try:
    #     newJSON = json.dumps(newEntry, ensure_ascii=False)
    # except:
    #     return False, "Syntax error. Could not write to json."
    #
    #
    # requiredFields = ["_id", "title", "isbn", "author"]
    # for field in requiredFields:
    #     if field not in json.loads(newJSON):
    #         return False, f"Entry is missing {field}. Please check your spelling and capitalization and try again."
    #
    #
    #
    # return True, json.loads(newJSON)




class write(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #TODO: .nextid

    @commands.command(name="write")
    async def find(self, ctx, *, newEntry):

        # valid, result = validator(newEntry)
        # await ctx.send(valid)
        # await ctx.send(json.dumps(newEntry))



        if not valid:
            await ctx.send(result)
        else:
            await ctx.send(content = "Add this book?")
            await ctx.send(result)
            await ctx.send(type(json.dumps(newEntry)))
            # await ctx.send(embed = embedder.book_embedder(result))

            message = await ctx.send("React!")
            # checkMark = bot.get_emoji(839142440266104852)
            await message.add_reaction("✅")
            def check(reaction, user):
                return user != message.author and str(reaction.emoji) == '✅'
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Too long!")
            else:
                await ctx.send("Done!")


        connection = Connect.writer_connection()
        db = connection.library








def setup(bot):
    bot.add_cog(write(bot))
