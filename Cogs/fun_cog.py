from datetime import datetime
import discord
from discord.ext import commands
import randfacts
import random
from Database.db_files import firebase
from .Listeners import AllListeners
import pyjokes
import requests
import json
import asyncio
OPTIONS = {
    "1️⃣": 0,
    "2️⃣": 1,
    "3️⃣": 2,
    "4️⃣": 3,
}

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #----------------------- Facts getting command---------------------------------------

    @commands.command(name="facts",aliases=["knowledge","fact"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _facts(self,ctx):
        x = randfacts.getFact(filter=True)
        await ctx.send(f"**{x}**")
    #-------------------------- Truth command ---------------------------------
    @commands.command(name="truth",aliases=["truths"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _truth(self,ctx,user:discord.Member):
        db = firebase.database()
        with open("truth.txt","r",encoding='utf-8') as f:
            truth_text = f.readlines()
        length_truth = random.randint(0,len(truth_text))
        truth = truth_text[length_truth].replace("\n"," ")
        em = discord.Embed(title=f"{ctx.author.name} asks {user.name}", description=f"{truth}",color=discord.Color.random())
        await ctx.send(embed=em)
        


    # @_truth.error
    # async def truth_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         em = HelpEmbeds.truth_embed()
    #         await ctx.send("**Please mention who to ask the question. See help for more details** :point_down::point_down:",embed=em)

    #----------------------- Dare command -----------------------------------------------
    @commands.command(name="dare",aliases=["dares"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _dare(self,ctx,user:discord.Member):
        with open("dare.txt","r",encoding='utf-8') as f:
            dare_text = f.readlines()
        length_dare = random.randint(0,len(dare_text))

        dare = dare_text[length_dare].replace("\n"," ")
        em = discord.Embed(title=f"{ctx.author.name} asks {user.name} to", description=f"{dare}",color=discord.Color.random())
        await ctx.send(embed=em)
        
    # @_dare.error
    # async def dare_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         em = HelpEmbeds.dare_embed()
    #         await ctx.send("**Pls mention whom to give the dare. See help for more details** :point_down::point_down:",embed=em)
    

    #----------------------- 8ball command--------------------------------
    @commands.command(name="8ball",aliases=["predict"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _8ball(self,ctx,*,question):
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
    # @_8ball.error
    # async def _8ball_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         await ctx.send("**Concentrate and ask again.**")

#---------------------- Opinion command ----------------------------
    @commands.command(name="opinion",aliases=["op"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _opinion(self,ctx,user:discord.Member):
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
            

    # @_opinion.error
    # async def opinion_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed=HelpEmbeds.opinion_embed())

    
    @commands.command(name="insult",aliases=["roast"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _insult(self,ctx,user:discord.Member):
        # with open("insult.txt","r") as f:
        #     roast_list = f.readlines()
        api_url = "https://api2.snowflakedev.xyz/api/roast"
        r = requests.get(api_url,headers={"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"}).content.decode()
        roast = json.loads(r)["roast"]
        #roast = roast_list[length_roast].replace("\n"," ")
        em = discord.Embed(title=f"{roast}",color=discord.Color.random())
        await ctx.send(embed=em)
    
    # @commands.command(name="joke")
    # async def 

    @commands.command(name="gayrate",aliases=["gr","gay","gae"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _gayrate(self,ctx,user:discord.Member=None):
        x = random.randint(1,100)
        if user is None:
            user = ctx.author
            em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is {100}% gay as he didn't mention the user. LMAO",color=discord.Color.random())
        else:
            if user.id == 576442029337477130:
                em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is 0% gay.",color=discord.Color.random())
            else:
                em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is {x}% gay.",color=discord.Color.random())
        await ctx.send(embed=em)
    @commands.command(name="genius",aliases=["intelligence","geniusrate","iq"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _genius(self,ctx,user:discord.Member=None):
        x = random.randint(1,100)
        if user is None:
            user = ctx.author
            em = discord.Embed(title=f"{user.name}'s intelligence quotient",description=f"{user.mention} has **{0} IQ** as he didn't mention the user. LMAO",color=discord.Color.random())
        else:
            if user.id == 576442029337477130:
                em = discord.Embed(title=f"{user.name}'s intelligence quotient",description=f"{user.mention} has **200 IQ**.",color=discord.Color.random())
            else:
                em = discord.Embed(title=f"{user.name}'s intelligence quotient",description=f"{user.mention} has **{x} IQ**.",color=discord.Color.random())
        await ctx.send(embed=em)
    @commands.command(name="joke",aliases=["jokes"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _joke(self,ctx):
        jk = pyjokes.get_joke()
        await ctx.send(jk)

    
    @commands.command(name="fight",aliases=["dumbfight"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _fight(self,ctx:commands.Context,user:discord.Member):
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
                    await ctx.send(f"{ctx.author.name} fought with {user.name}. **{a.name} was punched in the face by {user.name} and knocked unconsicious. He is now muted for {mute_time} seconds.**")
                else:
                    await ctx.send(f"{ctx.author.name} fought with {user.name}. **{a.name} was punched in the face by {ctx.author.name} and knocked unconsicious. He is now muted for {mute_time} seconds.**")
                await a.add_roles(mutedRole)
                await asyncio.sleep(mute_time)
                
                await a.remove_roles(mutedRole)
                await ctx.send(f"**{a.name} has been umuted..... Better not fight now**")
                
    # @_fight.error
    # async def fight_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         em = HelpEmbeds.fight_embed()
    #         await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)

    #---------------------Shoot Command and its errors---------------------------------------           
    @commands.command(name="shoot",aliases=["fire","headshot","kill"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _shoot(self,ctx:commands.Context,user:discord.Member):
        a = random.choice([ctx.author,user])
        mutedRole = discord.utils.get(ctx.guild.roles,name='Muted')
        b = random.randint(0,1)
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
                await ctx.send(f"{ctx.author.name} takes out a pistol and shoots himself. **He's on the brink of death. Type `hospital` in the next 10 seconds to save him.**")
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
                await asyncio.sleep(300)
                
                await a.remove_roles(mutedRole)
                await ctx.send(f"**{a.name} has been umuted..... Better not use gun now**")

    @commands.command(name="trivia",aliases=["questions","triv","tr"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _trivia(self,ctx,ques:int=None):
        if ques is None:
            ques = 10
        if ques > 15:
            ques = 15
        elif ques < 1:
            await ctx.send("Sorry cannot have less than 0 questions. So u will have 1 question")
            ques = 1
        url = f"https://opentdb.com/api.php?amount={ques}&type=multiple"
        r = requests.get(url=url).json()
        results = r["results"]
        correct = 0
        for i in range(len(results)):
            cat = results[i]['category']
            
            diff = results[i]['difficulty']
            
            question = results[i]['question']
            question = question.replace("&#039;","'")
            question = question.replace("&quot;","'")
            question = question.replace("&deg;","°")
            question = question.replace("acute;","")
            question = question.replace("&","")

            ans = results[i]['correct_answer']
            ans = ans.replace("&#039;","'")
            ans = ans.replace("&quot;","'")
            ans = ans.replace("&deg;","°")
            ans = ans.replace("acute;","")
            ans = ans.replace("&","")
            wans = results[i]['incorrect_answers']
            
            option = wans
            option.append(ans)
            options = []
            for j in option:
                temp = j.replace("&#039;","'")
                temp = j.replace("&quot;","'")
                temp = temp.replace("&deg;","°")
                temp = temp.replace("acute;","")
                temp = temp.replace("&","")
                options.append(temp)
            random.shuffle(options)
            em = discord.Embed(title=f"Question : {i+1}.)", description=f"**{question}\n1️⃣ {options[0]}\n2️⃣ {options[1]}\n3️⃣ {options[2]}\n4️⃣ {options[3]}**",color = discord.Color.blurple())
            em.add_field(name="Difficulty",value=f"`{diff}`")
            em.add_field(name="Category",value=f"`{cat}`")
            em.set_author(name=f"{ctx.author.name}'s Trivia Game",icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=em)
            def _check(r,u):
                return (r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
                )
            for emoji in list(OPTIONS.keys())[:len(OPTIONS)]:
                await msg.add_reaction(emoji)

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.send("Timed out! You didn't responsed in time")
                break
            else:
                choice = options[OPTIONS[reaction.emoji]]
                if choice == ans:
                    correct += 1
                    em.color = discord.Color.dark_green()
                    await msg.edit(embed=em)
                else:
                    em.color = discord.Color.dark_red()
                    em.set_footer(text=f"✔️Correct answer: {ans}\n❌Your Answer: {choice}")
                    await msg.edit(embed=em)
                await asyncio.sleep(2)
        em = discord.Embed(description=f"**{ctx.author.name}'s Score: {correct}/{ques}**",color=discord.Color.dark_teal())
        await ctx.send(embed=em)
    
    @commands.command(name="animetrivia",aliases=["atrivia","animetriv","atr"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _atrivia(self,ctx,ques:int=None):
        if ques is None:
            ques = 10
        if ques > 15:
            ques = 15
        elif ques < 1:
            await ctx.send("Sorry cannot have less than 0 questions. So u will have 1 question")
            ques = 1
        url = f"https://opentdb.com/api.php?amount={ques}&type=multiple&category=31"
        r = requests.get(url=url).json()
        results = r["results"]
        correct = 0
        for i in range(len(results)):
            cat = results[i]['category']
            
            diff = results[i]['difficulty']
            
            question = results[i]['question']
            question = question.replace("&#039;","'")
            question = question.replace("&quot;","'")
            question = question.replace("&deg;","°")
            question = question.replace("acute;","")
            question = question.replace("&","")

            ans = results[i]['correct_answer']
            ans = ans.replace("&#039;","'")
            ans = ans.replace("&quot;","'")
            ans = ans.replace("&deg;","°")
            ans = ans.replace("acute;","")
            ans = ans.replace("&","")
            wans = results[i]['incorrect_answers']
            
            option = wans
            option.append(ans)
            options = []
            for j in option:
                temp = j.replace("&#039;","'")
                temp = j.replace("&quot;","'")
                temp = temp.replace("&deg;","°")
                temp = temp.replace("acute;","")
                temp = temp.replace("&","")
                options.append(temp)
            random.shuffle(options)
            em = discord.Embed(title=f"Question : {i+1}.)", description=f"**{question}\n1️⃣ {options[0]}\n2️⃣ {options[1]}\n3️⃣ {options[2]}\n4️⃣ {options[3]}**",color = discord.Color.blurple())
            em.add_field(name="Difficulty",value=f"`{diff}`")
            em.add_field(name="Category",value=f"`{cat}`")
            em.set_author(name=f"{ctx.author.name}'s Trivia Game",icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=em)
            def _check(r,u):
                return (r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
                )
            for emoji in list(OPTIONS.keys())[:len(OPTIONS)]:
                await msg.add_reaction(emoji)

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.send("Timed out! You didn't responsed in time")
                break
            else:
                choice = options[OPTIONS[reaction.emoji]]
                if choice == ans:
                    correct += 1
                    em.color = discord.Color.dark_green()
                    await msg.edit(embed=em)
                else:
                    em.color = discord.Color.dark_red()
                    em.set_footer(text=f"✔️Correct answer: {ans}\n❎Your Answer: {choice}")
                    await msg.edit(embed=em)
                await asyncio.sleep(2)
        em = discord.Embed(description=f"**{ctx.author.name}'s Score: {correct}/{ques}**",color=discord.Color.dark_teal())
        await ctx.send(embed=em)
    
    @commands.command(name="simprate",aliases=["simp","srate"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def _simp(self,ctx,user:discord.User=None):
        if user == None:
            user = ctx.author
        db = firebase.database()
        #random.seed()
        x = random.randint(1,100)
        db.child("Simp").child(str(user.id)).set({"Simp":x})
        em = discord.Embed(title=f"{user.name}'s Simp rate",description=f"{user.mention} is **{x}%** Simp.",color=discord.Color.random())
        await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Fun(bot))
