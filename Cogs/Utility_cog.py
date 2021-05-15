import discord
from discord.ext import commands
import random
from helpEmbeds import HelpEmbeds
from Database.db_files import firebase
from Image_generation import LevelIMG
import asyncio
from bs4 import BeautifulSoup
import requests
from googlesearch import search
from .Listeners import AllListeners,difficulty
import wikipedia
from mal import AnimeSearch
from datetime import datetime
from colour import Color
import json
class Utility(commands.Cog):
    def __init__(self,bot,difficulty):
        self.bot = bot
        self.difficulty = difficulty

    #---------------------level Command and its errors---------------------------------------
    @commands.command(name = "level", aliases = ["lvl","rank","rnk"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _level(self,ctx:commands.Context,*,user=""):
        """Check ur Level with this.        
        Mention ur friend or use his ID to see their level.
        """
        database = firebase.database()
        if user == "":
            try:
                data = database.child('Levels').child(str(ctx.guild.id)).child(str(ctx.author.id)).get()
                x = data.val()["exp"]
                y = data.val()["lvl"]
                temp = []
                rnk_data = database.child('Levels').child(str(ctx.guild.id)).get()
                ti = []
                for i in rnk_data.each():
                    ti.append(i.val())
                ordered_list = sorted(ti, key=lambda k: k['exp'],reverse=True)
                for i in ordered_list:
                    temp.append(i["userName"]) 
                
                
                rank = (temp.index(str(ctx.author)))+1
                    
                image = LevelIMG(ctx.message.author.avatar_url,str(ctx.author),x,y,self.difficulty,rank)
                instance = image.drawIMG()
                with open('LVL.png', 'rb') as fp:
                    await ctx.send(file=discord.File(fp, 'LVL.png'))

            except TypeError:
                image = LevelIMG(ctx.message.author.avatar_url,str(ctx.author),0,1,self.difficulty,0)
                instance = image.drawIMG()
                with open('LVL.png', 'rb') as fp:
                    await ctx.send(file=discord.File(fp, 'LVL.png'))

            
        elif user != "":
            user = user.replace("<","")
            user = user.replace(">","")
            user = user.replace("@","")
            user = user.replace("!","")
            a = await self.bot.fetch_user(user)
            try:
                data = database.child('Levels').child(str(ctx.guild.id)).child(str(user)).get()
                x = data.val()["exp"]
                y = data.val()["lvl"]
                temp = []
                rnk_data = database.child('Levels').child(str(ctx.guild.id)).get()
                ti = []
                for i in rnk_data.each():
                    ti.append(i.val())
                ordered_list = sorted(ti, key=lambda k: k['exp'],reverse=True)
                for i in ordered_list:
                    temp.append(i["userName"])    
                
                
                rank = (temp.index(str(a)))+1
                image = LevelIMG(a.avatar_url,str(a),x,y,self.difficulty,rank)
                instance = image.drawIMG()
                with open('LVL.png', 'rb') as fp:
                    await ctx.send(file=discord.File(fp, 'LVL.png'))
            except TypeError:
                (x,y) = (0,1)
                image = LevelIMG(a.avatar_url,str(a),x,y,self.difficulty,0)
                instance = image.drawIMG()
                with open('LVL.png', 'rb') as fp:
                    await ctx.send(file=discord.File(fp, 'LVL.png'))
            except:
                await ctx.send("Pls mention the user or use his id.")



#---------------------leaderboard Command and its errors---------------------------------------
    @commands.command(name="leaderboard",aliases=["lb","leader","top"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _leaderboard(self,ctx:commands.Context):
        database = firebase.database()
        rnk_data = database.child('Levels').child(str(ctx.guild.id)).get()
        ti = []
        for i in rnk_data.each():
            ti.append(i.val())

        
        ordered_list = sorted(ti, key=lambda k: k['exp'],reverse=True)
        temp = []
        temp2 = []
        temp3 = []
        for i in ordered_list:
            temp.append(i["userName"])
            temp2.append(i["exp"])
            temp3.append(i["lvl"])
        leaderboard_embed = discord.Embed(title=f"**{ctx.guild.name}**",color=discord.Color.random()).set_thumbnail(url=f"{str(ctx.guild.icon_url)}").set_author(name="LeaderBoard")
        
        for i in range(len(temp)):
            if i ==0: 
                leaderboard_embed.add_field(name=f":first_place: ----> {temp[i]}",value=f"EXP: `{temp2[i]}`\n LVL: `{temp3[i]}`  ",inline=False)
            if i == 1:
                leaderboard_embed.add_field(name=f":second_place: ----> {temp[i]}",value=f"EXP: `{temp2[i]}`\n LVL: `{temp3[i]}` ",inline=False)
            if i == 2:
                leaderboard_embed.add_field(name=f":third_place: ----> {temp[i]}",value=f"EXP: `{temp2[i]}`\n LVL: `{temp3[i]}` ",inline=False)
            elif i < 10 and i > 2:
                leaderboard_embed.add_field(name=f"{i+1}. {temp[i]}",value=f"EXP: `{temp2[i]}`\n LVL: `{temp3[i]}` ",inline=False)
        await ctx.send(embed=leaderboard_embed)
        





#---------------------AFK Command and its errors---------------------------------------
    @commands.command(name="afk")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    # @commands.has_permissions(manage_nickname)
    async def _afk(self,ctx:commands.Context,*,reason="Busy...smh"):
        db = firebase.database()
        data = db.child("AFK").child(str(ctx.guild.id)).child(str(ctx.author.id)).get()
        if data.val() is None:
            db.child("AFK").child(str(ctx.guild.id)).child(str(ctx.author.id)).set({"reason":reason})        
            em = discord.Embed(title="SET AFK",description=f"I set your AFK {ctx.author.mention}, reason : {reason}",color=discord.Color.from_rgb(255,20,147))
            await ctx.send(embed=em)
            await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
        elif data.val() is not None:
            db.child("AFK").child(str(ctx.guild.id)).child(str(ctx.author.id)).remove()
            em = discord.Embed(title="AFK removed",description=f"Your AFK was removed {ctx.author.mention}",color=discord.Color.from_rgb(255,20,147))
            await ctx.send(ctx.author.mention,embed=em)
            await ctx.author.edit(nick = f"{ctx.author.name}")
        
    @_afk.error
    async def afk_error(self,ctx,error):
        if isinstance(error,commands.BotMissingPermissions):
            pass

#---------------------------Last seen command---------------------
    @commands.command(name="seen",aliases=["lastseen","last"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _seen(self,ctx:commands.Context,user:discord.Member):
        db = firebase.database()
        seen_data = db.child("Last Seen").child(str(user.id)).get()
        if seen_data.val() is None:
            await ctx.send("**I have not seen that user so far.**")
        else:
            time = seen_data.val()["Time"]
            time_seen = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
            final_time = datetime.utcnow()-time_seen
            total_min = round((final_time.total_seconds())/60)
            temp = 0
            while total_min >= 60:
                total_min -= 60
                temp += 1
            minutes = total_min-temp*(60)
            if temp == 0:
                em = discord.Embed(description=f"**`{user.name}` was last seen `{minutes} minutes` ago.**",color=discord.Color.random())
                await ctx.send(embed=em)
            else:
                em = discord.Embed(description=f"**`{user.name}` was last seen more than `{temp} hours` ago.**",color=discord.Color.random())
                await ctx.send(embed=em)



#------------------------ Custom auto react------------------------------------------
    @commands.command(name="autoreact",aliases=["ar","react","reaction"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _autoreact(self,ctx,sign:str,reaction):
        try:
            db = firebase.database()
            react_data = db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).get()
            if react_data.val() is None:
                if sign=="+":
                    db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).set({'Reaction':[reaction]})
                    em = discord.Embed(title="Custom Reaction added",description=f"{reaction} was added as an auto react for you {ctx.author.mention}. Reaction will be added when u are mentioned",color=discord.Color.random())
                    await ctx.send(embed=em)
                elif sign =="-":
                    await ctx.send("You have no autoreact setup")
            elif len(react_data.val()["Reaction"]) < 3 and sign=="+" and ctx.author.id != 576442029337477130:
                if react_data.val() is not None:
                    temp = react_data.val()["Reaction"]
                    temp.append(reaction)
                    db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).update({'Reaction':temp})
                    em = discord.Embed(title="Custom Reaction added",description=f"{reaction} was also added as your auto react {ctx.author.mention}. Reactions will be added when u are mentioned",color=discord.Color.random())
                    await ctx.send(embed=em)
            elif sign == "+" and ctx.author.id == 576442029337477130:
                if react_data.val() is not None:
                    temp = react_data.val()["Reaction"]
                    temp.append(reaction)
                    db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).update({'Reaction':temp})
                    em = discord.Embed(title="Custom Reaction added",description=f"{reaction} was also added as your auto react {ctx.author.mention}. Reactions will be added when u are mentioned",color=discord.Color.random())
                    await ctx.send(embed=em)
            elif sign == "-":
                if react_data.val() is not None:
                    temp = react_data.val()["Reaction"]
                    temp.remove(reaction)
                    db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).update({'Reaction':temp})
                    em = discord.Embed(title="Custom Reaction removed",description=f"{reaction} was removed as your auto react {ctx.author.mention}.",color=discord.Color.random())
                    await ctx.send(embed=em)
            else:
                await ctx.send("**You can only add upto 3 autoreacts.**")
            
        except Exception as e:
            pass

            #print(str(e))


        
    @commands.command(name="google",aliases=["search","find"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _google(self,ctx,*,query):
        db = firebase.database()
        temp = {}
        for j in search(query,tld="co.in" ,num=5,start=0, stop=5, pause=1): 
            #temp.append(j)
            url = str(j)
            response = requests.get(url)
            soup = BeautifulSoup(response.text,features="html.parser")

            metas = soup.find_all('meta')

            #desc = [ meta for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
            for m in metas:
                if m.get ('name') == 'description':
                    temp[j] = m.get('content')
                
        #print(temp)
        em = discord.Embed(title=f"Google Search: {query}",color=discord.Color.random())
        for k,v in temp.items():
            em.add_field(name=f"{k}",value=f"{v}",inline=False)
        await ctx.send(embed=em)
        # print(desc)
        # print(temp)

    @commands.command(name="wikisearch",aliases=["wsearch","wikipedia"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _wikisearch(self,ctx,*,query:str):
        x = wikipedia.summary(query,sentences=7)
        pg = wikipedia.page(query)
        link = pg.url
        em = discord.Embed(title='Wikipedia Results',description=f"**{x}**\n[**Click here**]({link}) for more info.",color=discord.Color.green())
        await ctx.send(embed=em)
    
    @commands.command(name="poll")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _poll(self,ctx,*,question:str):
        await ctx.message.delete()
        msg = await ctx.send(f'**{str(ctx.author)} asks** {question}')
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
            
    @commands.command(name="animesearch",aliases=['anime'])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _animesearch(self,ctx,*,query:str):
        search = AnimeSearch(query)
        url = f"https://api.jikan.moe/v3/search/anime?q={query}"
        r = requests.get(url=url).json()
        #print(r["results"][0])
        synopsis = r["results"][0]["synopsis"]
        title = r["results"][0]["title"]
        episodes = r["results"][0]["episodes"]
        score = r["results"][0]["score"]
        image_url = r["results"][0]["image_url"]
        url = r["results"][0]["url"]
        members = r["results"][0]["members"]
        start_date = r["results"][0]["start_date"]
        x = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S%z")
        end_date = r["results"][0]["end_date"]
        rated = r["results"][0]["rated"]
        em = discord.Embed(title=title,description=f"**{synopsis} [Read More]({url})**",color=discord.Color.random())
        em.add_field(name=":star: Ratings:",value=f"{score}/10")
        em.add_field(name=":tv: Episodes:",value=f"{episodes}")
        em.add_field(name=":clapper: Rated:",value=rated)
        em.add_field(name=":bust_in_silhouette: Users:",value=members)
        em.add_field(name=":satellite: Release Date:",value=x.strftime("%d %b %Y"))
        if end_date is not None:
            y = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S%z")
            em.add_field(name="End Date:",value=y.strftime("%d %b %Y"))
        else:
            em.add_field(name="End Date:",value="Still Airing")
        em.set_image(url=image_url)
        await ctx.send(embed=em)
    
    @commands.command(name="hex",aliases=["gethex"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _hex(self,ctx,*,color:str):
        c = Color(color=color)
        await ctx.send(f"The hex value for {color} color is: {c.hex_l}")
    @commands.command(name="vote",aliases=["upvote"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _vote(self,ctx):
        # db = firebase.database()
        # x = db.child('Items').child("gun").child(str(ctx.author.id)).get()
        # if x.val() is None:
        #     db.child('Items').child("gun").child(str(ctx.author.id)).set({'amount':1})
        # else:

        await ctx.send(f"Vote for the bot at : https://top.gg/bot/805430097426513941/vote")
    @commands.command(name="invite")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _invite(self,ctx):
        await ctx.send(f"Invite the Bot: https://top.gg/bot/805430097426513941")
    @commands.command(name="report",aliases=["bug"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def report(self,ctx,*,bug):
        em = discord.Embed(title="New Bug",description=bug,color=discord.Color.red(),timestamp=datetime.utcnow())
        em.add_field(name="Reported By:",value=f'{ctx.author.name}#{ctx.author.discriminator}')
        em.add_field(name="Reporter's ID:",value=f'{ctx.author.id}')
        em.add_field(name="From Guild:",value=f"{ctx.guild.id}")
        em.add_field(name="Guild Name:",value=f"{ctx.guild.name}")
        em.set_thumbnail(url=ctx.guild.icon_url)
        await self.bot.get_channel(828543394225324032).send(embed=em)
        await ctx.send("Bug report sent successfully. Thank you its appreciated.")
    @commands.command(name="pokedex",aliases=["pokesearch","pokemon"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def _pokedex(self,ctx,*,query):
        api_url = f"https://api2.snowflakedev.xyz/api/pokemon?name={query}"
        response = requests.get(api_url,headers={"query":str(query),"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"}).content.decode()
        r = json.loads(response)
        em = discord.Embed(title=f"{query}'s info",color=discord.Color.random()).set_thumbnail(url=r["image"])
        em.add_field(name="Name:",value=r["name"])
        em.add_field(name="ID:",value=r["id"])
        em.add_field(name='Type:',value=r["type"])
        em.add_field(name=":triangular_ruler: Height:",value=r["height"],inline=False)
        em.add_field(name=":scales: Weight:",value=r["weight"],inline=False)
        moves_list = r["moves"]
        if len(moves_list)>16:
            new_moves_list = moves_list[:15]
        else:
            new_moves_list = moves_list    
        moves = ""
        for i in new_moves_list:
            if moves == "":
                moves += f"`{i}`"
            else:
                moves += f", `{i}`"
        em.add_field(name="Moves:",value=moves)
        await ctx.send(embed=em)
        #print(r)
    @commands.command(name="weather",aliases=["temp","forecast"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _weather(self,ctx,*,place:str):
        if place is None:
            place = "delhi"
        url = f"http://api.openweathermap.org/data/2.5/weather?appid=1835f9064d23b2112f17339c8209e24e&q={place}"
        r = requests.get(url).json()
        if r["cod"] != 404:
            y = r["main"]
            current_temp = round(y["temp"]-273)
            #current_pressure = y['pressure']
            current_humidity = y["humidity"]
            desc = r["weather"][0]["description"]
            em = discord.Embed(title=f"Weather forecast for: `{place}`",description=f":thermometer: Temprature: `{current_temp}°C`\n:cloud_rain: Humidity: `{current_humidity}%`\nOverall : `{desc}`",color=discord.Color.random())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="City not found",color=discord.Color.red())
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Utility(bot,difficulty))
