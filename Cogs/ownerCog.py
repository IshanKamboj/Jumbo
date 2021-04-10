import discord
from discord.ext import commands
import os
from .Listeners import AllListeners
import sys
import dbl
class OwnerCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.token = os.getenv('DBL_TOKEN')
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def _shutdown(self,ctx):
        try:
            await ctx.send("Shutting down the bot..........")
            await self.bot.logout()
        except Exception as e:
            print(str(e))

    def restart_program(self):
        python = sys.executable
        os.execl(python,python,* sys.argv)
    @commands.command(name="restart")
    @commands.is_owner()
    async def _restart(self,ctx):
        try:
            await ctx.send("Restarting the bot....")
            self.restart_program()
            await ctx.send("Bot started....")
        except Exception as e:
            print(str(e))

def setup(bot):
    bot.add_cog(OwnerCommands(bot))