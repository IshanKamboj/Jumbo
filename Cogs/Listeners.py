import discord
from discord.ext import commands
import asyncio
from Database.db_files import firebase
from helpEmbeds import HelpEmbeds
from datetime import datetime
default_prefix = "j!"

lvl_add = 1
difficulty = 300
class CommandDisabled(commands.CheckFailure):
    pass
class MissingRequiredServerRoles(commands.CheckFailure):
    pass
class AllListeners(commands.Cog):
    def __init__(self,bot,difficulty,lvl_add):
        self.bot = bot
        self.difficulty = difficulty
        self.lvl_add = lvl_add
    
    def check_enabled(ctx):
        db = firebase.database()
        isEnabled = db.child('Disabled').child(str(ctx.guild.id)).child(ctx.command).get()
        if isEnabled.val() is None:
            return isEnabled.val() is None
        else:
            raise CommandDisabled
            return isEnabled.val() is None
    
    def role_check(ctx):
        db = firebase.database()
        req_role = db.child("Settings").child(str(ctx.guild.id)).child(str(ctx.command)).get()
        user_role = list(map(int, [r.id for r in ctx.author.roles]))
        if req_role.val() is not None:
            for i in user_role:
                if i in req_role.val()["roles_id"]:
                    return True
                    break
            raise MissingRequiredServerRoles
            return False
        else:
            return True
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Everyone Fight"))
        print('Logged in as {0.user}'.format(self.bot))
        await self.bot.get_channel(826719835630338058).send('Logged in as {0.user}'.format(self.bot))
     
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        emb = discord.Embed(title='Jumbo joined a guild.',color=discord.Color.random(),thumbnail=f'{guild.icon_url}')
        emb.add_field(name='Guild Name',value=f'`{guild.name}`')
        emb.add_field(name='Guild ID',value=f'`{guild.id}`')
        emb.add_field(name='Guild owner',value=f'`{guild.owner}`')
        emb.add_field(name='No. of members',value=f'`{guild.member_count}`')
        emb.add_field(name='Joined on',value=f'`{datetime.utcnow()}`')
        emb.add_field(name='Guild created at',value=f'{guild.created_at}')
        await self.bot.get_channel(826719835630338058).send(embed=emb)
        db = firebase.database()
        db.child('Prefixes').child(str(guild.id)).set({'Prefix':default_prefix})
        em = discord.Embed(title="Hola Nabs, I am Jumbo",description="""
        **Jumbo is a fun bot... use it to have fun with ur friends in the same server.**

        It also has many utility commands such as afk,dm,autreact. There are also fun commands.
        Don't forget levelling.... Jumbo also has a levelling system to check who's active or who's not.

        Default Prefix : `j!` (Mention to know the prefix of your server)
    
        Use *help <command> for extended information on a command
    
        [** •Invite me**](https://discord.com/api/oauth2/authorize?client_id=805430097426513941&permissions=469822528&scope=bot "Add the bot to your server")
        
        """,color=discord.Color.random()
        
        )

        for channel in guild.text_channels:
            if "general" in channel.name:
                await channel.send(embed=em)
                break
        
    @commands.Cog.listener()
    async def on_member_join(self,member):
        #print('yes')
        for channel in member.server.channels:
            if str(channel) == "general":
                await client.send_message(f'Hello {member.mention}')
                break
    @commands.Cog.listener()
    async def on_message(self,message):
        db = firebase.database()
        try:
            prefix_data = db.child('Prefixes').child(str(message.guild.id)).get()
        except:
            pass
        seen_data = db.child("Last Seen").child(str(message.author.id)).get()
        if seen_data.val() is None:
            db.child("Last Seen").child(str(message.author.id)).set({"Time":str(datetime.utcnow())})
        elif seen_data.val() is not None:
            db.child("Last Seen").child(str(message.author.id)).update({"Time":str(datetime.utcnow())})
        
        if message.author != self.bot.user:
            #msg = message.content
            try:
                if ":" == message.content[0] and ":" == message.content[-1]:
                    emoji_name = message.content[1:-1]
                    for emoji in message.guild.emojis:
                        if emoji_name == emoji.name:
                            webhooks = await message.channel.webhooks()
                            webhook = discord.utils.get(webhooks, name = "Imposter NQN")
                            if webhook is None:
                                webhook = await message.channel.create_webhook(name = "Imposter NQN")

                            await webhook.send(str(emoji), username = message.author.name, avatar_url = message.author.avatar_url)
                            # await message.delete()
                            # await message.channel.send(str(emoji))
                            await message.delete()
                            # break
            except Exception as e:
                print(str(e))
            if message.raw_mentions:
                for i in message.raw_mentions:
                    afk_data = db.child("AFK").child(str(message.guild.id)).child(str(i)).get()

            try:
                for i in message.raw_mentions:
                    reaction_data =  db.child('Reactions').child(str(message.guild.id)).child(str(i)).get()
                    await message.add_reaction(reaction_data.val()['Reaction'])
            except:
                pass
            try:
                reason = afk_data.val()["reason"]
                em = discord.Embed(title=f"User AFK",description=f"The Mentioned user is AFK....... **Reason: {reason}**",color=discord.Color.from_rgb(255,20,147))
                await message.channel.send(message.author.mention,embed=em)
            except:
                pass
            if message.content.startswith(prefix_data.val()['Prefix']):
                return
            elif self.bot.user.mentioned_in(message):
                em = (discord.Embed(description=f"Yo! My prefix here is `{prefix_data.val()['Prefix']}`. You can use `{prefix_data.val()['Prefix']}help` for more information",color=discord.Color.random()))
                await message.channel.send(embed = em)
            else:
                if not message.author.bot:
                    data = db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).get()   
                    if data.val() is None:
                        newUser = {"userName":str(message.author),"lvl":1,"exp":1}
                        db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).set(newUser)
                    elif data.val() is not None:
                        exp = data.val()['exp']
                        lvl = data.val()['lvl']
                        exp += self.lvl_add
                        
                        a = self.difficulty+(lvl-1)*self.difficulty
                        mention = message.author.mention
                        if exp >= a:
                            lvl += 1
                            lvl_embed = (discord.Embed(title="**Level Up**",
                            description= f"Congratulations {mention}. You just reached level {lvl}",
                            color = discord.Color.from_rgb(0,255,185)
                            )
                            .set_thumbnail(url=f"{message.author.avatar_url}")
                            )
                            await message.channel.send(mention,embed=lvl_embed)
                        db.child("Levels").child(str(message.guild.id)).child(str(message.author.id)).update({"exp":exp,"lvl":lvl})
                    await asyncio.sleep(2)
                else:
                    pass
        await self.bot.process_commands(message)
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        db = firebase.database()
        prefix_data = db.child('Prefixes').child(str(ctx.guild.id)).get()
        pre = prefix_data.val()["Prefix"]
        if isinstance(error,commands.CommandNotFound):
            em = discord.Embed(title="Command not found",description=f"{error}..... use `{pre}help` for info on commands.")
            await ctx.send(embed=em)
        elif isinstance(error,commands.BotMissingPermissions):
            pass
        elif isinstance(error, CommandDisabled):
            em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            await ctx.send(embed=em)
        elif isinstance(error, MissingRequiredServerRoles):
            #print('yes')
            em = discord.Embed(title="Missing Role Requirement",description=f"You are missing required roles for using this command. Use `*settings show` to see role requirements for this command.",color=discord.Color.random())
            await ctx.send(embed=em)
        elif isinstance(error,commands.CommandOnCooldown):
            temp = str(error).split(" ")
            time = str(temp[-1])
            time = time.replace("s","")
            time = float(time)
            time = round(time)
            if time >= 3600:
                finalTime= round(time/3600)
                em = discord.Embed(title="Take a hold of yourself",description=f"This command is on cooldown. You need to wait **{finalTime} hours** before using it again.",color=discord.Color.random())
            elif time < 3600 and time > 60:
                finalTime = round(time/60)
                em = discord.Embed(title="Take a hold of yourself",description=f"This command is on cooldown. You need to wait **{finalTime} minutes** before using it again.",color=discord.Color.random())
            elif time < 60:
                em = discord.Embed(title="Take a hold of yourself",description=f"This command is on cooldown. You need to wait **{time} seconds** before using it again.",color=discord.Color.random())
            #print(finalTime)
            await ctx.send(embed=em)
        else:
            pass
            # if 'The check functions for command failed.' in str(error):
            #     #print('yes')
            #     em = discord.Embed(description="This command is disabled in your server. Ask admin to enable it",color=discord.Color.random())
            #     await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(AllListeners(bot=bot,lvl_add=lvl_add,difficulty=difficulty))