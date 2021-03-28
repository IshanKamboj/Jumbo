import discord
from discord.ext import commands
import datetime
from Database.db_files import firebase
import asyncio
class InfoCogs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.sniped_msgs = {}
    # async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
    #     if error == UnboundLocalError:
    #         pass
    #     else:
    #         em = discord.Embed(description=f'{str(error)}',color=discord.Color.random())
    #         await ctx.send(embed=em)
    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed(description=f'{str(error)}',color=discord.Color.random())
        await ctx.send(embed=em)
    @commands.command(name="userinfo",aliases=["ui"])
    async def _userinfo(self,ctx,user:discord.Member=None):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            if user is None:
                user = ctx.author      
            date_format = "%a, %d %b %Y %I:%M %p"
            embed = discord.Embed(color=0xdfa3ff, description=user.mention)
            embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="Joined Guild", value=user.joined_at.strftime(date_format))
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at) 
            embed.add_field(name="Server Position", value=str(members.index(user)+1))
            embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
            if len(user.roles) > 1:
                role_string = ' '.join([r.mention for r in user.roles][1:])
                embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
            perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
            embed.add_field(name="Guild permissions", value=perm_string, inline=False)
            embed.set_footer(text='ID: ' + str(user.id))
            await ctx.send(embed=embed)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    
    @commands.command(name="roleinfo",aliases=["ri","rinfo"])
    async def _roleinfo(self,ctx,role:discord.Role):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            date_format = "%a, %d %b %Y %I:%M %p"
            role_info = discord.utils.get(ctx.guild.roles,name=str(role))
            temp = [i for i in ctx.guild.roles]
            em = discord.Embed(title=f"{role_info}",color=role_info.color)
            em.add_field(name="**ID**",value=f"`{role_info.id}`")
            em.add_field(name="**Created at:**",value=f"`{role_info.created_at.strftime(date_format)}`")
            em.add_field(name="**Color**",value=f"`{role_info.color}`")
            em.add_field(name="**Position**",value=f"`{len(temp)-role_info.position}`")
            em.add_field(name="**Members**",value=f"`{len(role_info.members)}`")
            if role_info.hoist:
                em.add_field(name="**Hoist**",value=":white_check_mark:")
            else:
                em.add_field(name="**Hoist**",value=":x:")
            if role_info.mentionable:
                em.add_field(name="**Mentionable**",value=":white_check_mark:")
            else:
                em.add_field(name="**Mentionable**",value=":x:")
            await ctx.send(embed=em)
            #print()
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    
    @commands.command(name="onlineinfo",aliases=["online"])
    async def _onlineinfo(self,ctx,user:discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            if str(user.status) == "offline":
                await ctx.send(f'{user.name} is offline....... Please check about anyone else')
            if user.is_on_mobile():
                em = discord.Embed(title=f"{user.name}'s info of device.",description=":white_check_mark: Mobile\n:x: Web\n:x: Desktop",color=user.color)
            elif str(user.web_status) != "offline":
                em = discord.Embed(title=f"{user.name}'s info of device.",description=":x: Mobile\n:white_check_mark: Web\n:x: Desktop",color=user.color)
            elif str(user.desktop_status) != "offline":
                em = discord.Embed(title=f"{user.name}'s info of device.",description=":x: Mobile\n:x: Web\n:white_check_mark: Desktop",color=user.color)
            # print(user.web_status)
            # print(user.is_on_mobile())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)

    @commands.command(name="ping")
    async def _ping(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            lat = round((self.bot.latency)*1000)
            if lat < 150:
                em = discord.Embed(title=":ping_pong: | Pong!",description=f":green_circle: Current Latency : `{lat}`ms",color=discord.Color.green())
            elif lat >= 150:
                em = discord.Embed(title=":ping_pong: | Pong!",description=f":yellow_circle: Current Latency : `{lat}`ms",color=discord.Color.from_rgb(255,255,0))  
            else:
                em = discord.Embed(title=":ping_pong: | Pong!",description=f":red_circle: Current Latency : `{lat}`ms",color=discord.Color.red())
            await ctx.send(embed=em)
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @commands.command(name="avatar",aliases=["av","image","pfp"])
    async def _avatar(self,ctx,user:discord.Member=None):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            if user == None:
                user = ctx.author
            em = discord.Embed(description=f"[PNG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=1024) | [JPEG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpeg?size=1024) | [JPG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpg?size=1024)",color=discord.Color.random())
            em.set_author(name=f"{user.name}'s avatar",url=f"{user.avatar_url}")
            em.set_image(url=f"{user.avatar_url}")
            await ctx.send(embed=em)

        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self,payload):
        try:
            message = payload.cached_message
            self.sniped_msgs[message.channel.id] = (message.content,message.author,message.channel,message.created_at)
            # await asyncio.sleep(300)
            # del self.sniped_msgs[message.guild.id]
        except:
            pass
    @commands.command(name="snipe",aliases=["sniper"])
    async def _snipe(self,ctx,channel:discord.channel.TextChannel=None):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            try:
                if channel is None:
                    contents , author , channel , time = self.sniped_msgs[ctx.channel.id]
                else:
                    contents , author , channel , time = self.sniped_msgs[channel.id]
                em = discord.Embed(description = contents, color = discord.Color.random(), timestamp = time)
                em.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
                em.set_footer(text=f"Deleted in : #{channel}")
                await ctx.send(embed=em)
            except KeyError:
                await ctx.send("**`Nothing to Snipe ;)`**")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
