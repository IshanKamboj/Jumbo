import discord
from discord.ext import commands
import asyncio
from Database.db_files import firebase
from helpEmbeds import HelpEmbeds
from datetime import datetime
import math
default_prefix = "j!"

lvl_add = 1
difficulty = 300

def convert_to_radians(angle):
    return math.radians(angle)
calcOPT = {
    "m":"000000",
    "k":"000",
    "K":"000",
    "M":"000000",
    "^":"**",
    "e":"*10**",

    "tan45":str(math.tan(convert_to_radians(45))),
    "tan60":str(math.tan(convert_to_radians(60))),
    "tan30":str(math.tan(convert_to_radians(30))),
    "tan0":str(math.tan(convert_to_radians(0))),
    "tan90":str(math.tan(convert_to_radians(90))),

    "cot0":str(math.pow(math.tan(convert_to_radians(0)),-1)),
    "cot30":str(math.pow(math.tan(convert_to_radians(30)),-1)),
    "cot45":str(math.pow(math.tan(convert_to_radians(45)),-1)),
    "cot60":str(math.pow(math.tan(convert_to_radians(60)),-1)),
    "cot90":str(math.pow(math.tan(convert_to_radians(90)),-1)),

    "sin45":str(math.sin(convert_to_radians(45))),
    "sin60":str(math.sin(convert_to_radians(60))),
    "sin90":str(math.sin(convert_to_radians(90))),
    "sin0":str(math.sin(convert_to_radians(0))),
    "sin30":str(math.sin(convert_to_radians(30))),

    "cosec0":str(math.pow(math.sin(convert_to_radians(0)),-1)),
    "cosec30":str(math.pow(math.cos(convert_to_radians(30)),-1)),
    "cosec45":str(math.pow(math.cos(convert_to_radians(45)),-1)),
    "cosec60":str(math.pow(math.cos(convert_to_radians(60)),-1)),
    "cosec90":str(math.pow(math.cos(convert_to_radians(90)),-1)),

    "cos0":str(math.cos(convert_to_radians(0))),
    "cos30":str(math.cos(convert_to_radians(30))),
    "cos45":str(math.cos(convert_to_radians(45))),
    "cos60":str(math.cos(convert_to_radians(60))),
    "cos90":str(math.cos(convert_to_radians(90))),

    "sec0":str(math.pow(math.cos(convert_to_radians(0)),-1)),
    "sec30":str(math.pow(math.cos(convert_to_radians(30)),-1)),
    "sec45":str(math.pow(math.cos(convert_to_radians(45)),-1)),
    "sec60":str(math.pow(math.cos(convert_to_radians(60)),-1)),
    "sec90":str(math.pow(math.cos(convert_to_radians(90)),-1)),
}
number_list = ['1','2','3','4','5','6','7','8','9','0','tan','sec','sin','cosec','cot','cos']
class CommandDisabled(commands.CheckFailure):
    pass
class MissingRequiredServerRoles(commands.CheckFailure):
    pass
class AllListeners(commands.Cog):
    def __init__(self,bot,difficulty,lvl_add):
        self.bot = bot
        self.difficulty = difficulty
        self.lvl_add = lvl_add
    
    def check_enabled(ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            return isEnabled.val() is None
        else:
            raise CommandDisabled
            return isEnabled.val() is None
    
    def role_check(ctx):
        db = firebase.database()
        req_role = db.child("Settings").child(str(ctx.guild.id)).child(str(ctx.command)).get()
        user_role = list(map(int, [r.id for r in ctx.author.roles]))
        if req_role.val() is not None:
            for i in user_role:
                if i in req_role.val()["roles_id"]:
                    return True
                    break
            raise MissingRequiredServerRoles
            return False
        else:
            return True
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Everyone Fight"))
        print('Logged in as {0.user}'.format(self.bot))
        await self.bot.get_channel(826719835630338058).send('Logged in as {0.user}'.format(self.bot))
     
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        emb = discord.Embed(title='Jumbo joined a guild.',color=discord.Color.random(),thumbnail=f'{guild.icon_url}')
        emb.add_field(name='Guild Name',value=f'`{guild.name}`')
        emb.add_field(name='Guild ID',value=f'`{guild.id}`')
        emb.add_field(name='Guild owner',value=f'`{guild.owner}`')
        emb.add_field(name='No. of members',value=f'`{guild.member_count}`')
        emb.add_field(name='Joined on',value=f'`{datetime.utcnow()}`')
        emb.add_field(name='Guild created at',value=f'{guild.created_at}')
        await self.bot.get_channel(826719835630338058).send(embed=emb)
        db = firebase.database()
        db.child('Prefixes').child(str(guild.id)).set({'Prefix':default_prefix})
        em = discord.Embed(title="Hola Nabs, I am Jumbo",description="""
        **This is a fun bot and has a variety of different commands, you can set autoreacts, afk, can see weather forecast for your city, calculate, play music, send emojis and much more.**
        **This bot has basically a mixture of commands and it cannot be called a particular type of bot. It combines features from many bots and also many new and original features are being added.**
        Default Prefix : `j!` 
    
        Use `j!help` to get started.
    
        [** •Invite me**](https://discord.com/api/oauth2/authorize?client_id=805430097426513941&permissions=1008073792&scope=bot "Add the bot to your server")
        
        """,color=discord.Color.random()
        
        )

        for channel in guild.text_channels:
            if "general" in channel.name:
                await channel.send(embed=em)
                break
        
    def replace_all(self,text,dic):
        for i , j in dic.items():
            text = text.replace(i,j)
        return text   
    @commands.Cog.listener()
    async def on_message(self,message):
        if not message.guild:
            return
        else:
            db = firebase.database()
            try:
                prefix_data = db.child('Prefixes').child(str(message.guild.id)).get()
            except:
                pass
            seen_data = db.child("Last Seen").child(str(message.author.id)).get()
            if message.author != self.bot.user:
                if any(i for i in number_list if message.content.startswith(i)):

                    try:
                        msg = message.content
                        y = self.replace_all(msg, calcOPT)
                        
                        calc = eval(str(y))
                        await message.add_reaction("➕")
                        def _check(r, u):
                            return (
                                r.emoji == "➕"
                                and u == message.author
                                and r.message.id == message.id
                            )
                        try:
                            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
                        except asyncio.TimeoutError:
                            await message.clear_reactions()
                        else:
                            em = discord.Embed(description=f"**Calculated:** `{calc:,.0f}`\n**Raw Calculated :** `{calc:.1f}`",color=discord.Color.random())
                            await message.channel.send(embed=em)
                    except:
                        pass
                if message.mentions:
                    for i in message.mentions:
                        afk_data = db.child("AFK").child(str(message.guild.id)).child(str(i)).get()
                        try:
                            reason = afk_data.val()["reason"]
                            em = discord.Embed(title=f"User AFK",description=f"The Mentioned user is AFK....... **Reason: {reason}**",color=discord.Color.from_rgb(255,20,147))
                            await message.channel.send(message.author.mention,embed=em)
                        except:
                            pass
                try:
                    for i in message.mentions:
                        reaction_data =  db.child('Reactions').child(str(message.guild.id)).child(str(i)).get()
                        for j in reaction_data.val()["Reaction"]:
                            await message.add_reaction(j)
                except Exception as e:
                    pass
                    #print(str(e))
                
                    
                if message.content.startswith(prefix_data.val()['Prefix']):
                    return
                # elif message.content.startswith(self.bot.user.mention):
                #     em = (discord.Embed(description=f"Yo! My prefix here is `{prefix_data.val()['Prefix']}`. You can use `{prefix_data.val()['Prefix']}help` for more information",color=discord.Color.random()))
                #     await message.channel.send(embed = em)
                else:
                    isEnabled = db.child('Disabled').child(str(message.guild.id)).child("level").get()
                    if isEnabled.val() is None:
                        if not message.author.bot:
                            
                            
                            data = db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).get()
                            last_exp = db.child("Last Seen").child(str(message.author.id)).get()   
                            if data.val() is None:
                                newUser = {"userName":str(message.author),"lvl":1,"exp":1}
                                db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).set(newUser)
                            elif data.val() is not None:
                                if last_exp.val() is None:
                                    exp = data.val()['exp']
                                    lvl = data.val()['lvl']
                                    exp += self.lvl_add
                                    
                                    a = self.difficulty+(lvl-1)*self.difficulty
                                    mention = message.author.mention
                                    if exp >= a:
                                        lvl += 1
                                        lvl_embed = (discord.Embed(title="**Level Up**",
                                        description= f"Congratulations {mention}. You just reached level {lvl}",
                                        color = discord.Color.from_rgb(0,255,185)
                                        )
                                        .set_thumbnail(url=f"{message.author.avatar_url}")
                                        )
                                        await message.channel.send(mention,embed=lvl_embed)
                                    if seen_data.val() is None:
                                        db.child("Last Seen").child(str(message.author.id)).set({"Time":str(datetime.utcnow())})
                                    elif seen_data.val() is not None:
                                        db.child("Last Seen").child(str(message.author.id)).update({"Time":str(datetime.utcnow())})
                                    db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).update({"userName":str(message.author),"exp":exp,"lvl":lvl})
                                elif last_exp.val() is not None:
                                    time = last_exp.val()["Time"]
                                    converted_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
                                    if (datetime.utcnow() - converted_time).seconds > 4:
                                        exp = data.val()['exp']
                                        lvl = data.val()['lvl']
                                        exp += self.lvl_add
                                        
                                        a = self.difficulty+(lvl-1)*self.difficulty
                                        mention = message.author.mention
                                        if exp >= a:
                                            lvl += 1
                                            lvl_embed = (discord.Embed(title="**Level Up**",
                                            description= f"Congratulations {mention}. You just reached level {lvl}",
                                            color = discord.Color.from_rgb(0,255,185)
                                            )
                                            .set_thumbnail(url=f"{message.author.avatar_url}")
                                            )
                                            await message.channel.send(mention,embed=lvl_embed)
                                        if seen_data.val() is None:
                                            db.child("Last Seen").child(str(message.author.id)).set({"Time":str(datetime.utcnow())})
                                        elif seen_data.val() is not None:
                                            db.child("Last Seen").child(str(message.author.id)).update({"Time":str(datetime.utcnow())})
                                        db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).update({"userName":str(message.author),"exp":exp,"lvl":lvl})
                            #await asyncio.sleep(2)
                        else:
                            pass
            #await self.bot.process_commands(message)
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if hasattr(ctx.command, 'on_error'):
            return
        db = firebase.database()
        prefix_data = db.child('Prefixes').child(str(ctx.guild.id)).get()
        pre = prefix_data.val()["Prefix"]
        if isinstance(error,commands.CommandNotFound):
            em = discord.Embed(title="Command not found",description=f"{error}..... use `{pre}help` for info on commands.")
            await ctx.send(embed=em)
        elif isinstance(error, CommandDisabled):
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
        elif isinstance(error, MissingRequiredServerRoles):
            #print('yes')
            em = discord.Embed(title="Missing Role Requirement",description=f"You are missing required roles for using this command. Use `*settings show` to see role requirements for this command.",color=discord.Color.random())
            await ctx.send(embed=em)
        elif isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            if time >= 3600:
                finalTime= round(time/3600)
                em = discord.Embed(title="Take a hold of yourself",description=f"This command is on cooldown. You need to wait **{finalTime} hours** before using it again.",color=discord.Color.random())
            elif time < 3600 and time > 60:
                finalTime = round(time/60)
                em = discord.Embed(title="Take a hold of yourself",description=f"This command is on cooldown. You need to wait **{finalTime} minutes** before using it again.",color=discord.Color.random())
            elif time < 60:
                em = discord.Embed(title="Take a hold of yourself",description=f"This command is on cooldown. You need to wait **{time} seconds** before using it again.",color=discord.Color.random())
            #print(finalTime)
            await ctx.send(embed=em)
        elif isinstance(error,commands.BotMissingPermissions):
            try:
                em = discord.Embed(title="Bot Missing Perms",description="Bot might be missing the perms required to use this command. Please check and try again.",color=discord.Color.red())
                msg = await ctx.send(embed=em)
                await msg.add_reaction('❌')
            except:
                pass
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                em = discord.Embed(title="Command Missing required arguments",description="The command is missing required arguments. See `*help <command_name>` for more details",color=discord.Color.red())
                msg = await ctx.send(embed=em)
                await msg.add_reaction('❌')
            except:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                em = discord.Embed(title="Missing Permission",description=f"{str(error)}",color=discord.Color.red())
                msg = await ctx.send(embed=em)
                await msg.add_reaction('❌')
            except:
                pass
        else:
            try:
                await ctx.send(str(error))
            except:
                pass
def setup(bot):
    bot.add_cog(AllListeners(bot=bot,lvl_add=lvl_add,difficulty=difficulty))