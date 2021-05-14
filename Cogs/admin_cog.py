from operator import mul
import discord
from discord.ext import commands
from discord.ext.commands.errors import NoEntryPointError
from Database.db_files import firebase
import random
from helpEmbeds import HelpEmbeds
from .Listeners import AllListeners, difficulty
import asyncio

class Admin(commands.Cog):
    def __init__(self,bot,difficulty):
        self.bot = bot
        self.difficulty = difficulty
    
    #---------------------Give level Command and its errors---------------------------------------
    @commands.command(name="givelevel",aliases=["gl"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.check(AllListeners.check_enabled)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _givelevel(self,ctx:commands.Context,user:discord.Member,level:int):
        database = firebase.database()
        x = database.child("Levels").child(str(ctx.guild.id)).child(str(user.id)).get()
        try:
            if level >= 1 and level <= 150:
                exp = self.difficulty+((level-1)*self.difficulty)-self.difficulty
                database.child("Levels").child(str(ctx.guild.id)).child(str(user.id)).update({'exp':exp,'lvl':level})
                lvl_embed = (discord.Embed(title="**Level Up**",
                                description= f"Congratulations {user.mention}. You just reached level {level}",
                                color = discord.Color.from_rgb(0,255,185)
                                )
                                .set_thumbnail(url=f"{user.avatar_url}")
                                )
                await ctx.send(user.mention,embed=lvl_embed)
            elif level<1 or level > 150:
                await ctx.send(f"{ctx.author.mention} **Are u a DumbASS??......... U cannot give level below 1 or above 150**")
        except TypeError:
            if level >=1:
                exp = self.difficulty+(level-1)*self.difficulty-self.difficulty
                database.child('Levels').child(str(ctx.guild.id)).child(str(user.id)).update({'lvl':level,'exp':exp,'userName':str(user)})
                lvl_embed = (discord.Embed(title="**Level Up**",
                                description= f"Congratulations {user.mention}. You just reached level {level}",
                                color = discord.Color.from_rgb(0,255,185)
                                )
                                .set_thumbnail(url=f"{user.avatar_url}")
                                )
                await ctx.send(user.mention,embed=lvl_embed)
            elif level<1:
                await ctx.send(f"{ctx.author.mention} **Are u a DumbASS??......... U cannot give level below one**")
        except:
            await ctx.send("Pls mention the user or use ID.")
    # @_givelevel.error
    # async def givelevel_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         em = HelpEmbeds.givelevel_embed()
    #         await ctx.send("**Missing required arguments. See help** :point_down::point_down:",embed = em)
    #     elif isinstance(error,commands.MissingPermissions):
    #         em = discord.Embed(title="Missing Required Permission",description="You are missing the following permissions.\n:arrow_forward: manage_guild",color=discord.Color.random())
    #         await ctx.send(embed = em)




#---------------------Change prefix Command and its errors---------------------------------------
    @commands.command(name="prefix",aliases=["cp","changeprefix"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.check(AllListeners.check_enabled)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _prefix(self,ctx:commands.Context,*,newPrefix):
        db = firebase.database()
        prefixs = {"Prefix":newPrefix}
        db.child('Prefixes').child(str(ctx.guild.id)).update({"Prefix":newPrefix})
        em = discord.Embed(description=f"Prefix update for this Sever. New Prefix `{newPrefix}`, use `{newPrefix}help` for more info.")
        await ctx.send(embed=em)

    # @_prefix.error
    # async def prefix_error(self,ctx,error):
    #     if isinstance(error,commands.MissingPermissions):
    #         em = discord.Embed(title="Missing Required Permission",description="You are missing the following permissions.\n:arrow_forward: Adminstrator",color=discord.Color.random())
    #         await ctx.send(embed = em)
    #     elif isinstance(error,commands.MissingRequiredArgument):
    #         em = HelpEmbeds.prefix_embed()
    #         await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed = em)

    #----------------------- Purge command added-----------------------------
    @commands.command(name="purge",aliases=["pu","delete"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.check(AllListeners.check_enabled)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _purge(self,ctx,number:int):
        db = firebase.database()
        try:
            await ctx.channel.purge(limit=number+1)
            # em = discord.Embed(description=f"**Messages removed: `{number}`**\n**Removed by: `{ctx.author.name}`**",color=discord.Color.random())
            #await asyncio.sleep(0.1)
            msg = await ctx.send(f'**Messages removed: **`{number}`\n**Removed by: **`{str(ctx.author)}`')
            await asyncio.sleep(2)
            await msg.delete()
        except ValueError:
            await ctx.send("Please enter a valid number")
    # @_purge.error
    # async def purge_error(self,ctx,error):
    #     if isinstance(error,commands.MissingPermissions):
    #         await ctx.send("**You are missing the required permissions** `manage guild`")
    #     elif isinstance(error,commands.MissingRequiredArgument):
    #         em = HelpEmbeds.purge_embed()
    #         await ctx.send("**Missing required arguments. See help** :point_down::point_down:",embed=em)


    
    
    @commands.command(name="disable",aliases=["toggle"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _disable(self,ctx,*,command):
        db = firebase.database()
        if command == "list":
            x = db.child('Disabled').child(str(ctx.guild.id)).get()
            #temp = []
            em = discord.Embed(title=f"Disabled Commands in {ctx.guild.name}:",description="",color=discord.Color.random())
            if x.val() is not None:
                #print(len(x.val()))
                for k in x.val():
                    if em.description == "":
                        em.description =f"`{k}`"
                    else:
                        em.description = em.description +","+f"`{k}`"
                    #temp.append(k)
                await ctx.send(embed=em)
            elif x.val() is None:
                await ctx.send(f"**No commands disabled in this server.**")
        else:
            command_disable = self.bot.get_command(command)
            
            disabledCommands = db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).get()
            if str(ctx.guild.owner_id) == str(ctx.author.id):
                if disabledCommands.val() is None:
                    if command_disable is None:
                        await ctx.send("`No command with that name found`")
                    elif command_disable == ctx.command or command_disable == "enable":
                        await ctx.send("`You cannot disable this command`")
                    else:
                        em = discord.Embed(description=f"**`{command_disable}` command is now disabled**")
                        db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).set({'isEnabled':False})
                        await ctx.send(embed=em)
                elif disabledCommands.val() is not None:
                    if command_disable is None:
                        await ctx.send("`No command with that name found`")
                    elif command_disable == ctx.command or command_disable == 'settings'  or command_disable == "enable":
                        await ctx.send("`You cannot enable/disable this command`")
                    else:
                        if disabledCommands.val()["isEnabled"] is True:
                            em = discord.Embed(description=f"**`{command_disable}` command is now disabled**",color=discord.Color.random())
                            db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).update({'isEnabled':False})
                            await ctx.send(embed=em)
                        elif disabledCommands.val()["isEnabled"] is False:
                            await ctx.send(f"**`{command_disable}` command is already disabled**")
                    #print(disabledCommands.val())
            else:
                em = discord.Embed(description="This is an owner only command.",color=discord.Color.red())
                await ctx.send(embed=em)
    # @_disable.error
    # async def disable_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed=HelpEmbeds.disable_embed())

    #     elif isinstance(error,commands.MissingPermissions):
    #         await ctx.send("**You are missing the required permissions:** `administrator`")




    @commands.command(name="enable")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _enable(self,ctx,*,command):
        db = firebase.database()
        command_disable = self.bot.get_command(command)
        disabledCommands = db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).get()

        if str(ctx.guild.owner_id) == str(ctx.author.id):
            if disabledCommands.val() is None:
                if command_disable is not None:
                    await ctx.send(f"**`{command_disable}` command is already enabled**")
                elif command_disable is None:
                    await ctx.send("`No command with that name found`")
            elif disabledCommands.val() is not None:
                if command_disable is None:
                    await ctx.send("`No command with that name found`")
                else:
                    if disabledCommands.val()["isEnabled"] is False:
                        em = discord.Embed(description=f"**`{command_disable}` command is now enabled**",color=discord.Color.random())
                        db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).remove()
                        await ctx.send(embed=em)
                    elif disabledCommands.val()["isEnabled"] is True:
                        await ctx.send(f"**`{command_disable}` command is already enabled**")
        else:

            em = discord.Embed(description="This is an owner only command.",color=discord.Color.red())
            await ctx.send(embed=em)

    # @_enable.error
    # async def enable_error(self,ctx,error):
    #     if isinstance(error,commands.MissingRequiredArgument):
    #         await ctx.send("**Missing required argument. See help** :point_down::point_down:",embed=HelpEmbeds.enable_embed())

    #     elif isinstance(error,commands.MissingPermissions):
    #         await ctx.send("**You are missing the required permissions:** `administrator`")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.check(AllListeners.check_enabled)
    @commands.has_permissions(manage_roles=True)
    async def role(self,ctx):
        db = firebase.database()
        await ctx.send(embed=HelpEmbeds.role_embed())
    @role.command(name="add")
    @commands.guild_only()
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
                if  highest_role > role or ctx.author.guild_permissions.administrator:
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
    @commands.guild_only()
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
                if  highest_role > role or ctx.author.guild_permissions.administrator:
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
    @commands.guild_only()
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
    @commands.guild_only()
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

    
    @commands.group(name="settings",aliases=["setting"],invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.check(AllListeners.check_enabled)
    async def settings(self,ctx):
        await  ctx.send(embed=HelpEmbeds.settings_embed())
        
    @settings.command(name="cmdrole")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _cmdrole(self,ctx,command,role:discord.Role):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("settings").get()
        if isEnabled.val() is None:
            command_ = self.bot.get_command(command)
            x = db.child("Settings").child(str(ctx.guild.id)).child(str(command_)).get()
            if x.val() is None:
                db.child("Settings").child(str(ctx.guild.id)).child(str(command_)).set({"roles_id":[role.id]})
                await ctx.send(f"`{role}` was added as requirment for using `{command_}` command")
            else:
                temp =[]
                if role.id in x.val()["roles_id"]:
                    temp = x.val()["roles_id"]
                    for i in temp:
                        if i == role.id:
                            temp.remove(i)
                    db.child("Settings").child(str(ctx.guild.id)).child(str(command_)).set({"roles_id":temp})
                    await ctx.send(f"Role: `{role}` was removed as requirment for using `{command_}` command")
                else:
                    temp = x.val()["roles_id"]
                    temp.append(role.id)
                    db.child("Settings").child(str(ctx.guild.id)).child(str(command_)).set({"roles_id":temp})

                    await ctx.send(f"Role: `{role}` was also  added as requirment for using `{command_}` command")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
    @settings.command(name="multi")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _multi(self,ctx, multiplier:int, channel:discord.TextChannel = None):
        db = firebase.database()
        if channel == None:
            channel = ctx.channel
        multi = db.child("Multi").child(str(ctx.guild.id)).child(str(channel.id)).get()
        if multiplier <=0:
            multiplier = 1
        if multiplier > 25:
            multiplier = 25
        if multi.val() is None:
            db.child("Multi").child(str(ctx.guild.id)).child(str(channel.id)).set({"Multiplier":multiplier})
            embed = discord.Embed(description=f"**Multi set to {multiplier}x in**{channel.mention}",color=discord.Color.random())
            await ctx.send(embed=embed)
        else:
            db.child("Multi").child(str(ctx.guild.id)).child(str(channel.id)).update({"Multiplier":multiplier})
            embed = discord.Embed(description=f"**Multi updated to {multiplier}x in** {channel.mention}",color=discord.Color.random())
            await ctx.send(embed=embed)
    @settings.command(name="showmulti")
    @commands.guild_only()
    async def _showmulti(self,ctx):
        db = firebase.database()
        multi = db.child("Multi").child(str(ctx.guild.id)).get()
        if not multi.val() is None:
            embed = discord.Embed(title=f"Multi Settings for : {ctx.guild.name}",description="",color=discord.Color.random()).set_thumbnail(url=f"{str(ctx.guild.icon_url)}")
            for i in multi.val():
                channel =  self.bot.get_channel(int(i))
                x = db.child("Multi").child(str(ctx.guild.id)).child(i).get()
                m = x.val()["Multiplier"]
                if  embed.description == "":
                    embed.description += f"{channel.mention}    :arrow_right:   **{m}x**"
                else:
                    embed.description += f"\n{channel.mention}  :arrow_right:   **{m}x**"
            await ctx.send(embed=embed)
        else:
            await ctx.send("No server settings for this guild")
        #print(embed.description)
    @settings.command(name='show')
    @commands.guild_only()
    async def _show(self,ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child("settings").get()
        if isEnabled.val() is None:
            x = db.child("Settings").child(str(ctx.guild.id)).get()
            if not x.val() is None:
                temp_text=""
                em = discord.Embed(title=f"Role Settings for {ctx.guild.name}",color=discord.Color.random()).set_thumbnail(url=f"{str(ctx.guild.icon_url)}")
                for i in x.val():
                    y = db.child("Settings").child(str(ctx.guild.id)).child(str(i)).get()
                    for j in y.val()["roles_id"]:
                        role = ctx.guild.get_role(j)
                        if temp_text == "":
                            temp_text = f"{role.mention}"
                        else:
                            temp_text += f", {role.mention}"
                    em.add_field(name=f"{i} Command",value=temp_text,inline=False)
                    temp_text = ""
                await ctx.send(embed=em)
            else:
                await ctx.send("No server settings for this guild")
        else:
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Admin(bot,difficulty))