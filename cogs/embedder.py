import discord

def book_embedder(book):
    embed = discord.Embed(title = book["title"], description = f"ID: {book['_id']}, ISBN: {book['isbn']}", color = 0x0a4309)
    for field in book:
        finished = ["title", "_id", "isbn"]
        if field not in finished:
            embed.add_field(name = field.title(), value = book[field], inline = True)
    return embed
