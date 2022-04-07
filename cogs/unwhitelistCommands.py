import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from urlextract import URLExtract
from discord.ext.commands import has_permissions, MissingPermissions
from pymongo import MongoClient, results

cluster = MongoClient("mongodb+srv://Slinky:mtrRDORQGLFv4uWH@cluster0.yu7kv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db1 = cluster["Anti-Link"]
whitelistedlinks = db1["whitelisted-links"]
whitelistedroles = db1["whitelist-roles"]
whitelistedchannels = db1["whitelisted-channels"]
whitelistedmembers = db1["whitelisted-members"]

extractor = URLExtract()

class unwhitelistCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    unwhitelist = SlashCommandGroup("unwhitelist", "Commnads related to unwhitelisting.")

    @unwhitelist.command()
    @has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """Unwhitelist a channel so people can't send links."""
        channelid = channel.id
        serverid = ctx.guild.id
        customid =  channelid + serverid

        if whitelistedchannels.count_documents({"_id": customid}):
            whitelistedchannels.delete_one({"_id": customid})

            unwhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> I have unwhitelisted **{channel.name}** links can no longer be sent there.")

            await ctx.respond(embed=unwhitelisted)

        else:
            notwhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> That channel was not whitelisted.")

            await ctx.respond("**TIP:** do `/whitelistchannel` to whitelist a channel.", embed=notwhitelisted)

    @unwhitelist.command()
    @has_permissions(administrator=True)
    async def member(self, ctx, member: discord.Member):
        """Unwhitelist a member so they can't send links."""
        memberid = ctx.author.id
        serverid = ctx.guild.id
        customid = (int(memberid) + int(serverid))

        if whitelistedmembers.count_documents({"_id": customid}):
            whitelistedmembers.delete_one({"_id": customid})
            unwhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {member.name}#{member.discriminator} is now unwhitelisted and can't send links.")

            await ctx.respond(embed=unwhitelisted)

        else:
            whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> That member was not whitelisted.")

            await ctx.respond(embed=whitelisted)

    @unwhitelist.command()
    async def role(self, ctx, role: discord.Role):
        """Unwhitelist a role so people can't send links."""
        roleid = role.id
        serverid = ctx.guild.id
        customid = (int(roleid) + int(serverid))

        if whitelistedroles.count_documents({"_id": customid}):
            whitelistedroles.delete_one({"_id": customid})
            unwhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {role.name} is now unwhitelisted and can't send links.")

            await ctx.respond(embed=unwhitelisted)

        else:
            whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> That role was not whitelisted.")

            await ctx.respond(embed=whitelisted)

    @unwhitelist.command()
    async def link(self, ctx, link: str):
        """Unwhitelist a link so people can't send it."""
        link = link.lower()
        serverid = ctx.guild.id

        if whitelistedlinks.count_documents({"_id": f"{link}{serverid}"}):
            whitelistedlinks.delete_one({"_id": f"{link}{serverid}"})
            unwhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> **{link}** is now unwhitelisted and can't be sent.")

            await ctx.respond(embed=unwhitelisted)

        else:
            whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> That link was not whitelisted.")

            await ctx.respond(embed=whitelisted)

def setup(bot):
    bot.add_cog(unwhitelistCommands(bot))