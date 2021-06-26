import discord
from discord.ext import commands
from datetime import timedelta

import requests
from Database.db_files import firebase
import asyncio
from platform import python_version
from time import time
from discord import __version__ as discord_version
from psutil import Process, virtual_memory, cpu_percent
from .Listeners import AllListeners
import psutil

class InfoCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped_msgs = {}
        self.editsnipe_msgs = {}
    # async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
    #     if error == UnboundLocalError:
    #         pass
    #     else:
    #         em = discord.Embed(description=f'{str(error)}',color=discord.Color.random())
    #         await ctx.send(embed=em)

    

    @commands.command(name="userinfo", aliases=["ui"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _userinfo(self, ctx, user: discord.Member = None):
        db = firebase.database()
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined Guild",
                        value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Server Position",
                        value=str(members.index(user)+1))
        embed.add_field(name="Registered",
                        value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(
                len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join(
            [str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions",
                        value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        await ctx.send(embed=embed)

    @commands.command(name="roleinfo", aliases=["ri", "rinfo"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _roleinfo(self, ctx, role: discord.Role):
        db = firebase.database()
        date_format = "%a, %d %b %Y %I:%M %p"
        role_info = discord.utils.get(ctx.guild.roles, name=str(role))
        temp = [i for i in ctx.guild.roles]
        em = discord.Embed(title=f"{role_info}", color=role_info.color)
        em.add_field(name="**ID**", value=f"`{role_info.id}`")
        em.add_field(name="**Created at:**",
                        value=f"`{role_info.created_at.strftime(date_format)}`")
        em.add_field(name="**Color**", value=f"`{role_info.color}`")
        em.add_field(name="**Position**",
                        value=f"`{len(temp)-role_info.position}`")
        em.add_field(name="**Members**",
                        value=f"`{len(role_info.members)}`")
        if role_info.hoist:
            em.add_field(name="**Hoist**", value=":white_check_mark:")
        else:
            em.add_field(name="**Hoist**", value=":x:")
        if role_info.mentionable:
            em.add_field(name="**Mentionable**",
                            value=":white_check_mark:")
        else:
            em.add_field(name="**Mentionable**", value=":x:")
        await ctx.send(embed=em)
            # print()

    @commands.command(name="onlineinfo", aliases=["online"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _onlineinfo(self, ctx, user: discord.Member):
        db = firebase.database()
        
        if str(user.status) == "offline":
            await ctx.send(f'{user.name} is offline....... Please check about anyone else')
            return
        if user.is_on_mobile():
            em = discord.Embed(title=f"{user.name}'s info of device.",
                                description=":white_check_mark: Mobile\n:x: Web\n:x: Desktop", color=user.color)
        elif str(user.web_status) != "offline":
            em = discord.Embed(title=f"{user.name}'s info of device.",
                                description=":x: Mobile\n:white_check_mark: Web\n:x: Desktop", color=user.color)
        elif str(user.desktop_status) != "offline":
            em = discord.Embed(title=f"{user.name}'s info of device.",
                                description=":x: Mobile\n:x: Web\n:white_check_mark: Desktop", color=user.color)
        # print(user.web_status)
        # print(user.is_on_mobile())
        await ctx.send(embed=em)
        

    @commands.command(name="ping")
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _ping(self, ctx):
        lat = round((self.bot.latency)*1000)
        em = discord.Embed(title=":ping_pong: | Pong!",color=discord.Color.gold())
        em.add_field(name="DWSP Latency:",value=f"`{lat}ms.`")
        start = time()
        message = await ctx.send(embed=em)
        end = time()
        em.add_field(name="Response Time:",value=f"`{(end-start)*1000:,.0f} ms.`")
        start = time()
        db = firebase.database()
        prefix_data = db.child('Prefixes').child(str(ctx.guild.id)).get()
        end = time()
        em.add_field(name="DB read:",value=f"`{(end-start)*1000:,.0f} ms.`")
        start = time()
        db.child('Dump').child(str(ctx.guild.id)).set({"Dump":"Dump"})
        end = time()
        em.add_field(name="DB write:",value=f"`{(end-start)*1000:,.0f} ms.`")
        await message.edit(embed=em)
    @commands.command(name="avatar", aliases=["av", "pfp"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _avatar(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        em = discord.Embed(
            description=f"[PNG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=1024) | [JPEG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpeg?size=1024) | [WEBP]({user.avatar_url})", color=discord.Color.random())
        em.set_author(name=f"{user.name}'s avatar",
                        url=f"{user.avatar_url}")
        em.set_image(url=f"{user.avatar_url}")
        await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        try:
            message = payload.cached_message
            self.sniped_msgs[message.channel.id] = (
                message.content, message.author, message.channel, message.created_at)
        except:
            pass

    @commands.command(name="snipe", aliases=["sniper"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _snipe(self, ctx, channel: discord.channel.TextChannel = None):
        db = firebase.database()
        
        try:
            if channel is None:
                contents, author, channel, time = self.sniped_msgs[ctx.channel.id]
            else:
                contents, author, channel, time = self.sniped_msgs[channel.id]
            em = discord.Embed(description=contents,
                                color=discord.Color.random(), timestamp=time)
            em.set_author(
                name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
            em.set_footer(text=f"Deleted in : #{channel}")
            await ctx.send(embed=em)
        except KeyError:
            await ctx.send("**`Found Nothing to Snipe ;)`**")

    @commands.command(name="botinfo", aliases=["bi", "binfo", "boti"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _botinfo(self, ctx):
        user = self.bot.user
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(title="Jumbo's Info", color=discord.Color.random())
        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time()-proc.create_time())
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)
        usage = psutil.cpu_percent(2)
        #player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        fields = [
            ("Owner","TheMonkeyCoder#0001",True),
            ("Python version", python_version(), True),
            ("discord.py version", discord_version, True),
            ("Uptime", uptime, True),
            ("Memory usage",f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
            ("CPU usage",f"{usage}%", True),
            ("Number of Guilds", len(self.bot.guilds),True),
            ("Users", f"{len(self.bot.users)}", True),
            ("Registered", user.created_at.strftime(date_format), True),
            ("Number of Commands", len(self.bot.commands)+12,True),
            ("Version", self.bot.version,True)
            ]
        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)
        em.set_thumbnail(url=str(user.avatar_url))
        await ctx.send(embed=em)
    
    @commands.Cog.listener()
    async def on_message_edit(self,message_before,message_after):
        try:
            self.editsnipe_msgs[message_after.channel.id] = (
                message_before.content, message_after.content, message_after.author,message_after.channel, message_after.created_at)
            
        except:
            pass
    
    @commands.command(name="editsnipe", aliases=["editsniper","esnipe"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _editsnipe(self, ctx, channel: discord.channel.TextChannel = None):
        try:
            if channel is None:
                message_before, message_after, author, channel, time = self.editsnipe_msgs[ctx.channel.id]
            else:
                message_before, message_after, author, channel, time = self.editsnipe_msgs[channel.id]
            em = discord.Embed(description=f'**Message Before:** {message_before}\n**Message After:** {message_after}',
                                color=discord.Color.random(), timestamp=time)
            em.set_author(
                name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
            em.set_footer(text=f"Edited in : #{channel}")
            await ctx.send(embed=em)
        except KeyError:
            await ctx.send("**`Found Nothing to Snipe ;)`**")
    
    @commands.command(name='whois')
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _whois(self,ctx,u_id:int):
        date_format = "%a, %d %b %Y %I:%M %p"
        user = await self.bot.fetch_user(u_id)
        em = discord.Embed(title=f"{user.name}#{user.discriminator} ---- {user.id}",color=discord.Color.random())
        em.set_thumbnail(url=f"{user.avatar_url}")
        em.add_field(name="Created on:",value=user.created_at.strftime(date_format))
        #em.add_field(name="Animated Avatar:",value=user.is_avatar_animated())
        em.add_field(name="Bot:",value=user.bot)
        em.add_field(name="Mutual Servers:",
        value="\n".join(f"`{i.id}` **{i.name}**" for i in user.mutual_guilds)
        )
        await ctx.send(embed=em)
        #print(user.mutual_guilds)
    @commands.command(name='github',aliases=["githubstats","gitstats"])
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _github(self,ctx,*,username:str):
        url = f"https://api.snowflake107.repl.co/api/githubstats?username={username}"
        r = requests.get(url=url,headers={"query":username,"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"},stream=True).json()
        #x = requests.get(url=url,headers={"query":username,"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"},stream=True).url
        name = r['name']
        avatar = r['avatar']
        followers = r['followers']
        repos = r['repos']
        pullreq = r['pullRequests']
        issues = r['issues']
        em = discord.Embed(color=discord.Color.dark_blue())
        em.set_author(name=name,icon_url=avatar)
        em.set_thumbnail(url=avatar)
        em.add_field(name='Name',value=name,inline=False)
        em.add_field(name='Followers',value=followers,inline=False)
        em.add_field(name="Repos",value=repos,inline=False)
        em.add_field(name='Issues',value=issues,inline=False)
        em.add_field(name="Pull Requests",value=pullreq,inline=False)
        await ctx.send(embed=em)
        #print(r)
        #x = Image.open(requests.get(url=url,headers={"Authorization":"NTc2NDQyMDI5MzM3NDc3MTMw.MTYxODU0MjEyNTA5Ng==.fc6b183fdd97d9bcc3cddce606e0ad70"},stream=True).raw)
        # with io.BytesIO() as image_binary:
        #     x.save(image_binary,"PNG")
        #     image_binary.seek(0)
        #     await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
def setup(bot):
    bot.add_cog(InfoCogs(bot))