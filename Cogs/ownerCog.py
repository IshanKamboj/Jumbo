import discord
from discord.ext import commands, tasks
import os
from .Listeners import AllListeners
import sys
import dbl
import requests
import socket
import socket
class OwnerCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.token = os.getenv('DBL_TOKEN')
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True, webhook_port=5000,webhook_path="/jumbo7")
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(socket.gethostbyname(socket.gethostname()))
        """An event that is called whenever someone votes for the bot on top.gg."""
        print(f"Received an upvote:{data}")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(socket.gethostbyname(socket.gethostname()))
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print(f"Received a test upvote:{data}")
    
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
    @commands.command(name="ip")
    @commands.is_owner()
    async def _ip(self,ctx):
        print(socket.gethostbyname(socket.gethostname()))
def setup(bot):
    bot.add_cog(OwnerCommands(bot))