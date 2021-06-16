from random import random, choice
import discord
from discord.ext import commands, tasks
import asyncio

from oauth2client.client import Error
from Database.db_files import firebase
from datetime import datetime
import math
import mpmath
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

    "cot30":str(mpmath.cot(30)),
    "cot45":str(mpmath.cot(45)),
    "cot60":str(mpmath.cot(60)),
    "cot90":str(mpmath.cot(90)),

    "sin45":str(math.sin(convert_to_radians(45))),
    "sin60":str(math.sin(convert_to_radians(60))),
    "sin90":str(math.sin(convert_to_radians(90))),
    "sin0":str(math.sin(convert_to_radians(0))),
    "sin30":str(math.sin(convert_to_radians(30))),

    "cosec30":str(mpmath.csc(30)),
    "cosec45":str(mpmath.csc(45)),
    "cosec60":str(mpmath.csc(60)),
    "cosec90":str(mpmath.csc(90)),

    "cos0":str(math.cos(convert_to_radians(0))),
    "cos30":str(math.cos(convert_to_radians(30))),
    "cos45":str(math.cos(convert_to_radians(45))),
    "cos60":str(math.cos(convert_to_radians(60))),
    "cos90":str(math.cos(convert_to_radians(90))),

    "sec0":str(mpmath.sec(0)),
    "sec30":str(mpmath.sec(30)),
    "sec45":str(mpmath.sec(45)),
    "sec60":str(mpmath.sec(60)),
}
number_list = ['1','2','3','4','5','6','7','8','9','0','tan','sec','sin','cosec','cot','cos']
sign_list = ['+','-','e','^','/','*']
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
                if i in req_role.val()["roles_id"] or ctx.author.guild_permissions.administrator:
                    return True
                    break
            raise MissingRequiredServerRoles
            return False
        else:
            return True
    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as {0.user}'.format(self.bot))
        await self.bot.get_channel(826719835630338058).send('Logged in as {0.user}'.format(self.bot))

        l = ["New Cmd: Try j!settings", "New Cmd: Try j!trivia","New Cmd: Try j!animetrivia","Checkout Cmds: Use j!help",f"Version: {self.bot.version}"]
        while True:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"j!help | {choice(l)}"))
            await asyncio.sleep(120)

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
        Default Prefix : `j!`
        
        **This is a fun bot and has a variety of different commands, you can set autoreacts, afk, can see weather forecast for your city, calculate, play music, send emojis and much more.**
        **This bot has basically a mixture of commands and it cannot be called a particular type of bot. It combines features from many bots and also many new and original features are being added.**
    
        Use `j!help` to get started.
    
        **Quick Links:**    
        [** •Invite me**](https://discord.com/api/oauth2/authorize?client_id=805430097426513941&permissions=1008073792&scope=bot "Add the bot to your server")[** •Vote for me**](https://top.gg/bot/805430097426513941/vote "Vote for the bot")[** •Support Server**](https://discord.gg/P3BmUsgv5y "Join the support server")
        
        """,color=discord.Color.random()
        
        )

        for channel in guild.text_channels:
            if "general" in channel.name:
                await channel.send(embed=em)
                break
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        db = firebase.database()
        db.child("Levels").child(str(guild.id)).remove()
        db.child("AFK").child(str(guild.id)).remove()
        db.child("Announcement").child(str(guild.id)).remove()
        db.child("Disabled").child(str(guild.id)).remove()
        db.child("Multi").child(str(guild.id)).remove()
        db.child("Reactions").child(str(guild.id)).remove()
        db.child("Settings").child(str(guild.id)).remove()
        emb = discord.Embed(title='Jumbo left a guild.',color=discord.Color.random(),thumbnail=guild.icon_url)
        emb.add_field(name='Guild Name',value=f'`{guild.name}`')
        emb.add_field(name='Guild ID',value=f'`{guild.id}`')
        emb.add_field(name='Guild owner',value=f'`{guild.owner}`')
        emb.add_field(name='No. of members',value=f'`{guild.member_count}`')
        emb.add_field(name='Joined on',value=f'`{datetime.utcnow()}`')
        emb.add_field(name='Guild created at',value=f'{guild.created_at}')
        await self.bot.get_channel(826719835630338058).send(embed=emb)
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
            if message.raw_mentions and not message.author.bot:
                for i in message.raw_mentions:
                    afk_data = db.child("AFK").child(str(message.guild.id)).child(str(i)).get()
                    try:
                        reason = afk_data.val()["reason"]
                        em = discord.Embed(title=f"User AFK",description=f"The Mentioned user is AFK....... **Reason: {reason}**",color=discord.Color.from_rgb(255,20,147))
                        await message.channel.send(message.author.mention,embed=em)
                    except:
                        pass
            try:
                if not message.author.bot:
                    for i in message.raw_mentions:
                        reaction_data =  db.child('Reactions').child(str(message.guild.id)).child(str(i)).get()
                        for j in reaction_data.val()["Reaction"]:
                            await message.add_reaction(j)
            except Exception as e:
                pass
            if message.content.startswith(prefix_data.val()['Prefix']):
                return
            else:
                await self.check_mentions_while_afk(message)
                await self.calculate(message)
                await self.rem_afk(message)
                await self.level_up_func(message,seen_data)
                
    async def calculate(self,message):
        if any(i for i in number_list if message.content.startswith(i)) and any(i for i in sign_list if i in str(message.content)):
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
                    em = discord.Embed(description=f"**Calculated:** `{calc:,.0f}`\n**Raw Calculated :** `{calc:.3f}`",color=discord.Color.random())
                    await message.channel.send(embed=em)
            except:
                pass
    async def check_mentions_while_afk(self,message):
        db = firebase.database()
        if message.raw_mentions and not message.author.bot:
            for i in message.raw_mentions:
                afk_data = db.child("AFK").child(str(message.guild.id)).child(str(i)).get()
                if afk_data.val() is None:
                    return
                else:
                    x = db.child("Mentions").child(str(i)).get()
                    if x.val() is None:
                        db.child("Mentions").child(str(i)).set({"Users:":[message.author.id]})
                    else:
                        u = x.val()['Users']
                        if message.author.id in u:
                            return
                        else:
                            u.append(message.author.id)
                            db.child("Mentions").child(str(i)).set({"Users:":u})

    async def rem_afk(self,message):
        db = firebase.database()
        afk_data = db.child("AFK").child(str(message.guild.id)).child(str(message.author.id)).get()
        try:
            if afk_data.val() is None:
                return
            else:
                db.child("AFK").child(str(message.guild.id)).child(str(message.author.id)).remove()
                x = db.child("Mentions").child(str(message.author.id)).get()
                
                em = discord.Embed(title="AFK removed",description=f"Your AFK was removed {message.author.mention}\n**Mentions while afk:**",color=discord.Color.from_rgb(255,20,147))
                if x.val() is not None:
                    for i in x.val()['Users:']:
                        em.description += f"\n <@{i}>"
                if x.val() is None:
                    em.description += "\nNone"
                db.child("Mentions").child(str(message.author.id)).remove()
                await message.channel.send(message.author.mention,embed=em)
                await message.author.edit(nick = f"{message.author.name}")
        except Exception as e:
            pass
    async def level_up_func(self, message, seen_data):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(message.guild.id)).child("level").get()
        if isEnabled.val() is None:
            if not message.author.bot:
                data = db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).get()
                last_exp = db.child("Last Seen").child(str(message.author.id)).get()
                announcement_channel = db.child("Announcement").child(str(message.guild.id)).get()   
                if data.val() is None:
                    newUser = {"userName":str(message.author),"lvl":1,"exp":1}
                    db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).set(newUser)
                    await self.check_level_role(message,1)
                elif data.val() is not None:
                    if last_exp.val() is None:
                        exp = data.val()['exp']
                        lvl = data.val()['lvl']
                        multi = db.child("Multi").child(str(message.guild.id)).child(str(message.channel.id)).get()
                        if multi.val() is None:
                            exp += self.lvl_add
                        else:
                            exp += multi.val()["Multiplier"]
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
                            if announcement_channel.val() is None:
                                await message.channel.send(mention,embed=lvl_embed)
                            else:
                                ch = announcement_channel.val()["channel"]
                                await self.bot.get_channel(ch).send(mention,embed=lvl_embed)
                            await self.check_level_role(message,lvl)
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
                            multi = db.child("Multi").child(str(message.guild.id)).child(str(message.channel.id)).get()
                            if multi.val() is None:
                                exp += self.lvl_add
                            else:
                                exp += multi.val()["Multiplier"]
                            
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
                                if announcement_channel.val() is None:
                                    await message.channel.send(mention,embed=lvl_embed)
                                else:
                                    ch = announcement_channel.val()["channel"]
                                    await self.bot.get_channel(ch).send(mention,embed=lvl_embed)
                                await self.check_level_role(message,lvl)
                            if seen_data.val() is None:
                                db.child("Last Seen").child(str(message.author.id)).set({"Time":str(datetime.utcnow())})
                            elif seen_data.val() is not None:
                                db.child("Last Seen").child(str(message.author.id)).update({"Time":str(datetime.utcnow())})
                            db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).update({"userName":str(message.author),"exp":exp,"lvl":lvl})

    async def check_level_role(self,message,lvl):
        db = firebase.database()
        x = db.child('LevelRoles').child(message.guild.id).child(lvl).get()
        if not x.val() is None:
            role_id = x.val()["roleid"]
            role = discord.utils.get(message.guild.roles,id=role_id)
            await message.author.add_roles(role)
        else:
            return
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        error = getattr(error, "original", error)
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
            em = discord.Embed(title="Bot Missing Perms",description="Bot might be missing the perms required to use this command. Please check and try again.",color=discord.Color.red())
            msg = await ctx.author.send(embed=em)
            await msg.add_reaction('❌')
        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(title="Command Missing required arguments",description="The command is missing required arguments. See `*help <command_name>` for more details",color=discord.Color.red())
            msg = await ctx.send(embed=em)
            await msg.add_reaction('❌')
        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Missing Permission",description=f"{str(error)}",color=discord.Color.red())
            msg = await ctx.author.send(embed=em)
            await msg.add_reaction('❌')
        elif isinstance(error,discord.errors.Forbidden):
            em = discord.Embed(title="Bot Missing Perms" , description=f"{error}",color=discord.Color.red())
            await ctx.author.send(embed=em)
        else:
            try:
                typ = type(error).__name__
                em = discord.Embed(title="Uh oh!",description=f"""
                An unkown error occured : `{error}`

            Pls try again and if this persists please report in the support server.
                
            [**Support Server**](https://discord.gg/P3BmUsgv5y)""",color=discord.Color.red())

                await ctx.send(embed=em)
            except:
                pass
    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        db = firebase.database()
        x = db.child("Commands").child(str(ctx.command.name)).get()
        if x.val() is None:
            db.child("Commands").child(str(ctx.command.name)).set({"TimesUsed":1})
        else:
            t = x.val()["TimesUsed"]
            db.child("Commands").child(str(ctx.command.name)).update({"TimesUsed":t+1})
def setup(bot):
    bot.add_cog(AllListeners(bot=bot,lvl_add=lvl_add,difficulty=difficulty))