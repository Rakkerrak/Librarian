import discord
from discord.ext import commands
from pymongo import MongoClient

from login import Connect
import cogs.embedder as embedder
import cogs.usercheck as usercheck


class find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="find")
    async def find(self, ctx, field, *, message):
        if usercheck.usercheck(ctx.message.author.id) == False:
            await ctx.send("You're not authorized to use that command!")
            return
        connection = Connect.reader_connection()
        db = connection.library
        value = f"{message}"
        if field == "_id":
            value = int(message)
        cursor = db.books.find( {f"{field}": value })
        if len(list(cursor)) == 0:
            cursor = db.books.find( { f"{field}": {"$regex": f"{value}*"}} )
        else:
            cursor = db.books.find( {f"{field}": value })
        count = 0
        for book in cursor:
            # await ctx.send(book)
            await ctx.send(embed = embedder.book_embedder(book))
            count += 1
            if count >= 10:
                break
        await ctx.send("Done!")

    @commands.command(name="nextid")
    async def nextid(self, ctx):
        if usercheck.usercheck(ctx.message.author.id) == False:
            await ctx.send("You're not authorized to use that command!")
            return
        connection = Connect.reader_connection()
        db = connection.library
        cursor = db.books.aggregate([{"$sort" : { "_id" : -1 }}]).batch_size(1)
        book = cursor.next()
        await ctx.send(f"Most recently used id is {book['_id']}")
        count = db.books.count_documents({})
        await ctx.send(f"There are {count} books in total.")



def setup(bot):
    bot.add_cog(find(bot))
