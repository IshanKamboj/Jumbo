import discord
from discord.ext import commands
from Database.db_files import firebase
from .Listeners import AllListeners
import asyncio
import random

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

class fights(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
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

    @commands.command(name="profile")
    @commands.cooldown(1, 7, commands.BucketType.user)
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
    @commands.cooldown(1, 7, commands.BucketType.user)
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
    @commands.cooldown(1, 7, commands.BucketType.user)
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