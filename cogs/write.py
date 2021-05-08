import json
import asyncio
import random
import datetime


import discord
from discord.ext import commands
from pymongo import MongoClient

from login import Connect
import cogs.embedder as embedder



def validator(newEntry):
    #this is just a  check. newJSON is a string, which is not the type pymongo uses for input
    try:
        dict= json.loads(newEntry)
    except:
        return False, "Syntax error. Could not write to json."

    requiredFields = ["_id", "title", "isbn", "author"]
    for field in requiredFields:
        if field not in dict:
            return False, f"Entry is missing {field}. Please check your spelling and capitalization and try again."

    return True, dict



def timecheck(queue, minutes):
    toDelete = []
    for idEntry in queue:
        entry = queue[idEntry]
        if datetime.datetime.now() > (entry["timestamp"] + datetime.timedelta(minutes = minutes)):
            toDelete.append(idEntry)

    for id in toDelete:
        queue.pop(id)

    return queue



class write(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    #TODO: .nextid

    @commands.command(name="write")
    async def write(self, ctx, *, newEntry):

        valid, result = validator(newEntry)

        if not valid:
            await ctx.send(result)
        else:
            rangen = random.randint(0,99999)
            while rangen in self.queue:
                rangen = random.randint(0,99999)
            self.queue[rangen] = {"entry": result, "userid": ctx.message.author.id, "timestamp": datetime.datetime.now() }
            await ctx.send(f"The id for your entry is {rangen} \nIt looks like this:")
            # await ctx.send(queue)
            await ctx.send(embed = embedder.book_embedder(result))
            await ctx.send(f"If you would like to proceed, please use the  `.insert {rangen}` command.")
            self.queue = timecheck(self.queue, 5)



    @commands.command(name="insert")
    async def insert(self, ctx, id):
        self.queue = timecheck(self.queue, 5)

        try:
            id = int(id)
        except:
            await ctx.send("That's not a number!")

        if id not in self.queue:
            await ctx.send("That id isn't active!  Try remaking your write request to get a new id.")
            return

        request = self.queue[id]

        if ctx.message.author.id == request["userid"]:
            await ctx.send("Writing!")

            connection = Connect.writer_connection()
            db = connection.library
            # verify = db.books.insert_one( request["entry"])
            await ctx.send("Added to database!")




def setup(bot):
    bot.add_cog(write(bot))
