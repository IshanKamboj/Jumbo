import discord
from discord.ext import commands
from pathlib import Path
import os
from Database.db_files import firebase
class Jumbo(commands.Bot):
    def __init__(self):
        self._cogs=[p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=self.prefix, case_insensitive=True, intents = intents)
    def setup(self):
        print("Running Setup.....")
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"Loaded {cog} cog.")
        print("Setup Complete.")
    
    def run(self,VERSION):
        self.setup()

        TOKEN = os.getenv('TOKEN')
        
        self.version = VERSION
        print("Running the bot")
        super().run(TOKEN,reconnect=True)
        
    async def on_ready(self):
        print(f"Bot ready.")
    
    async def prefix(self,client,message):
        try:
            db = firebase.database()
            data = db.child('Prefixes').child(str(message.guild.id)).get()
            x = data.val()['Prefix']
            return commands.when_mentioned_or(x,"j!")(client,message)
        except:
            return commands.when_mentioned_or("j!")(client,message)