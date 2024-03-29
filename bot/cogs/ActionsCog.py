import discord
from discord.ext import commands
import random
import requests
import json
from .Listeners import AllListeners
import os

api_key = os.getenv('TENOR_API_KEY')
lmt = 50

class ActionCog(commands.Cog,name=":hugging: **Action Commands**"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="slap")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _slap(self,ctx,user:discord.Member):
        """
        This command is used to slap someone.
        """
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
        
    @commands.command(name="punch")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _punch(self,ctx,user:discord.Member):
        """
        Punch the mentioned User
        """
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
        
    @commands.command(name="lick",aliases=["suck"])
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _lick(self,ctx,user:discord.Member):
        """
        Sends lick gif for the mentioned User
        """
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

    @commands.command(name="bite")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _bite(self,ctx,user:discord.Member):
        """
        Bite the mentioned User
        """
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
    
    @commands.command(name="bully")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _bully(self,ctx,user:discord.Member):
        """
        Bully the mentioned User
        """
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
            
    @commands.command(name="hug")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _hug(self,ctx,user:discord.Member):
        """
        Hug the mentioned User
        """
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
   

    @commands.command(name="kick",aliases=["laat"])
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _kick(self,ctx,user:discord.Member):
        """
        Kick the mentioned User
        """
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
            
        
    @commands.command(name="hardkick")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _hardkick(self,ctx,user:discord.Member):
        """
        Hardkick the mentioned User
        """
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
    
    @commands.command(name="pat")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _pat(self,ctx,user:discord.Member):
        """
        Pat the mentioned User
        """
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-pat', api_key, lmt))
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            top_8gifs = json.loads(r.content)
            random_gif = random.randint(0,len(top_8gifs['results'])-1)
            #print ()
            link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
            em = discord.Embed(color=discord.Color.random())
            em.set_author(name=f"{ctx.author.name} pats {user.name}. :3 They are now cheered up.",icon_url=f"{ctx.author.avatar_url}")
            em.set_image(url=f'{str(link)}')
            await ctx.send(embed=em)
        else:
            top_8gifs = None
    @commands.command(name="kiss")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _kiss(self,ctx,user:discord.Member):
        """
        Kiss the mentioned User
        """
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-kiss', api_key, lmt))
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            top_8gifs = json.loads(r.content)
            random_gif = random.randint(0,len(top_8gifs['results'])-1)
            #print ()
            link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
            em = discord.Embed(color=discord.Color.random())
            em.set_author(name=f"{ctx.author.name} kisses {user.name}. :3",icon_url=f"{ctx.author.avatar_url}")
            em.set_image(url=f'{str(link)}')
            await ctx.send(embed=em)
        else:
            top_8gifs = None
    @commands.command(name="spank")
    @commands.guild_only()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    async def _spank(self,ctx,user:discord.Member):
        """
        Spank the mentioned User
        """
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime-spank', api_key, lmt))
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            top_8gifs = json.loads(r.content)
            random_gif = random.randint(0,len(top_8gifs['results'])-1)
            #print ()
            link = top_8gifs['results'][random_gif]['media'][0]['mediumgif']['url']
            em = discord.Embed(color=discord.Color.random())
            em.set_author(name=f"{ctx.author.name} spanks {user.name}. Ouch!",icon_url=f"{ctx.author.avatar_url}")
            em.set_image(url=f'{str(link)}')
            await ctx.send(embed=em)
        else:
            top_8gifs = None
    
def setup(bot):
    bot.add_cog(ActionCog(bot))
