import discord
from discord.ext import commands


class examples(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bookexample")
    async def bookexample(self, ctx):
        await ctx.send("```{'_id': 53, 'isbn': '9780553258559', 'title': 'Title of Book', 'author': 'Author Name', 'publisher': 'Publisher Name', 'publish_date': 'Date or Year', 'format': 'Softcover', 'language': 'Language'}```")
        await ctx.send("This works with key:value pairs.  All keys should be lowercase. All values need to have '    ' around them besides the ID.\nTo add a new field, add your 'key': 'value' pair at the end of the list.")

def setup(bot):
    bot.add_cog(examples(bot))
