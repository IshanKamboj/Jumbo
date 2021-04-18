import discord
from discord.ext import commands
import os
import random
import asyncio
from helpEmbeds import HelpEmbeds
from discord import Intents
from Database.db_files import firebase
#----------------------- Prefix getting and bot setup--------------------------------
def get_prefix(client,message):
    try:
        db = firebase.database()
        data = db.child('Prefixes').child(str(message.guild.id)).get()
        return data.val()['Prefix']
    except:
        return "j!"

intent = Intents().all()   

bot = commands.AutoShardedBot(command_prefix=get_prefix,intents=intent,case_insensitive=True)
bot.remove_command("help")



## Making a group of Help cmds and embeds..........############################

@bot.group(invoke_without_command=True)
async def help(ctx):
    color_list = random.randint(0,250),random.randint(0,250),random.randint(0,250) 

    em = discord.Embed(title="Help",description="""
    **Jumbo is a fun bot... use it to have fun with ur friends in the same server.**

It also has many utility commands such as afk,dm,autreact. There are also fun commands.
Don't forget levelling.... Jumbo also has a levelling system to check who's active or who's not.

Default Prefix : `j!` (Mention to know the prefix of your server)
    
Use *help <command> for extended information on a command
    
[** •Invite me**](https://discord.com/api/oauth2/authorize?client_id=805430097426513941&permissions=1008073792&scope=bot "Add the bot to your server")[** •Support Server**](https://discord.gg/P3BmUsgv5y "Join the support server")
    
    """,color=discord.Color.random())
    em.add_field(name=":tools: | Utility Commands", value="`*help utility`")
    em.add_field(name=":lock: | Admin Commands",value="`*help admin`")
    em.add_field(name=":joystick: | Fun Commands",value="`*help fun`")
    em.add_field(name=":karate_uniform: | Fight Commands",value='`*help fights`')
    em.add_field(name=":hugging: | Action Commands",value="`*help action`")
    em.add_field(name=":mag: | Info Commands",value="`*help info`")
    em.add_field(name=":camera: | Image Commands",value="`*help image`")
    em.add_field(name=":triangular_ruler: | Calculation Commands",value="`*help calculation`")
    await ctx.send(embed=em)

#------------------------------ Section of help cmds -----------------------------
@help.command(name="utility")
async def utility(ctx):
    em = discord.Embed(title=":tools: | Utility commands",description="`Level`, `Leaderboard`, `AFK`, `Seen`, `Autoreact`, `Google`, `Wikisearch`, `Hex`, `Poll`, `Animesearch`, `Vote`, `Emoji`, `Report`, `Pokedex`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name="admin")
async def admin(ctx):
    em = discord.Embed(title=":lock: | Admin Commands",description="`Givelevel`, `Prefix`, `Purge`, `Disable`, `Enable`, `Role`, `Settings`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name="fun")
async def fun(ctx):
    em = discord.Embed(title=":joystick: | Fun Commands",description="`Fact`, `Truth`, `Dare`, `8ball`, `Opinion`, `Roast`, `Joke`, `Gayrate`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name="fights")
async def fight_help(ctx):
    em = discord.Embed(title=":karate_uniform: | Fight Commands",description="`Fight`, `Shoot`, `Train`, `Profile`, `Buy`, `Shop`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name="action",aliases=["actions"])
async def action(ctx):
    em = discord.Embed(title=":hugging: | Action Commands",description="`Slap`, `Punch`, `Kick`, `Hardkick`, `Lick`, `Bite`, `Bully`, `Hug`, `Pat`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name="info")
async def action(ctx):
    em = discord.Embed(title=":mag: | Info Commands",description="`Userinfo`, `Roleinfo`, `OnlineInfo`, `Ping`, `Avatar`, `Snipe`, `Editsnipe`,`Botinfo`, `Whois`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name='image')
async def image(ctx):
    em = discord.Embed(title=":camera: | Image Commands",description="`Wanted`, `Rip`, `Wallpaper`",color=discord.Color.random())
    await ctx.send(embed=em)

@help.command(name='calculation')
async def calculation(ctx):
    em = discord.Embed(title=':triangular_ruler: | Calculation Commands',description="`Area`, `Volume`, `Factorial`",color=discord.Color.random())
    await ctx.send(embed=em)
#-------------------------------LEVEL HELP COMMAND-----------------------------------
@help.command(name="Level",aliases=["level","lvl","rank","rnk"])
async def Level(ctx):
    em = HelpEmbeds.level_embed()
    await ctx.send(embed = em)

#-------------------------------LEADERBOARD HELP COMMAND-----------------------------------
@help.command(name="Leaderboard",aliases=["lb","leader","top"])
async def Leaderboard(ctx):
    em = HelpEmbeds.leaderboard_embed()
    await ctx.send(embed = em)

#-------------------------------GIVE LEVEL HELP COMMAND-----------------------------------
@help.command(name="givelevel",aliases=["gl"])
async def givelevel(ctx):
    em = HelpEmbeds.givelevel_embed()
    await ctx.send(embed = em)

#-------------------------------FIGHT HELP COMMAND-----------------------------------
@help.command(name="fight",aliases=["dumbfight"])
async def fight(ctx):
    em = HelpEmbeds.fight_embed()
    await ctx.send(embed = em)

#-------------------------------CHANGE PREFIX HELP COMMAND-----------------------------------
@help.command(name="prefix",aliases=["cp","changeprefix"])
async def prefix(ctx):
    em = HelpEmbeds.prefix_embed()
    await ctx.send(embed = em)

#-------------------------------AFK HELP COMMAND-----------------------------------
@help.command(name="afk")
async def afk(ctx):
    em = HelpEmbeds.afk_embed()
    await ctx.send(embed = em)


#-------------------------------SHOOT HELP COMMAND-----------------------------------
@help.command(name="shoot")
async def shoot(ctx):
    em = HelpEmbeds.shoot_embed()
    await ctx.send(embed = em)

#-------------------------------Last Seen help command---------------------------------
@help.command(name="seen",aliases=["lastseen"])
async def seen(ctx):
    em = HelpEmbeds.seen_embed()
    await ctx.send(embed=em)

#--------------------------------- Facts Help command-----------------------------
@help.command(name="fact",aliases=["facts"])
async def fact(ctx):
    em = HelpEmbeds.fact_embed()
    await ctx.send(embed=em)

#------------------------------------- Truth help cmd-------------------------------
@help.command(name="truth",aliases=["truths"])
async def truth(ctx):
    em = HelpEmbeds.truth_embed()
    await ctx.send(embed=em)
#------------------------------------- Dare help cmd----------------------- --------
@help.command(name="dare",aliases=["dares"])
async def dare(ctx):
    em = HelpEmbeds.dare_embed()
    await ctx.send(embed=em)


#-------------------------------------- Auto react help command---------------------------------
@help.command(name="autoreact",aliases=["ar","react","reaction"])
async def autoreact(ctx):
    em = HelpEmbeds.autoreact_embed()
    await ctx.send(embed=em)



#---------------------------------- Spam help--------------------------
@help.command(name="spam",aliases=["sp"])
async def spam(ctx):
    em = HelpEmbeds.spam_embed()
    await ctx.send(embed=em)
#---------------------------------- Purge help ---------------------------
@help.command(name="purge",aliases=["pu","delete"])
async def purge(ctx):
    em = HelpEmbeds.purge_embed()
    await ctx.send(embed=em)

#------------------------------ 8ball help ----------------------------
@help.command(name="8ball",aliases=["predict"])
async def _8ball_help(ctx):
    em = HelpEmbeds._8ball_embed()
    await ctx.send(embed=em)

#--------------------------- opinion help cmd -------------------
@help.command(name="opinion",aliases=["op"])
async def opinion(ctx):
    await ctx.send(embed=HelpEmbeds.opinion_embed())

@help.command(name="enable")
async def enable(ctx):
    await ctx.send(embed=HelpEmbeds.enable_embed())

@help.command(name="disable")
async def disable(ctx):
    await ctx.send(embed=HelpEmbeds.disable_embed())

@help.command(name="role")
async def role(ctx):
    await ctx.send(embed=HelpEmbeds.role_embed())
@help.command(name="shop")
async def shop(ctx):
    await ctx.send(embed=HelpEmbeds.shop_embed())
@help.command(name="buy")
async def buy(ctx):
    await ctx.send(embed=HelpEmbeds.buy_embed())
@help.command(name="profile")
async def profile(ctx):
    await ctx.send(embed=HelpEmbeds.profile_embed())
@help.command(name="train")
async def train(ctx):
    await ctx.send(embed=HelpEmbeds.train_embed())
@help.command(name="google",aliases=["search","find"])
async def google(ctx):
    await ctx.send(embed=HelpEmbeds.google_embed())
@help.command(name="insult",aliases=["roast"])
async def insult(ctx):
    await ctx.send(embed=HelpEmbeds.roast_embed())

@help.command(name="slap")
async def slap(ctx):
    await ctx.send(embed=HelpEmbeds.slap_embed())

@help.command(name="punch")
async def punch(ctx):
    await ctx.send(embed=HelpEmbeds.punch_embed())

@help.command(name="hug")
async def hug(ctx):
    await ctx.send(embed=HelpEmbeds.hug_embed())

@help.command(name="bite")
async def bite(ctx):
    await ctx.send(embed=HelpEmbeds.bite_embed())

@help.command(name="bully")
async def bully(ctx):
    await ctx.send(embed=HelpEmbeds.bully_embed())

@help.command(name="lick")
async def lick(ctx):
    await ctx.send(embed=HelpEmbeds.lick_embed())

@help.command(name="kick")
async def kick(ctx):
    await ctx.send(embed=HelpEmbeds.kick_embed())

@help.command(name="hardkick")
async def hardkick(ctx):
    await ctx.send(embed=HelpEmbeds.hardkick_embed())

@help.command(name="userinfo")
async def userinfo(ctx):
    await ctx.send(embed=HelpEmbeds.userinfo_embed())

@help.command(name="roleinfo",aliases=["rinfo"])
async def roleinfo(ctx):
    await ctx.send(embed=HelpEmbeds.roleinfo_embed())

@help.command(name="onlineinfo",aliases=["online"])
async def onlineinfo(ctx):
    await ctx.send(embed=HelpEmbeds.onlineinfo_embed())
@help.command(name="avatar",aliases=["av","pfp"])
async def avatar(ctx):
    await ctx.send(embed=HelpEmbeds.avatar_embed())
    
@help.command(name="snipe")
async def snipe(ctx):
    await ctx.send(embed=HelpEmbeds.snipe_command())

@help.command(name="editsnipe")
async def editsnipe(ctx):
    await ctx.send(embed=HelpEmbeds.editsnipe_command())

@help.command(name="gayrate",aliases=["gr","gay","gae"])
async def gayrate(ctx):
    await ctx.send(embed=HelpEmbeds.gayrate_embed())

@help.command(name="joke",aliases=["jokes"])
async def joke(ctx):
    await ctx.send(embed=HelpEmbeds.joke_embed())

@help.command(name="botinfo",aliases=["bi","binfo","boti"])
async def botinfo(ctx):
    await ctx.send(embed=HelpEmbeds.botinfo_embed())

@help.command(name='whois')
async def whois(ctx):
    await ctx.send(embed=HelpEmbeds.whois_embed())

@help.command(name="wikisearch",aliases=["wsearch","wikipedia"])
async def wikisearch(ctx):
    await ctx.send(embed=HelpEmbeds.wikisearch_embed())

@help.command(name="wanted")
async def wanted(ctx):
    await ctx.send(embed=HelpEmbeds.wanted_embed())

@help.command(name="rip")
async def rip(ctx):
    await ctx.send(embed=HelpEmbeds.rip_embed())

@help.command(name="hex")
async def hex(ctx):
    await ctx.send(embed=HelpEmbeds.hex_embed())

@help.command(name="wallpaper")
async def wallpaper(ctx):
    await ctx.send(embed=HelpEmbeds.wallpaper_embed())

@help.command(name="poll")
async def poll(ctx):
    await ctx.send(embed=HelpEmbeds.poll_embed())

@help.command(name="vote",aliases=["upvote"])
async def vote(ctx):
    await ctx.send(embed=HelpEmbeds.vote_embed())

@help.command(name="animesearch",aliases=["anime"])
async def anime(ctx):
    await ctx.send(embed=HelpEmbeds.anime_embed())
@help.command(name='area')
async def area(ctx):
    await ctx.send(embed=HelpEmbeds.area_embed())

@help.command(name='volume')
async def volume(ctx):
    await ctx.send(embed=HelpEmbeds.volume_embed())

@help.command(name='factorial')
async def factorial(ctx):
    await ctx.send(embed=HelpEmbeds.factorial_embed())

@help.command(name="settings",aliases=["setting"])
async def settings(ctx):
    await ctx.send(embed=HelpEmbeds.settings_embed())

@help.command(name="emojisearch",aliases=["esearch","emoji"])
async def emojisearch(ctx):
    await ctx.send(embed=HelpEmbeds.emojisearch_embed())
@help.command(name="report",aliases=["bug"])
async def report(ctx):
    await ctx.send(embed=HelpEmbeds.report_embed())
@help.command(name="pokedex",aliases=["pokesearch","pokemon"])
async def pokedex(ctx):
    await ctx.send(embed=HelpEmbeds.pokedex_embed())
#####################################    LOADING COGS    #########################################################
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')
    else:
        print(f"Could not load: Cogs.{filename[:-3]}")


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)