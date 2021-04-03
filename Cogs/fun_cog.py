import discord
from discord.ext import commands
import randfacts
import random
from Database.db_files import firebase
import asyncio
from helpEmbeds import HelpEmbeds
from .Listeners import AllListeners
import pyjokes

with open("truth.txt","r",encoding='utf-8') as f:
    truth_text = f.readlines()
with open("dare.txt","r") as f:
    dare_text = f.readlines()

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #---------------------Fight Command and its errors---------------------------------------
    @commands.command(name="fight",aliases=["dumbfight"])
    async def _fight(self,ctx:commands.Context,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("fight").get()
        if isEnabled.val() is None:
            gloves = db.child('Items').child("gloves").child(str(ctx.author.id)).get()
            gloves_user = db.child('Items').child("gloves").child(str(user.id)).get()
            if gloves.val() is None and gloves_user.val() is None:
                a = random.choice([ctx.author,user])
            elif gloves_user is not None and gloves.val() is None:
                a = random.choice([ctx.author,ctx.author,user,user,user])

            elif gloves.val() is not None and gloves_user is None:
                a = random.choice([ctx.author,ctx.author,ctx.author,user,user])
            else:
                a = random.choice([ctx.author,user])

            mutedRole = discord.utils.get(ctx.guild.roles,name='Muted')
            if not mutedRole:
                mutedRole = await ctx.guild.create_role(name='Muted')
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            if mutedRole in user.roles:
                await ctx.send(f"**{user.name} is already unconsicious.... Pick someone else to fight.... YOU COWARD**")
            elif mutedRole in ctx.author.roles:
                await ctx.send(f"**{ctx.author.name} u cannot fight....... U were already beaten up LMAO**")
            else:
                if ctx.author == user:
                    await ctx.send(f"**{ctx.author.mention}.... Was So stupid he punched himself and couldn't take it.... he has been muted for 60 seconds**")
                    await user.add_roles(mutedRole)
                    await asyncio.sleep(60)
                    await user.remove_roles(mutedRole)
                elif user == self.bot.user:
                    await ctx.send(f"{ctx.author.mention} **U cannot fight me......LMAO**")
                else:
                    mute_time = random.randint(20,60)
                    if a == ctx.author:
                        await ctx.send(f"{ctx.author.name} fought with {user.name}. **{a.name} was punched in the face by {user.name} and knocked unconsicious. He is now muted for {mute_time} seconds.\n{user.name} was given 5 points for winning.**")
                        x = db.child('FightPoints').child(str(user.id)).get()
                        db.child('FightPoints').child(str(user.id)).update({"points":x.val()["points"]+5})
                    else:
                        await ctx.send(f"{ctx.author.name} fought with {user.name}. **{a.name} was punched in the face by {ctx.author.name} and knocked unconsicious. He is now muted for {mute_time} seconds. \n{ctx.author.name} was given 5 points for winning.**")
                        x = db.child('FightPoints').child(str(ctx.author.id)).get()
                        db.child('FightPoints').child(str(ctx.author.id)).update({"points":x.val()["points"]+5})
                    await a.add_roles(mutedRole)
                    await asyncio.sleep(mute_time)
                    
                    await a.remove_roles(mutedRole)
                    await ctx.send(f"**{a.name} has been umuted..... Better not fight now**")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
                
    @_fight.error
    async def fight_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.fight_embed()
            await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)

    #---------------------Shoot Command and its errors---------------------------------------           
    @commands.command(name="shoot",aliases=["fire","headshot","kill"])
    async def _shoot(self,ctx:commands.Context,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("shoot").get()
        if isEnabled.val() is None:
            gun = db.child('Items').child("gun").child(str(ctx.author.id)).get()
            break_chance = random.randint(0,11)
            if gun.val() is None or gun.val()["amount"] == 0:
                await ctx.send(f"{ctx.author.mention} **You dont have a gun so you cannot shoot. Purchase one from shop.....smh**")
            else:
                a = random.choice([ctx.author,user])
                b = random.randint(0,1)
                
                mutedRole = discord.utils.get(ctx.guild.roles,name='Muted')
                def check(msg):
                    return msg.content.lower() in ["hospital","ambulance"] and msg.author != a
                if not mutedRole:
                    mutedRole = await ctx.guild.create_role(name='Muted')
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                if mutedRole in user.roles:
                    await ctx.send(f"**{user.name} is already dead or fainted.... Try to shoot someone else.... YOU BITCH**")
                elif mutedRole in ctx.author.roles:
                    await ctx.send(f"**{ctx.author.name} u cannot shoot....... U are in hospital LMAO**")
                elif user == self.bot.user:
                    await ctx.send(f"{ctx.author.mention} **U cannot shoot me......LMAO**")
                else:
                    if ctx.author == user:
                        await ctx.send(f"{ctx.author.name} takes out a pistol and shoots himself. **He is now muted for 60 minutes**")
                    elif ctx.author == a:
                        await ctx.send(f"{ctx.author.name} tried to shoot {user.name} but did not know how to use the gun. **He shot himself and is on the brink of death**\n **Type `hospital` in next 10 seconds to save him.**")
                    else:
                        await ctx.send(f"{ctx.author.name} takes out a pistol and shoots {user.name} in head.**{user.name} is on the brink of death**\n **Type `hospital` in next 10 seconds to save him.**")
                    await a.add_roles(mutedRole)
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=10) # 10 seconds to reply
                        if b != 1:
                            raise asyncio.TimeoutError
                        await ctx.send(f"**Hush! It was a close call. {a.name} was saved**")
                        await a.remove_roles(mutedRole)
                    except asyncio.TimeoutError:
                        await ctx.send(f"Sorry, either it was too late or doctors were not able to save {a.name}. **he is now muted for 5 minutes**")
                        if break_chance == 9 or break_chance == 10:
                            number = gun.val()["amount"]
                            db.child('Items').child("gun").child(str(ctx.author.id)).update({"amount":number-1})
                            await ctx.send(f"Oh! {ctx.author.mention} Your gun broke. Now you have {number-1} remaining")
                        await asyncio.sleep(300)
                        
                        await a.remove_roles(mutedRole)
                        await ctx.send(f"**{a.name} has been umuted..... Better not use gun now**")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @_shoot.error
    async def shoot_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.shoot_embed()
            await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)
    #----------------------- Facts getting command---------------------------------------

    @commands.command(name="facts",aliases=["knowledge","fact"])
    async def _facts(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("fact").get()
        if isEnabled.val() is None:

            x = randfacts.getFact(filter=True)
            await ctx.send(f"**{x}**")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    #-------------------------- Truth command ---------------------------------
    @commands.command(name="truth",aliases=["truths"])
    async def _truth(self,ctx,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("truth").get()
        if isEnabled.val() is None:
            length_truth = random.randint(0,len(truth_text))
            truth = truth_text[length_truth].replace("\n"," ")
            em = discord.Embed(title=f"{ctx.author.name} asks {user.name}", description=f"{truth}",color=discord.Color.random())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)


    @_truth.error
    async def truth_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.truth_embed()
            await ctx.send("**Please mention who to ask the question. See help for more details** :point_down::point_down:",embed=em)

    #----------------------- Dare command -----------------------------------------------
    @commands.command(name="dare",aliases=["dares"])
    async def _dare(self,ctx,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("dare").get()
        if isEnabled.val() is None:
            length_dare = random.randint(0,len(dare_text))
            dare = dare_text[length_dare].replace("\n"," ")
            em = discord.Embed(title=f"{ctx.author.name} asks {user.name} to", description=f"{dare}",color=discord.Color.random())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @_dare.error
    async def dare_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.dare_embed()
            await ctx.send("**Pls mention whom to give the dare. See help for more details** :point_down::point_down:",embed=em)
    

    #----------------------- 8ball command--------------------------------
    @commands.command(name="8ball",aliases=["predict"])
    async def _8ball(self,ctx,*,question):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("8ball").get()
        if isEnabled.val() is None:

            response = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Don't count on it.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
            answer = random.choice(response)
            em = discord.Embed(title=f"Answer to {ctx.author.name}'s Question",description=f"{answer}",color=discord.Color.random())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @_8ball.error
    async def _8ball_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("**Concentrate and ask again.**")

#---------------------- Opinion command ----------------------------
    @commands.command(name="opinion",aliases=["op"])
    async def _opinion(self,ctx,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("opinion").get()
        if isEnabled.val() is None:
            
                opinion_list = ["I think they are a dumbass",
                "My opinion is that they are kind of smart",
                "I guess they are stupid.",
                "Hmm.... He's just laughing all the time (kind of stupid)",
                "I think of them as a moron",
                "He's kind of weird... eww",
                "I believe that they are clever",
                "In my experience they are kind",
                "Personally I think they are shot-tempered",
                "Sabse bada chutiya :middle_finger::middle_finger:",
                "I dont want to tell you",
                "I think to punch them if I ever see them :punch:",
                "They are kind of a good person",
                "LAZY......nothing more nothing less",
                "They are a kind person",
                "I think they are a quick learner",
                "Hmm... I would not share my opinion with the likes of you",
                "Honestly speaking, all of the members here are just a piece of shit.",
                "Crap just Crap",
                "They are nice",
                "They talk a lot",
                "He thinks of himself as a very wise person, but everyone knows he is not."
                ]
                random_response = random.choice(opinion_list)
                em = discord.Embed(description=f"**{random_response}**",color=discord.Color.random())
                await ctx.send(embed=em)
            
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)

    @_opinion.error
    async def opinion_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed=HelpEmbeds.opinion_embed())

    
    @commands.command(name="insult",aliases=["roast"])
    async def _insult(self,ctx,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("insult").get()
        if isEnabled.val() is None:
            with open("insult.txt","r") as f:
                roast_list = f.readlines()
            length_roast = random.randint(0,len(roast_list))
            roast = roast_list[length_roast].replace("\n"," ")
            em = discord.Embed(title=f"{roast}",color=discord.Color.random())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    
    # @commands.command(name="joke")
    # async def 

    @commands.command(name="gayrate",aliases=["gr","gay","gae"])
    @commands.check(AllListeners.check_enabled)
    async def _gayrate(self,ctx,user:discord.Member=None):
        x = random.randint(1,100)
        if user is None:
            user = ctx.author
            em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is {100}% gay as he didn't mention the user. LMAO",color=discord.Color.random())
        else:
            em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is {x}% gay.",color=discord.Color.random())
        await ctx.send(embed=em)
    
    @commands.command(name="joke",aliases=["jokes"])
    async def _joke(self,ctx):
        jk = pyjokes.get_joke()
        await ctx.send(jk)