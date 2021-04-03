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
from .Listeners import AllListeners
import wikipedia
shop = [
    {
        "item":":boxing_glove: **Boxing Glove**",
        "price":100,
        "value":"Increases your winning chances."
    },
    {
        "item":":gun: **Gun**",
        "price":200,
        "value":"It is used to shoot someone. You need to have a gun if u wanna shoot someone."
    }

]
glove_alias = ["glove","boxing glove","boxing"]
gun_alias = ["gun","pistol"]

class Utility(commands.Cog):
    def __init__(self,bot,difficulty):
        self.bot = bot
        self.difficulty = difficulty

    #---------------------level Command and its errors---------------------------------------
    @commands.command(name = "level", aliases = ["lvl","rank","rnk"])
    async def _level(self,ctx:commands.Context,*,user=""):
        """Check ur Level with this.        
        Mention ur friend or use his ID to see their level.
        """
        database = firebase.database()
        isEnabled = database.child('Disabled').child(str(ctx.guild.id)).child("level").get()
        if isEnabled.val() is None:
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
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)



#---------------------leaderboard Command and its errors---------------------------------------
    @commands.command(name="leaderboard",aliases=["lb","leader","top"])
    async def _leaderboard(self,ctx:commands.Context):
        database = firebase.database()
        isEnabled = database.child('Disabled').child(str(ctx.guild.id)).child("leaderboard").get()
        if isEnabled.val() is None:
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
            await ctx.send(embed=leaderboard_embed)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
        





#---------------------AFK Command and its errors---------------------------------------
    @commands.command(name="afk")
    # @commands.has_permissions(manage_nickname)
    async def _afk(self,ctx:commands.Context,*,reason="Busy...smh"):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("afk").get()
        if isEnabled.val() is None:
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
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)

    @_afk.error
    async def afk_error(self,ctx,error):
        pass


#---------------------------Last seen command---------------------
    @commands.command(name="seen",aliases=["lastseen","last"])
    async def _seen(self,ctx:commands.Context,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("seen").get()
        if isEnabled.val() is None:
            lastMsg = None
            fetchMsg = await ctx.channel.history(limit=350).find(lambda m: m.author.id == user.id)
            if fetchMsg is None:
                em = discord.Embed(description=f"**No message found from the author `{user.name}`. The last message by the author may be very old.**",color=discord.Color.random())
                await ctx.send(embed=em) 
            a = ctx.message.created_at
            b = fetchMsg.created_at
            c = a-b
            total_min = round((c.total_seconds())/60)
            temp = 0
            while total_min >= 60:
                total_min -= 60
                temp += 1
            minutes = total_min-temp*(60)
            
            if temp == 0:
                em = discord.Embed(description=f"**`{user.name}` was last seen `{minutes} minutes` ago in this channel.**",color=discord.Color.random())
                await ctx.send(embed=em)
            else:
                em = discord.Embed(description=f"**`{user.name}` was last seen more than `{temp} hours` ago in this channel.**",color=discord.Color.random())
                await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)

    @_seen.error
    async def seen_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = HelpEmbeds.seen_embed()
            await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)
        










#------------------------ Custom auto react------------------------------------------
    @commands.command(name="autoreact",aliases=["ar","react","reaction"])
    async def _autoreact(self,ctx,*,reaction):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("autoreact").get()
        if isEnabled.val() is None:
            react_data = db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).get()
            if react_data is None:
                db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).set({'Reaction':reaction})
                em = discord.Embed(title="Custom Reaction added",description=f"{reaction} was added as an auto react for you {ctx.author.mention}. Reaction will be added when u are mentioned",color=discord.Color.random())
                await ctx.send(embed=em)
            elif react_data is not None:
                db.child('Reactions').child(str(ctx.guild.id)).child(str(ctx.author.id)).update({'Reaction':reaction})
                em = discord.Embed(title="Custom Reaction updated",description=f"{reaction} was updated as your auto react {ctx.author.mention}. Reaction will be added when u are mentioned",color=discord.Color.random())
                await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    
    @_autoreact.error
    async def autoreact_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.autoreact_embed()
            await ctx.send(f"**Missing required arguments. See help** :point_down::point_down:",embed=em)


    @commands.command(name="train",aliases=["learn"])
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def _train(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(str(ctx.command)).get()
        if isEnabled.val() is None:
            x = db.child('FightPoints').child(str(ctx.author.id)).get()
            if x.val() is None:
                points = random.randint(0,11)
                db.child('FightPoints').child(str(ctx.author.id)).set({'points':points})
                em = discord.Embed(description=f"You were give {points} points for your first training.",color=ctx.author.color)
                await ctx.send(embed=em)
            elif x.val() is not None:
                check = x.val()["points"]
                if int(check) == 100:
                    await ctx.send(f"{ctx.author.mention} **You have trained enough...... Go and fight to gain more points.**")
                else:
                    points = random.randint(0,9)
                    temp = x.val()["points"]
                    db.child('FightPoints').child(str(ctx.author.id)).update({'points':points+temp})
                    em = discord.Embed(description=f"**You were give {points} points for your training.**\n**Your total points now are:** `{points+temp}`",color=ctx.author.color)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)

    @_train.error
    async def train_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            if time >= 3600:
                finalTime= round(time/3600)
                em = discord.Embed(title="Take a hold of yourself",description=f"You can't train without taking a rest. You need to wait **{finalTime} hours** before training again.",color=discord.Color.random())
            elif time < 3600:
                finalTime = round(time/60)
                em = discord.Embed(title="Take a hold of yourself",description=f"You can't train without taking a rest. You need to wait **{finalTime} minutes** before training again.",color=discord.Color.random())
            #print(finalTime)
            await ctx.send(embed=em)

    @commands.command(name="profile")
    async def _profile(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(str(ctx.command)).get()
        if isEnabled.val() is None:
            x = db.child('FightPoints').child(str(ctx.author.id)).get()
            item_glove = db.child('Items').child("gloves").child(str(ctx.author.id)).get()
            item_gun = db.child('Items').child("gun").child(str(ctx.author.id)).get()
            if x.val() is not None:
                pts = x.val()["points"]
            else:
                pts = 0
            em = discord.Embed()
            em.set_author(name=f"{ctx.author.name}'s profile",icon_url=f"{ctx.author.avatar_url}")
            em.add_field(name=f"**Fight Points:**",value=f":boxing_glove: **`{pts}`**")
            if item_glove is None and item_gun is None:
                em.add_field(name="**Items**",value="None",inline=False)
            elif item_glove is not None and item_gun is not None:
                amt_glove = item_glove.val()["amount"]
                amt_gun = item_gun.val()["amount"]
                em.add_field(name="**Items**",value="Here are all the items you own. These items might break after use.",inline=False)
                em.add_field(name=":boxing_glove: **Boxing Glove**",value=f"{amt_glove}",inline=True)
                em.add_field(name=":gun: **Gun**",value=f"{amt_gun}",inline=True)
            elif item_glove is not None and item_gun is None:
                amt_glove = item_glove.val()["amount"]
                em.add_field(name="**Items**",value="Here are all the items you own. These items might break after use.",inline=False)
                em.add_field(name=":boxing_glove: **Boxing Glove**",value=f"{amt_glove}")
            elif item_glove is None and item_gun is not None:
                amt_gun = item_gun.val()["amount"]
                em.add_field(name="**Items**",value="Here are all the items you own. These items might break after use.",inline=False)
                em.add_field(name=":gun: **Gun**",value=f"{amt_gun}")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
        

    
    @commands.command(name="shop",aliases=["items","item"])
    async def _shop(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(str(ctx.command)).get()
        if isEnabled.val() is None:
            em = discord.Embed(title=":shopping_cart: Welcome to Shop.",description="Buy items from shop and increase your winning chances.",color=discord.Color.random())
            for i in shop:
                item = i["item"]
                price = i["price"]
                value = i["value"]
                em.add_field(name=f"{item} ---- `{price} Points.`",value=f"{value}",inline=False)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @commands.command(name="buy",aliases=["acquire","get"])
    async def _buy(self,ctx,item:str,amount=1):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(str(ctx.command)).get()
        if isEnabled.val() is None:
            if item in glove_alias:
                for i in shop:
                    if i["item"] == ":boxing_glove: **Boxing Glove**":
                        temp = i
                        item_name = "gloves"
                        itemDB = db.child('Items').child("gloves").child(str(ctx.author.id)).get()
            elif item in gun_alias:
                for i in shop:
                    if i["item"] == ":gun: **Gun**":
                        temp = i
                        item_name = "gun"
                        itemDB = db.child('Items').child("gun").child(str(ctx.author.id)).get()
            else:
                await ctx.send(f"{ctx.author.mention} You stupid or what?! No item named : {item} in the shop.")
            
            user_pts = db.child('FightPoints').child(str(ctx.author.id)).get()
            i = temp["item"]

            if int(user_pts.val()["points"]) >= temp["price"]*amount:
                x = int(user_pts.val()["points"])
                final = x-temp["price"]*amount
                db.child('FightPoints').child(str(ctx.author.id)).update({"points":final})
                if itemDB.val() is None:
                    db.child("Items").child(item_name).child(str(ctx.author.id)).set({"amount":amount})
                elif itemDB.val() is not None:
                    previous_amt = itemDB.val()["amount"]
                    db.child("Items").child(item_name).child(str(ctx.author.id)).update({"amount":amount+previous_amt})
                pts_given = temp["price"]*amount
                await ctx.send(f"**You successfully bought {amount}** {i} **after giving {pts_given} points. Now you have {final} points left.**")
            elif int(user_pts.val()["points"]) < temp["price"]*amount:
                await ctx.send("Sorry you don't have enough points to buy this item.")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
        
    @commands.command(name="google",aliases=["search","find"])
    async def _google(self,ctx,*,query):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            temp = {}
            for j in search(query,tld="co.in" ,num=6,start=0, stop=7, pause=0.5): 
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
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
        # print(desc)
        # print(temp)

    @commands.command(name="wikisearch",aliases=["wsearch","wikipedia"])
    @commands.check(AllListeners.check_enabled)
    async def _wikisearch(self,ctx,*,query:str):
        try:
            x = wikipedia.summary(query,sentences=7)
            pg = wikipedia.page(query)
            link = pg.url
            
            await ctx.send(f"**{x}**\n More info can be found here: {link}")
        except Exception as e:
            print(str(e))
    
    @commands.command(name="poll")
    @commands.check(AllListeners.check_enabled)
    async def _poll(self,ctx,*,question:str):
        try:
            msg = await ctx.send(f'**{str(ctx.author)} asks** {question}')
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except Exception as e:
            print(str(e))
    