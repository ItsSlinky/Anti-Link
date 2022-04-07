import discord
from discord.ext import commands
from pymongo import MongoClient, results
from urlextract import URLExtract

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
whitelistedmembers = db1["whitelisted-members"]

extractor = URLExtract()

def getmessageaction(serverid):
    try:
        messageaction = messageactions.find_one({"_id": serverid})
        return messageaction["action"]
    except:
        return None

class messageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        memberid = message.author.id
        guildid = message.guild.id
        channelid = message.channel.id
        channelcustomid = (channelid + guildid)
        membercustomid = (memberid + guildid)
        
        if extractor.has_urls(message.content):
            for url in extractor.gen_urls(message.content):
                linkinmessage = url
                link = url.lower()
                if serverlogs.count_documents({"_id": guildid}):
                    results = serverlogs.find({"_id": guildid})

                    for result in results:
                        channel = (result["channel"])
                        logtype = (result["logtype"])
                    
                    if logtype == "Minimalism":
                        realchannel = self.bot.get_channel(channel)
                        try:
                            try:
                                logembed = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {message.author.mention} sent a link in {message.channel.mention}.")
                                logembed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar)
                                await realchannel.send(embed=logembed)
                            except:
                                logembed = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> {message.author.mention} sent a link in {message.channel.mention}.")
                                logembed.set_author(name=f"{message.author.name}#{message.author.discriminator}")
                                await realchannel.send(embed=logembed)                                
                        except:
                            print("something went wrong.")
                    elif logtype == "Maximalism":
                        realchannel = self.bot.get_channel(channel)
                        try:
                            try:
                                logembed = discord.Embed(colour=discord.Colour(0xFF0000), description=f"Offender: {message.author.name}#{message.author.discriminator}, {message.author.id}\nChannel: {message.channel}, {message.channel.id}\nFlagged link: {linkinmessage}")
                                logembed.add_field(name="Original message:", value=f"```{message.content}```", inline=False)
                                logembed.set_author(name=f"Link Found.", icon_url=message.author.avatar)

                                await realchannel.send(embed=logembed)
                            except:
                                logembed = discord.Embed(colour=discord.Colour(0xFF0000), description=f"Offender: {message.author.name}#{message.author.discriminator}, {message.author.id}\nChannel: {message.channel}, {message.channel.id}\nFlagged link: {linkinmessage}")
                                logembed.add_field(name="Original message:", value=f"```{message.content}```", inline=False)
                                logembed.set_author(name=f"Link Found.")

                                await realchannel.send(embed=logembed)
                        except:
                            print("something went wrong.")
                if antilinkstatus.count_documents({"_id": guildid}):
                    if whitelistedlinks.count_documents({"_id": f"{link}{guildid}"}):
                        print("Link is whitelisted")
                    else:
                        if adminbypassdb.count_documents({"_id": guildid}):
                            if message.author.guild_permissions.administrator:
                                print("Whitelisted")
                            else:
                                if whitelistedchannels.count_documents({"_id": channelcustomid}): 
                                    print("Whitelisted.")
                                else:
                                    print("hey")
                                    if whitelistedmembers.count_documents({"_id": membercustomid}): 
                                        print("Whitelisted.")
                                    else:
                                        if cases.count_documents({"_id": guildid}):
                                            results = cases.find({"_id": guildid})

                                            for result in results:
                                                casenumber = (result["casenumber"])

                                            newcasenum = casenumber+1
                                            cases.delete_one({"_id": guildid})
                                            cases.insert_one({"_id": guildid, "casenumber": newcasenum})

                                            antilink = discord.Embed(title=f"Link Found | Case #{casenumber}", colour=discord.Colour(0xFF0000), description=f"Offender: {message.author.name}#{message.author.discriminator}, {message.author.id}\nChannel: {message.channel}, {message.channel.id}\nFlagged link: {linkinmessage}")
                                            antilink.add_field(name="Original message:", value=f"```{message.content}``` ", inline=False)

                                            await message.channel.send(embed=antilink)

                                            if serveractions.count_documents({"_id": guildid}):
                                                results = serveractions.find({"_id": guildid})

                                                for result in results:
                                                    useraction = (result["action"])

                                                if useraction == "Delete Message":
                                                    await message.delete()
                                                elif useraction == "Ban Member":
                                                    await message.author.ban(reason="User sent a link, to change what happens when a user sends a link do /action")
                                                elif useraction == "Kick Member":
                                                    await message.author.kick(reason="User sent a link, to change what happens when a user sends a link do /action")
                                                elif useraction == "Delete Message & Kick Member":
                                                    await message.delete()
                                                    await message.author.kick(reason="User sent a link, to change what happens when a user sends a link do /action")
                                                elif useraction == "Delete Message & Ban Member":
                                                    await message.delete()
                                                    await message.author.ban(reason="User sent a link, to change what happens when a user sends a link do /action")
                                            else:
                                                await message.delete()

                                        else:
                                            cases.insert_one({"_id": guildid, "casenumber": 1})

                                            antilink = discord.Embed(title=f"Link Found | Case #{casenumber}", colour=discord.Colour(0xFF0000), description=f"Offender: {message.author.name}#{message.author.discriminator}, {message.author.id}\nChannel: {message.channel}, {message.channel.id}\nFlagged link: {linkinmessage}")
                                            antilink.add_field(name="Original message:", value=f"```{message.content}``` ", inline=False)

                                            await message.channel.send(embed=antilink)
                                            await message.delete()
                        else:
                            if whitelistedchannels.count_documents({"_id": channelcustomid}):
                                print("Whitelisted.")
                            else:
                                if whitelistedmembers.count_documents({"_id": membercustomid}): 
                                    print("Whitelisted.")
                                else:
                                    if cases.count_documents({"_id": guildid}):
                                        results = cases.find({"_id": guildid})

                                        for result in results:
                                            casenumber = (result["casenumber"])

                                        newcasenum = casenumber+1
                                        cases.delete_one({"_id": guildid})
                                        cases.insert_one({"_id": guildid, "casenumber": newcasenum})


                                        antilink = discord.Embed(title=f"Link Found | Case #{casenumber}", colour=discord.Colour(0xFF0000), description=f"Offender: {message.author.name}#{message.author.discriminator}, {message.author.id}\nChannel: {message.channel}, {message.channel.id}\nFlagged link: {linkinmessage}")
                                        antilink.add_field(name="Original message:", value=f"```{message.content}``` ", inline=False)

                                        await message.channel.send(embed=antilink)
                                        await message.delete()

                                    else:
                                        cases.insert_one({"_id": guildid, "casenumber": 1})

                                        antilink = discord.Embed(title=f"Link Found | Case #1", colour=discord.Colour(0xFF0000), description=f"Offender: {message.author.name}#{message.author.discriminator}, {message.author.id}\nChannel: {message.channel}, {message.channel.id}\nFlagged link: {linkinmessage}")
                                        antilink.add_field(name="Original message:", value=f"```{message.content}``` ", inline=False)

                                        await message.channel.send(embed=antilink)
                                        await message.delete()
def setup(bot):
    bot.add_cog(messageEvent(bot)) 