import discord
import locale
from discord.ext import commands
from discord.commands import Option
from discord.ext.commands import has_permissions, MissingPermissions
from pymongo import MongoClient, results

cluster = MongoClient("mongodblink")

db1 = cluster["Anti-Link"]
cases = db1["cases"]
serveractions = db1["server-actions"]
messageactions = db1["message-actions"]
usedlinks = db1["used-links"]
adminbypassdb = db1["admin-bypass"]
antilinkstatus = db1["antilinkstatus"]
whitelistedchannels = db1["whitelisted-channels"]
whitelistedmembers = db1["whitelisted-members"]

locale.setlocale(locale.LC_ALL, 'en_US')

def fetchcases(guildid):
    if cases.count_documents({"_id": guildid}):
        results = cases.find({"_id": guildid})

        for result in results:
            casenumber = (result["casenumber"])

        return casenumber
    else:
        return "0"

def fetchusedlinks(guildid):
    if usedlinks.count_documents({"_id": guildid}):
        results = usedlinks.find({"_id": guildid})

        for result in results:
            usedlink = (result["link"])
            uses = (result["uses"])

        return f"is **{usedlink}** and its been used **{uses}** times"
    else:
        return "can't be fetched, no links have been sent"

class infoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def help(self, ctx, option: Option(str, "Please select the option you want.", choices=["All", "Whitelist", "Unwhitelist", "Logging"])):
        """Receive a list of commands."""
        if option == "All":
            help = discord.Embed(title=f"How to use Anti-Link", colour=discord.Colour(0xFF0000), description="Anti-Link allows discord server owners to delete links seamlessly with Anti-Link so you can get on with the things you need to do.")

            help.add_field(name="➜ Getting started", value="You can get started using Anti-Link by doing **/antilink enable**, this enables the anti link and deletes messages sent by all members except users with administrator.", inline=False)
            help.add_field(name="➜ Whitelisting", value="Members can be whitelisted using the **/whitelistmember**, channels can be whitelisted using **/whitelistchannel**.", inline=False)
            help.add_field(name="➜ Unwhitelisting", value="Members can be unwhitelisted using the **/unwhitelistmember**, channels can be unwhitelisted using **/unwhitelistchannel**.", inline=False)
            help.add_field(name="➜ Configuration", value="The servers config can be viewed and edited using the **/config** command.", inline=False)

            await ctx.respond(embed=help)
        elif option == "Whitelist":
            whitelist = discord.Embed(title=f"How to whitelist", colour=discord.Colour(0xFF0000), description="Whitelisting allows certian people to send links.")

            whitelist.add_field(name="➜ Whitelist members", value="You can whitelist a member using the **/whitelist member** command.", inline=False)
            whitelist.add_field(name="➜ Whitelist channels", value="You can whitelist a channel using the **/whitelist channel** command.", inline=False)
            whitelist.add_field(name="➜ Whitelist roles", value="You can whitelist a role using the **/whitelist role** command.", inline=False)
            whitelist.add_field(name="➜ Configuration", value="The servers config can be viewed and edited using the **/config** command.", inline=False)

            await ctx.respond(embed=whitelist)
        elif option == "Unwhitelist":
            unwhitelist = discord.Embed(title=f"How to unwhitelist", colour=discord.Colour(0xFF0000), description="Unwhitelisting stops people from sending links.")

            unwhitelist.add_field(name="➜ Unwhitelist members", value="You can unwhitelist a member using the **/unwhitelist member** command.", inline=False)
            unwhitelist.add_field(name="➜ Unwhitelist channels", value="You can unwhitelist a channel using the **/unwhitelist channel** command.", inline=False)
            unwhitelist.add_field(name="➜ Unwhitelist roles", value="You can unwhitelist a role using the **/unwhitelist role** command.", inline=False)
            unwhitelist.add_field(name="➜ Configuration", value="The servers config can be viewed and edited using the **/config** command.", inline=False)

            await ctx.respond(embed=whitelist)
        elif option == "Logs":
            logs = discord.Embed(title=f"How to setup logging", colour=discord.Colour(0xFF0000), description="Logging allows server owners and admins to track links been sent.")

            logs.add_field(name="➜ Set logs", value="You can set the logs channel and log type by doing **/logs set**.", inline=False)
            logs.add_field(name="➜ Delete logs", value="You can delete the logs config using the **/logs remove** command.", inline=False)
            logs.add_field(name="➜ Configuration", value="The servers config can be viewed and edited using the **/config** command.", inline=False)

            await ctx.respond(embed=logs)

    @commands.slash_command()
    async def invite(self, ctx):
        """Invite the bot to your server."""
        invite = discord.Embed(title="Invite Anti-Link!", colour=discord.Colour(0xFF0000), description=f"> Invite Anti-Link along with the other **{len(self.bot.guilds)}** servers.")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Invite Anti-Link', url='https://discord.com/api/oauth2/authorize?client_id=948988752309665792&permissions=8&scope=bot%20applications.commands', style=discord.ButtonStyle.url))

        await ctx.respond(embed=invite, view=view)

    @commands.slash_command()
    async def botinfo(self, ctx):
        """View some basic bot information."""
        shardcount = self.bot.shard_count
        shardnumber = ctx.guild.shard_id + 1
        shardping = self.bot.latency

        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count 
        
        commands = 0
        for command in self.bot.walk_application_commands():
            commands += 1

        channels = 0
        for channel in self.bot.get_all_channels():
            channels += 1

        memberswithcommas = locale.format("%d", members, grouping=True)
        channelswithcommas = locale.format("%d", channels, grouping=True)

        botinfo = discord.Embed(title="Anti-Link", description=f"The all in one anti link bot to stop the spread of links\nWant to invite the bot? click [here](https://discord.com/api/oauth2/authorize?client_id=948988752309665792&permissions=8&scope=bot%20applications.commands)",colour=discord.Colour(0xFF0000))
        botinfo.add_field(name="Statistics", value=f"Guilds: {len(self.bot.guilds)}\nUsers: {memberswithcommas}\nChannels: {channelswithcommas}\nCommands: {commands}\nShard: {shardnumber}/{shardcount}\nLibrary: discord.py\nDeveloper: Slinky#0001 (683243013904007168)", inline=False)
        botinfo.set_thumbnail(url="https://cdn.discordapp.com/avatars/948988752309665792/0de8ec95989bb8310e124689807c82fa.png?size=80")

        await ctx.respond(embed=botinfo)

def setup(bot):
    bot.add_cog(infoCommands(bot))