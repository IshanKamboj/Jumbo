import discord
from discord.ext import commands
import json
from .Listeners import AllListeners
import requests,json
from helpEmbeds import HelpEmbeds
import math

class Calculations(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.group(invoke_without_command=True)
    @commands.check(AllListeners.check_enabled)
    @commands.cooldown(1, 7, commands.BucketType.user)
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
    
    @commands.group(invoke_without_command=True)
    @commands.check(AllListeners.check_enabled)
    async def volume(self,ctx):
        await ctx.send(embed=HelpEmbeds.volume_embed())
    
    @volume.command(name='cube')
    @commands.check(AllListeners.check_enabled)
    async def _cube(self,ctx,side:float):
        volume = side**3
        csa = 4*(side**2)
        tsa = 6*(side**2)
        volume = round(volume,3)
        csa = round(csa,3)
        tsa = round(tsa,3)
        em = discord.Embed(title="Volume of Cube",color=discord.Color.random())
        em.add_field(name='Dimensions:',value=side,inline=False)
        em.add_field(name='Volume:',value=volume,inline=False)
        em.add_field(name='CSA:',value=csa,inline=False)
        em.add_field(name='TSA:',value=tsa,inline=False)
        await ctx.send(embed=em)
    
    @volume.command(name='cuboid')
    @commands.check(AllListeners.check_enabled)
    async def _cuboid(self,ctx,*,dimensions:str):
        try:
            l,b,h = dimensions.split(',')
            l = float(l)
            b = float(b)
            h = float(h)
            volume = l*b*h
            csa = 2*h*(l+b)
            tsa = 2*((l*b)+(b*h)+(h*l))
            volume = round(volume,3)
            csa = round(csa,3)
            tsa = round(tsa,3)
            em = discord.Embed(title="Volume of Cuboid",color=discord.Color.random())
            em.add_field(name='Dimensions:',value=f"{l}x{b}x{h}",inline=False)
            em.add_field(name='Volume:',value=volume,inline=False)
            em.add_field(name='CSA:',value=csa,inline=False)
            em.add_field(name='TSA:',value=tsa,inline=False)
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(f'Error! :{str(e)}')
    
    @volume.command(name='sphere')
    @commands.check(AllListeners.check_enabled)
    async def _sphere(self,ctx,radius:float):
        try:
            volume = (4/3*22/7)*(radius**3)
            volume = round(volume,3)
            tsa = 4*22/7*(radius**2)
            tsa = round(tsa,2)
            em = discord.Embed(title="Volume of Sphere",color=discord.Color.random())
            em.add_field(name='Dimensions:',value=radius,inline=False)
            em.add_field(name='Volume:',value=volume,inline=False)
            em.add_field(name='CSA:',value=tsa,inline=False)
            em.add_field(name='TSA:',value=tsa,inline=False)
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(f'Error! :{str(e)}')
    
    @volume.command(name='hemisphere')
    @commands.check(AllListeners.check_enabled)
    async def _hemisphere(self,ctx,radius:float):
        try:
            volume = (2/3*22/7)*(radius**3)
            volume = round(volume,3)
            tsa = 3*22/7*(radius**2)
            tsa = round(tsa,3)
            csa = 2*22/7*(radius**2)
            csa = round(csa,3)
            em = discord.Embed(title="Volume of Hemi-Sphere",color=discord.Color.random())
            em.add_field(name='Dimensions:',value=radius,inline=False)
            em.add_field(name='Volume:',value=volume,inline=False)
            em.add_field(name='CSA:',value=csa,inline=False)
            em.add_field(name='TSA:',value=tsa,inline=False)
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(f'Error! :{str(e)}')
    
    @volume.command(name='cone')
    @commands.check(AllListeners.check_enabled)
    async def _cone(self,ctx,*,dimensions:str):
        try:
            radius,height = dimensions.split(',')
            radius = float(radius)
            height = float(height)
            l = math.sqrt((radius**2)+(height**2))
            l = round(l,2)
            volume = (2/3*22/7)*(radius**3)
            volume = round(volume,3)
            csa = 22/7*radius*l
            csa = round(csa,3)
            tsa = csa + 22/7*(radius**2)
            tsa = round(tsa,3)
            em = discord.Embed(title="Volume of Cone",color=discord.Color.random())
            em.add_field(name='Dimensions:',value=f'Radius: {radius}, Height: {height}',inline=False)
            em.add_field(name='Volume:',value=volume,inline=False)
            em.add_field(name='CSA:',value=csa,inline=False)
            em.add_field(name='TSA:',value=tsa,inline=False)
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(f'Error! :{str(e)}')
    
    @volume.command(name='cylinder')
    @commands.check(AllListeners.check_enabled)
    async def _cylinder(self,ctx,*,dimensions:str):
        try:
            radius,ht = dimensions.split(',')
            radius = float(radius)
            ht = float(ht)
            volume = 22/7*(radius**2)*ht
            tsa = 2*22/7*radius*(ht+radius)
            csa = 2*22/7*radius*ht
            volume = round(volume,3)
            csa = round(csa,3)
            tsa = round(tsa,3)
            em = discord.Embed(title="Volume of Cylinder",color=discord.Color.random())
            em.add_field(name='Dimensions:',value=f'Radius:{radius}, Height:{ht}',inline=False)
            em.add_field(name='Volume:',value=volume,inline=False)
            em.add_field(name='CSA:',value=csa,inline=False)
            em.add_field(name='TSA:',value=tsa,inline=False)
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(f'Error! :{str(e)}')
        
    @commands.command(name="factorial")
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.check(AllListeners.check_enabled)
    async def _factorial(self,ctx,number:int):
        factorials = math.factorial(number)
        em = discord.Embed(title="Factorial",description=f"**{number}! == {factorials}**    ",color=discord.Color.random())
        await ctx.send(embed=em)
        
def setup(bot):
    bot.add_cog(Calculations(bot))