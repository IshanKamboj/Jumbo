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
    
    #----------------------- Facts getting command---------------------------------------

    @commands.command(name="facts",aliases=["knowledge","fact"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _facts(self,ctx):
        x = randfacts.getFact(filter=True)
        await ctx.send(f"**{x}**")
    #-------------------------- Truth command ---------------------------------
    @commands.command(name="truth",aliases=["truths"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _truth(self,ctx,user:discord.Member):
        db = firebase.database()
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
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _dare(self,ctx,user:discord.Member):
        db = firebase.database()
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
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _8ball(self,ctx,*,question):
        db = firebase.database()

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
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _opinion(self,ctx,user:discord.Member):
        db = firebase.database()
            
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
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _insult(self,ctx,user:discord.Member):
        db = firebase.database()
        with open("insult.txt","r") as f:
            roast_list = f.readlines()
        length_roast = random.randint(0,len(roast_list))
        roast = roast_list[length_roast].replace("\n"," ")
        em = discord.Embed(title=f"{roast}",color=discord.Color.random())
        await ctx.send(embed=em)
    
    # @commands.command(name="joke")
    # async def 

    @commands.command(name="gayrate",aliases=["gr","gay","gae"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _gayrate(self,ctx,user:discord.Member=None):
        x = random.randint(1,100)
        if user is None:
            user = ctx.author
            em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is {100}% gay as he didn't mention the user. LMAO",color=discord.Color.random())
        else:
            em = discord.Embed(title=f"{user.name}'s Gayrate",description=f"{user.mention} is {x}% gay.",color=discord.Color.random())
        await ctx.send(embed=em)
    
    @commands.command(name="joke",aliases=["jokes"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _joke(self,ctx):
        jk = pyjokes.get_joke()
        await ctx.send(jk)

def setup(bot):
    bot.add_cog(Fun(bot))