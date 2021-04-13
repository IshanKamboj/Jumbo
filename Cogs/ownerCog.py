import discord
from discord.ext import commands, tasks
import os
from .Listeners import AllListeners
import sys
import dbl
import requests
class OwnerCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.token = os.getenv('DBL_TOKEN')
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True,webhook_path='/dblwebhook', webhook_auth='Ishan@1608', webhook_port=5000)
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("Received an upvote:", "\n", data, sep="")
    
    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received a test upvote:", "\n", data, sep="")
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
    @commands.command(name="checkvote")
    @commands.is_owner()
    async def _checkvote(self,ctx,uid:int):
        url = f"https://top.gg/api//bots/805430097426513941/check?userId={uid}"
        resp = requests.get(url)
        print(resp)
def setup(bot):
    bot.add_cog(OwnerCommands(bot))