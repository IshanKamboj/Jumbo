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
    #---------------------Fight Command and its errors---------------------------------------
    @commands.command(name="fight",aliases=["dumbfight"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _fight(self,ctx:commands.Context,user:discord.Member):
        db = firebase.database()
        a = random.choice(ctx.author,user)
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
                
    @_fight.error
    async def fight_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.fight_embed()
            await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)

    #---------------------Shoot Command and its errors---------------------------------------           
    @commands.command(name="shoot",aliases=["fire","headshot","kill"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _shoot(self,ctx:commands.Context,user:discord.Member):
        db = firebase.database()
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
 
    @_shoot.error
    async def shoot_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            em = HelpEmbeds.shoot_embed()
            await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)
    @commands.command(name="train",aliases=["learn"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def _train(self,ctx):
        db = firebase.database()
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

    @commands.command(name="profile")
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _profile(self,ctx):
        db = firebase.database()
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

    
    @commands.command(name="shop",aliases=["items","item"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _shop(self,ctx):
        db = firebase.database()
        em = discord.Embed(title=":shopping_cart: Welcome to Shop.",description="Buy items from shop and increase your winning chances.",color=discord.Color.random())
        for i in shop:
            item = i["item"]
            price = i["price"]
            value = i["value"]
            em.add_field(name=f"{item} ---- `{price} Points.`",value=f"{value}",inline=False)
        await ctx.send(embed=em)
    @commands.command(name="buy",aliases=["acquire","get"])
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _buy(self,ctx,item:str,amount=1):
        db = firebase.database()
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

def setup(bot):
    bot.add_cog(fights(bot))