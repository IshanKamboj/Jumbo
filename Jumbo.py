import discord
from discord.ext import commands
import os
from discord import Intents
from Database.db_files import firebase
#----------------------- Prefix getting and bot setup--------------------------------
def get_prefix(client,message):
    try:
        db = firebase.database()
        data = db.child('Prefixes').child(str(message.guild.id)).get()
        x = data.val()['Prefix']
        return commands.when_mentioned_or(x,"j!")(client,message)
    except:
        return commands.when_mentioned_or("j!")(client,message)

intent = Intents().all()   

bot = commands.AutoShardedBot(command_prefix=get_prefix,intents=intent,case_insensitive=True,strip_after_prefix=True)
bot.remove_command("help")

bot.version = "0.0.10"

#####################################    LOADING COGS    #########################################################
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')
    else:
        print(f"Could not load: Cogs.{filename[:-3]}")


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)