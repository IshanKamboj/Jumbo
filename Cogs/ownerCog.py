import discord
from discord.ext import commands
import os
import sys
import dbl
import socket
import socket
from Database.db_files import firebase
class OwnerCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.token = os.getenv('DBL_TOKEN')
        self.dblpy = dbl.DBLClient(self.bot, self.token,autopost=True)
    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        #print(socket.gethostbyname(socket.gethostname()))
        """An event that is called whenever someone votes for the bot on top.gg."""
        print(f"Received an upvote:{data}")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        #print(socket.gethostbyname(socket.gethostname()))
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
        except Exception as e:
            print(str(e))
    @commands.command(name="ip")
    @commands.is_owner()
    async def _ip(self,ctx):
        print(socket.gethostbyname(socket.gethostname()))
    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self,ctx,*,code):
        try:
            exe = eval(code)
            await ctx.send(f"```{exe}```")
        except Exception as e:
            await ctx.send(str(e))
    @commands.command(name="permsimp",aliases=["permanentsimp"])
    @commands.is_owner()
    async def _permsimp(self,ctx,user:discord.User=None):
        if user == None:
            user = ctx.author
        db = firebase.database()
        x = db.child('PermanentSimp').get()
        if x.val() is None:
            db.child('PermanentSimp').set({'Ids':[user.id]})
            await ctx.send(f"Added {user.mention} as a permanent simp.")
        else:
            y = x.val()
            y = y['Ids']
            #print()
            if user.id not in y:
                y.append(user.id)
            db.child('PermanentSimp').update({'Ids':y})
            await ctx.send(f"Added {user.mention} as a permanent simp.")
def setup(bot):
    bot.add_cog(OwnerCommands(bot))