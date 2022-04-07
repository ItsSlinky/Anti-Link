import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.commands import Option, SlashCommandGroup
from pymongo import MongoClient, results

cluster = MongoClient("mongodblink")

db1 = cluster["Anti-Link"]
cases = db1["cases"]
serveractions = db1["server-actions"]
messageactions = db1["message-actions"]
adminbypassdb = db1["admin-bypass"]
antilinkstatus = db1["antilinkstatus"]
serverlogs = db1["server-logs"]
whitelistedchannels = db1["whitelisted-channels"]
whitelistedmembers = db1["whitelisted-members"]

def fetchantilinkstatus(guildid):
    if antilinkstatus.count_documents({"_id": guildid}):
        return "enabled"
    else:
        return "disabled"

def fetchcases(guildid):
    if cases.count_documents({"_id": guildid}):
        results = cases.find({"_id": guildid})

        for result in results:
            casenumber = (result["casenumber"])

        return casenumber
    else:
        return "0"

def fetchadminstatus(guildid):
    if adminbypassdb.count_documents({"_id": guildid}):
        return "**ARE** automatically whitelisted"
    else:
        return "are **NOT** automatically whitelisted"

class configCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = SlashCommandGroup("config", "Commnads related to configuring.")

    @config.command()
    async def view(self, ctx):
        """View the servers config."""
        memberid = ctx.author.id
        guildid = ctx.guild.id
        channelid = ctx.channel.id
        customid = (memberid + guildid)

        antilinkstatus = fetchantilinkstatus(guildid)
        totalcases = fetchcases(guildid)
        adminwhitelist = fetchadminstatus(guildid)

        config = discord.Embed(title=f"Anti-Link configuration", description=f"This is the Anti-Link config, here you can view lots of useful things.", colour=discord.Colour(0xFF0000))

        config.add_field(name="➜ Anti-Link status", value=f"Anti-Link is currently **{antilinkstatus}**.", inline=False)
        config.add_field(name="➜ Anti-Link cases", value=f"There have been **{totalcases}** case(s) were links had been sent.", inline=False)
        config.add_field(name="➜ Admins are whitelisted", value=f"Members with administrators {adminwhitelist}.", inline=False)
        config.add_field(name="➜ Change configuration", value="To change the configuration of the server do /help.", inline=False)

        await ctx.respond(embed=config)

    @commands.slash_command()
    @has_permissions(administrator=True)
    async def antilink(self, ctx, action: Option(str, "Please select what you want to do.", choices=["Enable", "Disable"])):
        """Enable or disable anti-link."""
        serverid = ctx.guild.id

        if action == "Enable":
            if antilinkstatus.count_documents({"_id": serverid}):
                alreadyenabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Anti-Link is already enabled.")

                await ctx.respond("**TIP:** do `/antilink disable` to disable anti-link.", embed=alreadyenabled)
            else:
                antilinkstatus.insert_one({"_id": serverid})
                enabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Anti-Link is now enabled.")

                await ctx.respond("**TIP:** do `/antilink disable` to disable anti-link.", embed=enabled)

        elif action == "Disable":
            if antilinkstatus.count_documents({"_id": serverid}):
                antilinkstatus.delete_one({"_id": serverid})
                disabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Anti-Link is now disabled.")

                await ctx.respond("**TIP:** do `/antilink enable` to enable anti-link.", embed=disabled)
            else:
                alreadydisabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Anti-Link is already disabled.")

                await ctx.respond("**TIP:** do `/antilink enable` to enable anti-link.", embed=alreadydisabled)

    @config.command()
    @has_permissions(administrator=True)
    async def punishment(self, ctx, action: Option(str, "Please select what you want to do.", choices=["Delete Message", "Ban Member", "Kick Member", "Delete Message & Kick Member", "Delete Message & Ban Member"])):
        """Select the action you want to happen when someone sends an unwanted link."""
        serverid = ctx.guild.id

        if serveractions.count_documents({"_id": serverid}):
            serveractions.delete_one({"_id": serverid})
            serveractions.insert_one({"_id": serverid, "action": action})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> An action for when links have been sent has been set.")

            await ctx.respond(embed=actionset)
        else:
            serveractions.insert_one({"_id": serverid, "action": action})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> An action for when links have been sent has been set.")

            await ctx.respond(embed=actionset)

    @config.command()
    @has_permissions(administrator=True)
    async def adminbypass(self, ctx: discord.ApplicationContext, action: Option(str, "Please select what you want to do.", choices=["Enable", "Disable"])):
        """Make it so admins can bypass Anti-Link."""
        serverid = ctx.guild.id

        if action == "Enable":
            if adminbypassdb.count_documents({"_id": serverid}):
                alreadyenabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Admin bypass is already enabled.")

                await ctx.respond(embed=alreadyenabled)
            else:
                adminbypassdb.insert_one({"_id": serverid})
                enabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Admin bypass is now enabled.")

                await ctx.respond(embed=enabled)

        elif action == "Disable":
            if adminbypassdb.count_documents({"_id": serverid}):
                adminbypassdb.delete_one({"_id": serverid})

                disabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Admin bypass is disabled.")

                await ctx.respond(embed=disabled)
            else:
                notenabled = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Admin bypass is not enabled.")

                await ctx.respond(embed=notenabled)

    @config.command()
    @has_permissions(administrator=True)
    async def action(self, ctx, action: Option(str, "Please select what you want to do.", choices=["Send Message In Chat", "Send Message In Users DMs"])):
        """Select the action you want to happen when someone sends an unwanted link."""
        serverid = ctx.guild.id

        if messageactions.count_documents({"_id": serverid}):
            messageactions.delete_one({"_id": serverid})
            messageactions.insert_one({"_id": serverid, "action": action})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> A message action for when links have been sent has been set.")

            await ctx.respond(embed=actionset)
        else:
            messageactions.insert_one({"_id": serverid, "action": action})
            actionset = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> A message action for when links have been sent has been set.")

            await ctx.respond(embed=actionset)

def setup(bot):
    bot.add_cog(configCommands(bot))