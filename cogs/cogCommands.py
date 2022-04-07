import discord
from discord.ext import commands
from discord.commands import Option

developers = [683243013904007168, 923656083355103312]

class cogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def reload(self, ctx, cog: str):
        """Reload a cog from the cogs folder."""
        if ctx.author.id in developers:
            try:
                self.bot.reload_extension(cog)
                reloaded = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Reloaded {cog} successfully.")

                await ctx.respond(embed=reloaded)
            except:
                failedtoreload = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Failed to reload {cog}, are you sure thats the name of the cog?")

                await ctx.respond(embed=failedtoreload)
        else:
            notdeveloper = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Only developers can run this command.")

            await ctx.respond(embed=notdeveloper)


    @commands.slash_command()
    async def unload(self, ctx, cog: str):
        """Unload a cog from the cogs folder."""
        if ctx.author.id in developers:
            try:
                self.bot.unload_extension(cog)
                unloaded = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Unloaded {cog} successfully.")

                await ctx.respond(embed=unloaded)
            except:
                failedtounload = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Failed to unload {cog}, are you sure thats the name of the cog?")

                await ctx.respond(embed=failedtounload)
        else:
            notdeveloper = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Only developers can run this command.")

            await ctx.respond(embed=notdeveloper)

    @commands.slash_command()
    async def load(self, ctx, cog: str):
        """Load a cog from the cogs folder."""
        if ctx.author.id in developers:
            try:
                self.bot.load_extension(cog)
                loaded = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Loaded {cog} successfully.")

                await ctx.respond(embed=loaded)
            except:
                failedtoload = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Failed to load {cog}, are you sure thats the name of the cog?")

                await ctx.respond(embed=failedtoload)
        else:
            notdeveloper = discord.Embed(colour=discord.Colour(0xFF0000), description=f"> Only developers can run this command.")

            await ctx.respond(embed=notdeveloper)

def setup(bot):
    bot.add_cog(cogCommands(bot))