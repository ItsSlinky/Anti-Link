import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from urlextract import URLExtract
from discord.ext.commands import has_permissions, MissingPermissions
from pymongo import MongoClient, results

cluster = MongoClient("mongodblink")

db1 = cluster["Anti-Link"]
whitelistedlinks = db1["whitelisted-links"]
whitelistedroles = db1["whitelist-roles"]
whitelistedchannels = db1["whitelisted-channels"]
whitelistedmembers = db1["whitelisted-members"]

extractor = URLExtract()

class whitelistCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    whitelist = SlashCommandGroup("whitelist", "Commnads related to whitelisting.")

    @whitelist.command()
    @has_permissions(administrator=True)
    async def member(self, ctx, member: discord.Member):
        """Whitelist a member so they can send links."""
        memberid = ctx.author.id
        guildid = ctx.guild.id
        customid = memberid + guildid

        if whitelistedmembers.count_documents({"_id": customid}):
            alreadywhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> That member is already whitelisted.")

            await ctx.respond(embed=alreadywhitelisted)
        else:
            whitelistedmembers.insert_one({"_id": customid})
            whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {member.name}#{member.discriminator} is now whitelised and can send links.")

            await ctx.respond(embed=whitelisted)

    @whitelist.command()
    @has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """Whitelist a channel so users can send links within the channel."""
        channelid = channel.id
        serverid = ctx.guild.id
        customid =  channelid + serverid
        if whitelistedchannels.count_documents({"_id": customid}):

            alreadywhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> **{channel.name}** seems to be already whitelisted.")

            await ctx.respond("**TIP:** do `/unwhitelistchannel` to unwhitelist a channel.", embed=alreadywhitelisted)

        else:
            whitelistedchannels.insert_one({"_id": customid})

            whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> I have whitelisted **{channel.name}** links can now be sent there.")

            await ctx.respond("**TIP:** do `/unwhitelistchannel` to unwhitelist a channel.", embed=whitelisted)

    @whitelist.command()
    @has_permissions(administrator=True)
    async def role(self, ctx, role: discord.Role):
        """Whitelist a role so users with the role can send links."""
        roleid = role.id
        serverid = ctx.guild.id
        customid = roleid + serverid

        if whitelistedroles.count_documents({"_id": customid}):

            alreadywhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> **{role.name}** seems to be already whitelisted.")

            await ctx.respond("**TIP:** do `/unwhitelistrole` to unwhitelist a role.", embed=alreadywhitelisted)

        else:
            whitelistedroles.insert_one({"_id": customid})

            whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> I have whitelisted **{role.name}** users can now send links.")

            await ctx.respond("**TIP:** do `/unwhitelistrole` to unwhitelist a role.", embed=whitelisted)

    @whitelist.command()
    @has_permissions(administrator=True)
    async def link(self, ctx, link: str):
        """Whitelist a link so it can be sent."""
        link = link.lower()
        serverid = ctx.guild.id

        if extractor.has_urls(link):
            if whitelistedlinks.count_documents({"_id": f"{link}{serverid}"}):

                alreadywhitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> **{link}** seems to be already whitelisted.")

                await ctx.respond("**TIP:** do `/unwhitelistlink` to unwhitelist a link.", embed=alreadywhitelisted)

            else:
                whitelistedlinks.insert_one({"_id": f"{link}{serverid}"})

                whitelisted = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> I have whitelisted **{link}** that link can now be sent.")

                await ctx.respond("**TIP:** do `/unwhitelistlink` to unwhitelist a link.", embed=whitelisted)
        else:
            invalidlink = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Please enter a valid link.")

            await ctx.respond(embed=invalidlink)

def setup(bot):
    bot.add_cog(whitelistCommands(bot))