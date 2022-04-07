import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.AutoShardedBot(shard_count=5, intents=intents, status=discord.Status.dnd)

@bot.event
async def on_ready():
    print("anti-link is ready!")

if discord.AutoShardedBot.is_ws_ratelimited == True:
    print("websocket is ratelimited")
else:
    print("websocket is not ratelimited")

extensions = ["cogs.whitelistCommands", "cogs.unwhitelistCommands", "cogs.infoCommands", "cogs.messageEvent", "cogs.configCommands"]

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)
        
bot.run('bottoken')