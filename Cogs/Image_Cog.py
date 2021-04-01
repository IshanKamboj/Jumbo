import discord 
from discord.ext import commands
import PIL
from PIL import Image, ImageDraw, ImageFont
from .Listeners import AllListeners
from io import BytesIO
from datetime import datetime
class ImageCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="wanted")
    @commands.check(AllListeners.check_enabled)
    async def _wanted(self,ctx, user:discord.Member=None):
        if user is None:
            user = ctx.author
        wanted = Image.open('wanted.jpg')
        width, height = wanted.size
        asset = user.avatar_url
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((300,300))
        d = ImageDraw.Draw(wanted)
        font = ImageFont.truetype(font='wanted.otf',size=35)
        w,h = d.textsize(user.name,font=font)
        posX = (width-w)/2
        d.text((posX,500),user.name,fill=(0,0,0),font=font)
        wanted.paste(pfp, (100,180))
        wanted.save('wanted_img.jpg')
        await ctx.send(file=discord.File('wanted_img.jpg'))
    
    @commands.command(name="rip")
    async def _rip(self,ctx,user:discord.Member=None):
        try:
            if user == None:
                user = ctx.author
            tomb = Image.open('tomb.jpg')
            width, height = tomb.size
            d = ImageDraw.Draw(tomb)
            font = ImageFont.truetype(font='Roboto-Bold.ttf',size=38)
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
            tomb.save('RIP.jpg')
            await ctx.send(file=discord.File('RIP.jpg'))
        except Exception as e:
            print(str(e))

    