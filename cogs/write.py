import json
import asyncio
import random
import datetime


import discord
from discord.ext import commands
from pymongo import MongoClient

from login import Connect
import cogs.embedder as embedder
import cogs.usercheck as usercheck


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
    #checks to make sure there are no timed out entries in the queue
    toDelete = []
    for idEntry in queue:
        entry = queue[idEntry]
        if datetime.datetime.now() > (entry["timestamp"] + datetime.timedelta(minutes = minutes)):
            toDelete.append(idEntry)

    for id in toDelete:
        queue.pop(id)

    return queue


def checkid(queue, id):
    #checks if an id is an int and in the current queue
    try:
        id = int(id)
    except:
        return False,"That's not a number!"

    if id not in queue:
        return False, "That id isn't active!  Try remaking your write request to get a new id."

    return True, "Good ID"


class write(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}


    @commands.command(name="write")
    async def write(self, ctx, *, newEntry):
        self.queue = timecheck(self.queue, 5)
        if usercheck.usercheck(ctx.message.author.id) == False:
            await ctx.send("You're not authorized to use that command!")
            return

        valid, result = validator(newEntry)

        if not valid:
            await ctx.send(result)
        else:
            rangen = random.randint(0,99999)
            while rangen in self.queue:
                rangen = random.randint(0,99999)
            self.queue[rangen] = {"entry": result, "userid": ctx.message.author.id, "timestamp": datetime.datetime.now() }
            await ctx.send(f"The id for your entry is {rangen} \nIt looks like this:")
            await ctx.send(embed = embedder.book_embedder(result))
            await ctx.send(f"If you would like to proceed, please use the  `.insert {rangen}` command.")
            self.queue = timecheck(self.queue, 5)



    @commands.command(name="insert")
    async def insert(self, ctx, id):
        self.queue = timecheck(self.queue, 5)
        if usercheck.usercheck(ctx.message.author.id) == False:
            await ctx.send("You're not authorized to use that command!")
            return

        check, response = checkid(self.queue, id)
        if check == False:
            await ctx.send(response)
            return

        id = int(id)
        request = self.queue[id]
        entry = request["entry"]

        if ctx.message.author.id == request["userid"]:
            await ctx.send("Writing!")

            connection = Connect.writer_connection()
            db = connection.library
            # verify = db.books.insert_one( request["entry"])
            await ctx.send(f"Added {entry} to database!")

    @commands.command(name="viewqueue")
    async def viewqueue(self, ctx):
        self.queue = timecheck(self.queue, 5)
        current = []
        for id in self.queue:
            current.append(id)
        await ctx.send (f"Current items in queue: {current}")

    @commands.command(name="viewfullqueue")
    async def viewfullqueue(self, ctx):
        self.queue = timecheck(self.queue, 5)
        await ctx.send(self.queue)

    @commands.command(name="viewid")
    async def viewid(self, ctx, *ids):
        self.queue = timecheck(self.queue, 5)
        for id in ids:
            check, response = checkid(self.queue, id)
            if check == False:
                await ctx.send(response)
            else:
                # await ctx.send(self.queue[id])
                id = int(id)
                entry = self.queue[id]
                book = entry["entry"]
                await ctx.send(embed = embedder.book_embedder(book))




def setup(bot):
    bot.add_cog(write(bot))
