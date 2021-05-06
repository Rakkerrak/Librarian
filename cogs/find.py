import discord
from discord.ext import commands
from pymongo import MongoClient

from login import Connect
import cogs.embedder as embedder


class find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="find")
    async def find(self, ctx, field, *, message):
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



def setup(bot):
    bot.add_cog(find(bot))
