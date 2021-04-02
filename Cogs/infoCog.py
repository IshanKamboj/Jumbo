import discord
from discord.ext import commands
import datetime
from datetime import datetime, timedelta
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

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed(
            description=f'{str(error)}', color=discord.Color.random())
        await ctx.send(embed=em)

    @commands.command(name="userinfo", aliases=["ui"])
    async def _userinfo(self, ctx, user: discord.Member = None):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(
            str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
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
        else:
            em = discord.Embed(
                description="This command is disabled in your server. Ask admin to enable it", color=discord.Color.random())
            await ctx.send(embed=em)

    @commands.command(name="roleinfo", aliases=["ri", "rinfo"])
    async def _roleinfo(self, ctx, role: discord.Role):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(
            str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
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
        else:
            em = discord.Embed(
                description="This command is disabled in your server. Ask admin to enable it", color=discord.Color.random())
            await ctx.send(embed=em)

    @commands.command(name="onlineinfo", aliases=["online"])
    async def _onlineinfo(self, ctx, user: discord.Member):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(
            str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
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
        else:
            em = discord.Embed(
                description="This command is disabled in your server. Ask admin to enable it", color=discord.Color.random())
            await ctx.send(embed=em)

    @commands.command(name="ping")
    @commands.check(AllListeners.check_enabled)
    async def _ping(self, ctx):
        lat = round((self.bot.latency)*1000)
        em = discord.Embed(title=":ping_pong: | Pong!")
        if lat < 150:
            em.color = 0x008000
            em.add_field(name="DWSP Latency:",value=f"`{lat}ms.`")
        elif lat >= 150:
            em.color = 0xffff00
            em.add_field(name="DWSP Latency:",value=f"`{lat}ms.`")
        else:
            em.color = 0xff0000
            em.add_field(name="DWSP Latency:",value=f"`{lat}ms.`")
        start = time()
        message = await ctx.send(embed=em)
        end = time()
        em.add_field(name="Response Time:",value=f"`{(end-start)*1000:,.0f} ms.`")
        await message.edit(embed=em)
    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def _avatar(self, ctx, user: discord.Member = None):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(
            str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            if user == None:
                user = ctx.author
            em = discord.Embed(
                description=f"[PNG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=1024) | [JPEG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpeg?size=1024) | [JPG](https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.jpg?size=1024)", color=discord.Color.random())
            em.set_author(name=f"{user.name}'s avatar",
                          url=f"{user.avatar_url}")
            em.set_image(url=f"{user.avatar_url}")
            await ctx.send(embed=em)

        else:
            em = discord.Embed(
                description="This command is disabled in your server. Ask admin to enable it", color=discord.Color.random())
            await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        try:
            message = payload.cached_message
            self.sniped_msgs[message.channel.id] = (
                message.content, message.author, message.channel, message.created_at)
            await asyncio.sleep(600)
            del self.sniped_msgs[message.channel.id]
        except:
            pass

    @commands.command(name="snipe", aliases=["sniper"])
    async def _snipe(self, ctx, channel: discord.channel.TextChannel = None):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(
            str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
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
        else:
            em = discord.Embed(
                description="This command is disabled in your server. Ask admin to enable it", color=discord.Color.random())
            await ctx.send(embed=em)

    @commands.command(name="botinfo", aliases=["bi", "binfo", "boti"])
    @commands.check(AllListeners.check_enabled)
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
        fields = [
            ("Owner","TheMonkeyCoder#9860",True),
            ("Python version", python_version(), True),
            ("discord.py version", discord_version, True),
            ("Uptime", uptime, True),
            ("Memory usage",f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
            ("CPU usage",f"{usage}%", True),
            ("Number of Guilds", len(self.bot.guilds),True),
            ("Users", f"{len(self.bot.users)}", True),
            ("Registered", user.created_at.strftime(date_format), True),
            ("Number of Commands", len(self.bot.commands),True)
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
            await asyncio.sleep(600)
            del self.editsnipe_msgs[message_after.channel.id]
        except:
            pass
    
    @commands.command(name="editsnipe", aliases=["editsniper"])
    @commands.check(AllListeners.check_enabled)
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