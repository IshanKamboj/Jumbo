import discord
from discord.ext import commands
import json
from .Listeners import AllListeners
import requests,json
from helpEmbeds import HelpEmbeds

class Calculations(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.group(invoke_without_command=True)
    @commands.check(AllListeners.check_enabled)
    async def area(self,ctx):
        await ctx.send(embed=HelpEmbeds.area_embed())
    
    @area.command(name="triangle")
    @commands.check(AllListeners.check_enabled)
    async def _triangle(self,ctx,*,dimensions:str):
        ht,bs = dimensions.split(',')
        ht = int(ht)
        bs = int(bs)
        area = 1/2*(ht)*(bs)
        await ctx.send(f"The area of the triangle would be: **{area}**")
    
    @area.command(name="rectangle")
    @commands.check(AllListeners.check_enabled)
    async def _rectangle(self,ctx,*,dimensions:str):
        length,breadth = dimensions.split(',')
        length = int(length)
        breadth = int(breadth)
        area = 2*(length+breadth)
        await ctx.send(f"The area of the rectangle would be: **{area}**")
    
    @area.command(name="square")
    @commands.check(AllListeners.check_enabled)
    async def _square(self,ctx,dimensions:str):
        side = int(dimensions)
        area = side**2
        await ctx.send(f"The area of the square would be: **{area}**")
    
    @area.command(name="circle")
    @commands.check(AllListeners.check_enabled)
    async def _circle(self,ctx,dimensions:str):
        side = int(dimensions)
        area = 22/7*side**2
        await ctx.send(f"The area of the circle would be: **{area}**")