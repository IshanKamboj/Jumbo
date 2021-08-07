import discord
from discord.ext import commands
from discord.errors import Forbidden
from Database.db_files import firebase

async def send_embed(ctx, embed):
    
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog,name=":link: **Help**"):
    """
    Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Shows all modules of that bot"""
        # db = sqlite3.connect("Config.db")
        # cursor = db.cursor()
        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS config(
        #     guild_id INT,
        #     prefix TEXT
        # )
        # """)
        # x = cursor.execute(f"SELECT prefix FROM config WHERE guild_id = {ctx.guild.id}")
        # y = x.fetchone()
        # if y is None:
        #     prefix = "g!"
        # else:
        #     prefix = y[0]
        db = firebase.database()
        data = db.child('Prefixes').child(str(ctx.guild.id)).get()
        prefix = data.val()['Prefix']
        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        version = self.bot.version # enter version of your code

        # setting owner name - if you don't wanna be mentioned remove line 49-60 and adjust help text (line 88) 
        owner = 576442029337477130	# ENTER YOU DISCORD-ID
        owner_name = "TheMonkeyCoder"	# ENTER YOUR USERNAME#1234

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            # starting to build embed
            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':smiley:\n`<>` **-----> Required Argument**\n`[]` **-----> Optional Argument**')

            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                if cog != "AllListeners" and cog != "owner" and cog != "WordGame":
                    x = cog.lower().split(" ")
                    #print(x)
                    x = x[1].replace("*","")
                    #print(x)
                    cogs_desc += f'{cog} \n`{prefix}help {x}`\n\n'
                else:
                    continue
                # {self.bot.cogs[cog].__doc__}
            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # setting information about author
            # emb.add_field(name="About", value=f"The Bots is developed by {owner}, based on discord.py.")
            emb.set_footer(text=f"Bot is running {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                #y = ""
                if cog != "AllListeners" and cog != "owner" and cog != "WordGame":
                    x = cog.lower().split("**")
                else:
                    continue
               # print(type(x))
                if input[0].lower() in x[1]:
                    #desc = f"{self.bot.cogs[cog].__doc__}"
                    desc = ""
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            if desc == "":
                                desc += f"`{command.name}`"
                            else:
                                desc += f", `{command.name}`"
                            #emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog}', description=desc,
                                        color=discord.Color.green())

                    # getting commands from cog
                    
                    # found cog - breaking loop
                    break
            
            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                # print(self.bot.commands)
                # for cmd in self.bot.commands:
                #     if str(cmd) in input[0].lower():
                #         emb = discord.Embed(title=f'{cmd} - Command', description=self.bot.commands[cmd].__doc__,
                #                         color=discord.Color.green())
                #print("yes")
                #if (command := discord.utils.get(self.bot.commands,name = input[0].lower())):
                if (command := self.bot.get_command(name = input[0].lower())):
                    #cmd_aliases = "|".join([str(command),*command.aliases])
                    emb = discord.Embed(title=f'{str(command.name).capitalize()} - Command', description=f"**Usage**:\n {command.help}",
                                     color=discord.Color.green())
                    emb.add_field(name="Syntax",value=self.syntax(command,prefix))
                else:
                    emb = discord.Embed(title="What's that?!",
                                        description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                        color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        # else:
        #     emb = discord.Embed(title="It's a magical place.",
        #                         description="I don't know how you got here. But I didn't see this coming at all.\n"
        #                                     "Would you please be so kind to report that issue to me on github?\n"
        #                                     "https://github.com/nonchris/discord-fury/issues\n"
        #                                     "Thank you! ~Chris",
        #                         color=discord.Color.red())

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)

    def syntax(self,command,prefix):
        cmd_and_aliases = "|".join([str(command), *command.aliases])
        params = []

        for key, value in command.params.items():
            if key not in ("self", "ctx"):
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

        params = " ".join(params)

        return f"```{prefix}{cmd_and_aliases} {params}```"

def setup(bot):
    bot.add_cog(Help(bot))