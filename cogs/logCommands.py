import discord
from pymongo import MongoClient
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.commands import Option, SlashCommandGroup

cluster = MongoClient("mongodblink")

db1 = cluster["Anti-Link"]
cases = db1["cases"]
serveractions = db1["server-actions"]
messageactions = db1["message-actions"]
whitelistedlinks = db1["whitelisted-links"]
adminbypassdb = db1["admin-bypass"]
antilinkstatus = db1["antilinkstatus"]
serverlogs = db1["server-logs"]
whitelistedchannels = db1["whitelisted-channels"]

class logCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    logs = SlashCommandGroup("logs", "Commnads related to logs.")

    @logs.command()
    @has_permissions(administrator=True)
    async def set(self, ctx, channel: discord.TextChannel, logtype: Option(str, "Please select the log type you want.", choices=["Minimalism", "Maximalism"])):
        """Customize the way Anti-Link sends logs."""
        serverid = ctx.guild.id

        if serverlogs.count_documents({"_id": serverid}):
            serverlogs.delete_one({"_id": serverid})
            serverlogs.insert_one({"_id": serverid, "channel": channel.id, "logtype": logtype})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {channel.mention} has been set as the logs channel.")

            await ctx.respond(embed=actionset)
        else:
            serverlogs.insert_one({"_id": serverid, "channel": channel.id, "logtype": logtype})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {channel.mention} has been set as the logs channel.")

            await ctx.respond(embed=actionset)
    
    @logs.command()
    @has_permissions(administrator=True)
    async def remove(self, ctx):
        """Delete your logs configuration."""
        serverid = ctx.guild.id

        if serverlogs.count_documents({"_id": serverid}):
            serverlogs.delete_one({"_id": serverid})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> The logs channel has been deleted.")

            await ctx.respond(embed=actionset)
        else:
            notenabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> The logs channel has not been set.")

            await ctx.respond(embed=notenabled)

def setup(bot):
    bot.add_cog(logCommands(bot))