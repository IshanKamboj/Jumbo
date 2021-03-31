import discord
from discord.ext import commands
import asyncio
from Database.db_files import firebase
from colour import Color
from helpEmbeds import HelpEmbeds
from .Listeners import AllListeners

db = firebase.database()
class AdminCogs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed(description=f'{str(error)}',color=discord.Color.random())
        await ctx.send(embed=em)
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def role(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("role").get()
        if isEnabled.val() is None:
            await ctx.send(embed=HelpEmbeds.role_embed())
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @role.command(name="add")
    @commands.has_permissions(manage_roles=True)
    async def _addrole(self,ctx,user:discord.Member,role:discord.Role):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("role").get()
        if isEnabled.val() is None:
            Role = discord.utils.get(ctx.guild.roles,name=str(role))
            if not Role:
                em = discord.Embed(description=f"No role named : {str(role)} exists",color=discord.Color.random())
                await ctx.send(embed=em)
            elif Role in user.roles:
                em = discord.Embed(description=f"`{user.name}` **already has the role:** `{Role}`",color=discord.Color.random())
                await ctx.send(embed=em)
            else:
                list_roles = ctx.author.roles
                highest_role = list_roles[-1]
                if  highest_role >= role:
                    await user.add_roles(Role)
                    em = discord.Embed(description=f"**Gave role: `{Role}` to `{user.name}`**",color=role.color)
                    await ctx.send(embed=em)   
                else:
                    em = discord.Embed(description=f"**Error: You cannot give higher roles.**")
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @role.command(name="remove")
    @commands.has_permissions(manage_roles=True)
    async def _removerole(self,ctx,user:discord.Member,role:discord.Role):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("role").get()
        if isEnabled.val() is None:
            Role = discord.utils.get(ctx.guild.roles,name=str(role))
            if not Role:
                em = discord.Embed(description=f"No role named : {str(role)} exists",color=discord.Color.random())
                await ctx.send(embed=em)
            elif Role in user.roles:
                list_roles = ctx.author.roles
                highest_role = list_roles[-1]
                if  highest_role >= role:
                    await user.remove_roles(Role)
                    em = discord.Embed(description=f"**Removed role: `{Role}` from user: `{user.name}`**",color=discord.Color.random())
                    await ctx.send(embed=em)  
                else:
                    em = discord.Embed(description=f"**Error: You cannot remove higher roles.**")
                    await ctx.send(embed=em)
                
            else:
                em = discord.Embed(description=f"**User `{user.name}` does not have the role `{Role}`**",color=role.color)
                await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @role.command(name="create",aliases=["new"])
    @commands.has_permissions(manage_roles=True)
    async def create(self,ctx,role,hoist=False,mentionable=False):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("role").get()
        if isEnabled.val() is None:
            Role = discord.utils.get(ctx.guild.roles,name=str(role))
            if Role:
                em = discord.Embed(description=f"**Role `{role}` already exists**")
                await ctx.send(embed=em)
            else:
                await ctx.guild.create_role(name=f"{role}",hoist=hoist,mentionable=mentionable)
                em = discord.Embed(description=f"**Role created : `{role}`**\n**Role color:** #ffffff\n**Mentionable:** {mentionable}\n**Display seprately:** {hoist}")
                await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @role.command(name="color",aliases=["colour","looks"])
    @commands.has_permissions(manage_roles=True)
    async def color(self,ctx,role:discord.Role,color:discord.Color):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("role").get()
        if isEnabled.val() is None:
            await role.edit(color=color)
            em = discord.Embed(description=f"**Color of role: {role} changed.**")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
class UtilityCogs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="hex",aliases=["gethex"])
    async def _hex(self,ctx,*,color:str):
        c = Color(color=color)
        await ctx.send(f"The hex value for {color} color is: {c.hex_l}")