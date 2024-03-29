import random
import discord 
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .Listeners import AllListeners
from io import BytesIO
import io
import aiohttp
from waifu import WaifuClient
import datetime
import requests
from jikanpy import Jikan
import asyncio
from Database.db_files import firebase
class ImageCommands(commands.Cog,name=":camera: **Image Commands**"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="wanted")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _wanted(self,ctx, user:discord.Member=None):
        """
        Returns a wanted image of someone.
        """
        if user is None:
            user = ctx.author
        wanted = Image.open('template_imgs/wanted.jpg')
        width, height = wanted.size
        asset = user.avatar_url
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((300,300))
        d = ImageDraw.Draw(wanted)
        font = ImageFont.truetype(font='fonts/wanted.otf',size=35)
        w,h = d.textsize(user.name,font=font)
        posX = (width-w)/2
        d.text((posX,500),user.name,fill=(0,0,0),font=font)
        wanted.paste(pfp, (100,180))
        with io.BytesIO() as image_binary:
            wanted.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        # wanted.save('wanted_img.jpg')
        # await ctx.send(file=discord.File('wanted_img.jpg'))
    
    @commands.command(name="rip")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _rip(self,ctx,user:discord.Member=None):
        """
        This command returns a RIP image of someone.
        """
        if user == None:
            user = ctx.author
        tomb = Image.open('template_imgs/tomb.jpg')
        width, height = tomb.size
        d = ImageDraw.Draw(tomb)
        font = ImageFont.truetype(font='fonts/Roboto-Bold.ttf',size=38)
        #width, height = wanted.size
        asset = user.avatar_url
        date_format = "%a, %d %b %Y "
        #d.text(())
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((150,150))
        w,h = d.textsize(user.name,font=font)
        posX = (width-w)/2
        d.text((posX,440),f'{user.name}',fill=(204,0,102),font=font)
        tomb.paste(pfp,(100,290))
        with io.BytesIO() as image_binary:
            tomb.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    # https://source.unsplash.com/1600x900/?nature,water
    @commands.command(name="wallpaper",aliases=["wall"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _wallpaper(self,ctx,query:str=None):
        """
        This command returns a random 1080p image for wallpaper.
        """
        if query == None:
            url = 'https://source.unsplash.com/random/1920x1080'
        else:
            url = f'https://source.unsplash.com/1920x1080/?{query}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'cool_image.png'))
    @commands.command(name="trash",aliases=['garbage'])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _trash(self,ctx,user:discord.Member=None):
        """
        Generates a trash image of user.
        """
        if user == None:
            user = ctx.author
        trash = Image.open("template_imgs/trash.jpg")
        d = ImageDraw.Draw(trash)
        asset = user.avatar_url
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((190,190))
        trash.paste(pfp,(265,580))
        with io.BytesIO() as image_binary:
            trash.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    @commands.command(name="waifu",aliases=["waifus","waif"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _waifu(self,ctx):
        """
        Return a waifu image depending on your luck
        """
        t = random.randint(1,100)
        #perm_simp = [752492486714327131,576442029337477130, 536444230659342337]
        db = firebase.database()
        x = db.child('PermanentSimp').get()
        if x.val() is not None:
            if ctx.author.id in x.val()['Ids']:
                t = 100
        if t >= 60:
            client = WaifuClient()
            x = client.sfw(category='waifu')
            em = discord.Embed(title="Oh Yeah! You got a waifu",description=f"[Download]({x})",color=discord.Color.blurple())
            em.set_image(url=x)
            em.set_footer(text=f"Invoked by: {ctx.author.name}#{ctx.author.discriminator}",icon_url=f'{ctx.author.avatar_url}')
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em)
        elif t < 60:
            em = discord.Embed(title="Uh Oh!",description=f"You weren't lucky enough to get a waifu. Luck percent: {t}%",color=discord.Color.dark_orange())
            em.timestamp = datetime.datetime.utcnow()
            em.set_footer(text=f"Invoked by: {ctx.author.name}#{ctx.author.discriminator}",icon_url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=em)
    
    @commands.command(name="grayscale",aliases=["gray",'gscal'])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _grayscale(self,ctx,link:str):
        """
        Return an image in grayscale
        """
        link = link.replace("<","")
        link = link.replace(">","")
        x = Image.open(requests.get(link, stream=True).raw)
        y = x.convert("L")
        with io.BytesIO() as image_binary:
            y.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    @commands.command(name="emboss")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _emboss(self,ctx,link:str):
        """
        Return an image with an emboss filter.
        """
        link = link.replace("<","")
        link = link.replace(">","")
        x = Image.open(requests.get(link, stream=True).raw)
        y = x.filter(ImageFilter.EMBOSS)
        with io.BytesIO() as image_binary:
            y.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    
    @commands.command(name="cat",aliases=["catpic","catpicture"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _catpic(self,ctx):
        """
        Returns a cat picture
        """
        # url = "https://api2.snowflakedev.xyz/api/cat"
        # x = Image.open(requests.get(url=url,headers={"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"},stream=True).raw)
        # with io.BytesIO() as image_binary:
        #     x.save(image_binary,"PNG")
        #     image_binary.seek(0)
        #     await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        url = "https://api.thecatapi.com/v1/images/search"
        async with aiohttp.request("GET",url) as r:
            r = await r.json()
        #r = requests.get(url=url).json()
        final_url = r[0]['url']
        x = Image.open(requests.get(final_url,stream=True).raw)
        with io.BytesIO() as image_binary:
            x.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(name="dog",aliases=["dogpic","dogpicture"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _dog(self,ctx):
        """
        Returns a dog picture
        """
        url = "https://random.dog/woof.json"
        async with aiohttp.request("GET",url) as r:
            r = await r.json()
        final_url = r['url']
        #print(r)
        x = Image.open(requests.get(final_url,stream=True).raw)
        with io.BytesIO() as image_binary:
            x.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    
    @commands.command(name="character",aliases=["animechar","animecharacter","achar"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)        
    async def _character(self,ctx,*,query:str):
        """
        Returns images of character of anime.
        """
        jikan = Jikan()
        url = f"https://api.jikan.moe/v3/search/character?q={query}"
        async with aiohttp.request("GET",url) as r:
            search_result = await r.json()
        x = 0
        pages = len(search_result["results"])
        results = search_result['results'][x]
        #print(results)
        # id_ = results['mal_id']
        # d = jikan.character(id_)
        img_url = results['image_url']
        name = results['name']
        em = discord.Embed(title=name,color=discord.Color.random()).set_image(url=img_url).set_footer(text=f"Page: {x+1}/{pages}")
        msg = await ctx.send(embed=em)
        buttons = ["⬅️","⏹️","➡️"]
        for i in buttons:
            await msg.add_reaction(i)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add",check=lambda reaction, user: user == ctx.author and not user.bot and reaction.emoji in buttons, timeout=20.0)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            else:
                if reaction.emoji == "⬅️" and x > 0:
                    x -= 1
                elif reaction.emoji == "➡️" and x < len(search_result["results"]):
                    x += 1
                elif reaction.emoji == "⏹️":
                    await msg.clear_reactions()
                    break
                for button in buttons:
                    await msg.remove_reaction(button,ctx.author)
                results = search_result['results'][x]
                img_url = results['image_url']
                name = results['name']
                em = discord.Embed(title=name,color=discord.Color.random()).set_image(url=img_url).set_footer(text=f"Page: {x+1}/{pages}")
                await msg.edit(embed=em)
    @commands.command(name="fox",aliases=["foxpic","foxpicture"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _fox(self,ctx):
        """
        Returns a fox picture
        """
        url = "https://api.snowflake107.repl.co/api/fox"
        x = Image.open(requests.get(url=url,headers={"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"},stream=True).raw)
        with io.BytesIO() as image_binary:
            x.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    @commands.command(name="wasted")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _wasted(self,ctx,user:discord.Member=None):
        """
        Returns an image with GTA style wasted filter
        """
        if user == None:
            user = ctx.author
        pfp = Image.open(requests.get(url=user.avatar_url,stream=True).raw)
        pfp = pfp.convert("RGBA")
        img = Image.open("template_imgs/wasted2.png")
        img = img.resize(pfp.size)
        pfp.paste(img,(0,0),img)
        draw = ImageDraw.Draw(img)
        draw.rectangle(((0, 0), pfp.size), fill=(109,51,54,130))
        image = Image.alpha_composite(pfp, img)
        with io.BytesIO() as image_binary:
            image.save(image_binary,"PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
def setup(bot):
    bot.add_cog(ImageCommands(bot))
