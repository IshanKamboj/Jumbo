import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from Database.db_files import firebase
from .Listeners import AllListeners, difficulty
import asyncio

class Admin(commands.Cog,name=":lock: **Admin Commands**"):
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
        """
        Gives Levels to users. You cannot give level more than 150.
        """
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
        """
        Change the prefix for your server.
        """
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
        """
        This command deletes a bulk of messages. Just enter a number and that many messages would be deleted.
        """
        #db = firebase.database()
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
        """
        This command disables an already enabled command.
        """
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
                elif command_disable == ctx.command or str(command_disable) == 'settings'  or str(command_disable) == "enable" or str(command_disable) == "help" or str(command_disable) == "prefix":
                    await ctx.send("`You cannot enable/disable this command`")
                else:
                    if disabledCommands.val()["isEnabled"] is True:
                        em = discord.Embed(description=f"**`{command_disable}` command is now disabled**",color=discord.Color.random())
                        db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).update({'isEnabled':False})
                        await ctx.send(embed=em)
                    elif disabledCommands.val()["isEnabled"] is False:
                        await ctx.send(f"**`{command_disable}` command is already disabled**")
                    #print(disabledCommands.val())
            
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
        """
        This command enables a disabled command.
        """
        db = firebase.database()
        command_disable = self.bot.get_command(command)
        disabledCommands = db.child('Disabled').child(str(ctx.guild.id)).child(str(command_disable)).get()

        
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
        em = discord.Embed(title="Role command",color=discord.Color.random())
        em.add_field(name="***role add <user> <role/role ID>**",value="Gives the specified user the specifed role.",inline=False)
        em.add_field(name="***role remove <user> <role/role ID>**",value="Removes the specified role from the user.",inline=False)
        em.add_field(name="***role create <role name> <hoist:(True/False)> <mentionable:(True/False)>**",value="Creates a role with name specified.",inline=False)
        em.add_field(name="***role color <role name> <color:hex_value>**",value="Changes the color of the role specified")
        await ctx.send(embed=em)
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
    @commands.check(AllListeners.check_enabled)
    async def settings(self,ctx):
        em = discord.Embed(title=f"Settings Commands",color=discord.Color.random())
        em.add_field(name="j!settings show",value="Shows the command roles settings for this server.",inline=False)
        em.add_field(name="j!settings cmdrole <command_name> <role_id/role>",value="Sets the required role for using any command. Removes the role if it is already there.",inline=False)
        em.add_field(name="j!settings multi <multiplier> [channel(optional)]",value="Sets the level multiplier for a specific channel.",inline=False)
        em.add_field(name="j!settings announcements",value="Sets an announcements channel for your guild. All the level up messages are then sent in that channel.",inline=False)
        em.add_field(name="j!settings nomessage",value="Toggles between enabling and disabling the level up messages",inline=False)
        em.add_field(name="j!settings lvlrole <lvl:int> <role:id/name>",value="Sets the level roles for your guild. These roles are automatically given on reaching specified levels",inline=False)
        await  ctx.send(embed=em)
        
    @settings.command(name="cmdrole")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _cmdrole(self,ctx,command,role:discord.Role):
        db = firebase.database()
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
        
    @settings.command(name="multi")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _multi(self,ctx, multiplier:int=None, channel:discord.TextChannel = None):
        db = firebase.database()
        if channel == None:
            channel = ctx.channel
        if multiplier == None:
            multi = db.child("Multi").child(str(ctx.guild.id)).get()
            announcement_channel = db.child("Announcement").child(str(ctx.guild.id)).get()
            embed = discord.Embed(title=f"Level Settings for : {ctx.guild.name}",description="",color=discord.Color.random()).set_thumbnail(url=f"{str(ctx.guild.icon_url)}")
            if announcement_channel.val() != None:
                ch = self.bot.get_channel(announcement_channel.val()["channel"])
                embed.add_field(name="Announcements Channel:",value=f"{ch.mention}")
            if not multi.val() is None:
                emoji = discord.utils.get(self.bot.emojis, name = "parrow")
                for i in multi.val():
                    channel =  self.bot.get_channel(int(i))
                    x = db.child("Multi").child(str(ctx.guild.id)).child(i).get()
                    m = x.val()["Multiplier"]
                    if  embed.description == "":
                        embed.description += f"{channel.mention}    {emoji}    **{m}x**"
                    else:
                        embed.description += f"\n{channel.mention}  {emoji}   **{m}x**"
                await ctx.send(embed=embed)
            else:
                await ctx.send("No server settings for this guild")

        else:
            multi = db.child("Multi").child(str(ctx.guild.id)).child(str(channel.id)).get()
            if multiplier <=0:
                multiplier = 1
            if multiplier > 25:
                multiplier = 25
            if multi.val() is None:
                db.child("Multi").child(str(ctx.guild.id)).child(str(channel.id)).set({"Multiplier":multiplier})
                embed = discord.Embed(description=f"**Multi set to {multiplier}x in  **{channel.mention}",color=discord.Color.random())
                await ctx.send(embed=embed)
            else:
                db.child("Multi").child(str(ctx.guild.id)).child(str(channel.id)).update({"Multiplier":multiplier})
                embed = discord.Embed(description=f"**Multi updated to {multiplier}x in ** {channel.mention}",color=discord.Color.random())
                await ctx.send(embed=embed)
    @settings.command(name='announcements',aliases=["announcement","ancments","levelmsg","ann","announce"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _announcement(self,ctx,channel:discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        db = firebase.database()
        announcement_channel = db.child("Announcement").child(str(ctx.guild.id)).get()
        if announcement_channel.val() == None:
            db.child("Announcement").child(str(ctx.guild.id)).set({"channel":channel.id})
            em = discord.Embed(title="Announcements channel set",description=f"{channel.mention} was set as your announcements channel. Now all the level up messages would be sent their.",color=discord.Color.green())
            await ctx.send(embed=em)
        else:
            db.child("Announcement").child(str(ctx.guild.id)).update({"channel":channel.id})
            em = discord.Embed(title="Announcements channel updated",description=f"{channel.mention} was updated as your announcements channel. Now all the level up messages would be sent their.",color=discord.Color.green())
            await ctx.send(embed=em)
    @settings.command(name="nomessage")
    @commands.has_permissions(manage_guild=True)
    async def _nomessage(self,ctx,):
        db = firebase.database()
        x = db.child("LevelMsg").child(ctx.guild.id).get()
        
        if x.val() is None:
            db.child("LevelMsg").child(ctx.guild.id).set({"enabled":False})
            em = discord.Embed(description=f"✅ Level up messages have been disabled successfully",color=discord.Color.green())
            await ctx.send(embed=em)
        elif x.val() is not None:
            y = not x.val()["enabled"]
            db.child("LevelMsg").child(ctx.guild.id).update({"enabled":y})
            if y:
                em = discord.Embed(description=f"✅ Level up messages have been enabled successfully",color=discord.Color.green())
            else:
                em = discord.Embed(description=f"✅ Level up messages have been disabled successfully",color=discord.Color.green())
            await ctx.send(embed=em)
    @settings.command(name='show')
    @commands.guild_only()
    async def _show(self,ctx):
        db = firebase.database()
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
        
    @settings.command(name='levelroles',aliases=["levelrole","lvlrole","lvlroles"])
    @commands.guild_only()
    async def _lvlrole(self,ctx,lvl:int=None,*,role:discord.Role=None):
        db = firebase.database()
        x = db.child('LevelRoles').child(ctx.guild.id).get()
        if lvl == None:
            
            if x.val() == None:
                em = discord.Embed(title=f"Settings Commands",color=discord.Color.random())
                em.add_field(name="*settings show",value="Shows the command roles settings for this server.",inline=False)
                em.add_field(name="*settings cmdrole <command_name> <role_id/role>",value="Sets the required role for using any command. Removes the role if it is already there.",inline=False)
                em.add_field(name="*settings multi <multiplier> [channel(optional)]",value="Sets the level multiplier for a specific channel.",inline=False)
                em.add_field(name="*settings announcements",value="Sets an announcements channel for your guild. All the level up messages are then sent in that channel.",inline=False)
                em.add_field(name="*settings lvlrole <lvl:int> <role:id/name>",value="Sets the level roles for your guild. These roles are automatically given on reaching specified levels",inline=False)
                await  ctx.send(embed=em)
            else:
                em = discord.Embed(title="Level Roles:",description="",color=discord.Color.random())
                em.set_thumbnail(url=f"{str(ctx.guild.icon_url)}")
                emoji = discord.utils.get(self.bot.emojis, name = "parrow")
                #print(x.val())
                for i in x.val():
                    #print(i)
                    
                    y = db.child('LevelRoles').child(ctx.guild.id).child(i).get()
                    
                    
                    role_id = y.val()["roleid"]
                    
                    role = discord.utils.get(ctx.guild.roles,id=role_id)
                    
                    em.description += f"\n{role.mention} {emoji}   `{i}`"
                await ctx.send(embed=em)            
        else:
            if role is None:
                raise MissingRequiredArgument('required argument `role` is missing')
            if x.val() == None:
                db.child('LevelRoles').child(ctx.guild.id).child(lvl).set({"roleid":role.id})
            else:
                db.child('LevelRoles').child(ctx.guild.id).child(lvl).update({"roleid":role.id})
            em = discord.Embed(description=f"{role.mention} was set as role for level: `{lvl}`",color=discord.Color.blurple())
            await ctx.send(embed=em)
    @commands.command(name="resetexp",aliases=["reset","remxp","rexp","resetxp"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.check(AllListeners.check_enabled)
    @commands.check(AllListeners.role_check)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _resetexp(self,ctx,user:discord.Member=None):
        """
        Resets the user exp.
        """
        if user == None:
            user = ctx.author
        db = firebase.database()
        db.child("Levels").child(str(ctx.guild.id)).child(str(user.id)).remove()
        em = discord.Embed(title="Exp reset",description=f"{user.mention} exp was reset.",color=discord.Color.blurple())
        await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Admin(bot,difficulty))