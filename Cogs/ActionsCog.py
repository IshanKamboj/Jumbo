import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
import random
from Database.db_files import firebase
import asyncio
from helpEmbeds import HelpEmbeds
import requests
import json
from .Listeners import AllListeners
import os

api_key = os.getenv('TENOR_API_KEY')
lmt = 50

class ActionCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="slap")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _slap(self,ctx,user:discord.Member):
            try:
                r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-slap', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print (random_gif)
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} slaps {user.name}. Ouch! It looks like it hurts.",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
        
    @_slap.error
    async def slap_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    @commands.command(name="punch")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _punch(self,ctx,user:discord.Member):
            try:
                x = random.randint(0,10)
                if x == 1:
                    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('eren-kick', api_key, 1))
                else:
                    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-punch', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} slams {user.name}. It really hit them.",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
        
    @_punch.error
    async def punch_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    @commands.command(name="lick",aliases=["suck"])
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _lick(self,ctx,user:discord.Member):
            try:
                r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-lick', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} licks {user.name}!!. How does it taste?!.",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
    @_lick.error
    async def lick_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    @commands.command(name="bite")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _bite(self,ctx,user:discord.Member):
            try:
                r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-bite', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} gives {user.name} a bite. Yummy~",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
        
    @_bite.error
    async def bite_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    @commands.command(name="bully")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _bully(self,ctx,user:discord.Member):
            try:
                r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-bully', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} bullies {user.name}. >:3",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
    @_bully.error
    async def bully_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    @commands.command(name="hug")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _hug(self,ctx,user:discord.Member):
            try:
                r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-hug', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} hugs {user.name}.",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))

    @_hug.error
    async def hug_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)    

    @commands.command(name="kick",aliases=["laat"])
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _kick(self,ctx,user:discord.Member):
            try:
                x = random.randint(0,10)
                if x == 1:
                    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('levi-kick', api_key, 1))
                else:
                    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-kick', api_key, lmt))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} kick {user.name}. >:3. Ouch! it hit very hard",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
        
    @_kick.error
    async def kick_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    @commands.command(name="hardkick")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _hardkick(self,ctx,user:discord.Member):
            try:
                r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('levi-kick', api_key, 8))
                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content)
                    random_gif = random.randint(0,len(top_8gifs['results'])-1)
                    #print ()
                    link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                    em = discord.Embed(color=discord.Color.random())
                    em.set_author(name=f"{ctx.author.name} hard kicks {user.name}. >:3. Ouch! it hit very very hard",icon_url=f"{ctx.author.avatar_url}")
                    em.set_image(url=f'{str(link)}')
                    await ctx.send(embed=em)
                else:
                    top_8gifs = None
            except Exception as e:
                print(str(e))
    @_hardkick.error
    async def hardkick_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)
    
    @commands.command(name="pat")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _pat(self,ctx,user:discord.Member):
        try:
            r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-pat', api_key, lmt))
            if r.status_code == 200:
                # load the GIFs using the urls for the smaller GIF sizes
                top_8gifs = json.loads(r.content)
                random_gif = random.randint(0,len(top_8gifs['results'])-1)
                #print ()
                link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
                em = discord.Embed(color=discord.Color.random())
                em.set_author(name=f"{ctx.author.name} pats {user.name}. :3 He's now cheered up.",icon_url=f"{ctx.author.avatar_url}")
                em.set_image(url=f'{str(link)}')
                await ctx.send(embed=em)
            else:
                top_8gifs = None
        except Exception as e:
            print(str(e))
    
    @_pat.error
    async def pat_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            em = discord.Embed(title="Hold your Horses",description=f"This command has a cooldown of `5` seconds. Wait **{time} seconds** to use it again.")   
            await ctx.send(embed=em)