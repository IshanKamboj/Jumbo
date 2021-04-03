import discord
from discord.ext import commands

class HelpEmbeds():
#-------------------- Utility commands help embed-----------------------------
    def level_embed():
        em = discord.Embed(title = ":first_place: | Level", description = "Is used to check level of your and others",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*lvl <user(optional)>")
        return em
    def leaderboard_embed():
        em = discord.Embed(title = ":medal: | Leaderboard", description = "Shows the leaderboard for this Server.",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*lb")
        return em
    def afk_embed():
        em = discord.Embed(title = ":keyboard: | AFK", description = "Set AFK for your and let other people know. Use it again to remove ur afk",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*afk <reason>")
        return em
    def seen_embed():
        em = discord.Embed(title="Last Seen", description="This command tells you when the mentioned person was last seen.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*seen <user>")
        return em
    def autoreact_embed():
        em = discord.Embed(title=":upside_down: | Auto react help",description="This command helps set an auto react will will be triggered when u are mentioned")
        em.add_field(name="**Syntax**",value="*ar <reaction>")
        em.add_field(name="**Example**",value="*ar :smile:")
        return em
    
#------------------- Admin commands help embeds --------------------------------
    def givelevel_embed():
        em = discord.Embed(title = "GiveLevel", description = "Gives the mentioned user levels",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*gl <user> <level>")
        return em
    def prefix_embed():
        em = discord.Embed(title = "Prefix", description = "Change the prefix for your server. Customize it acc. to ur needs",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*cp <newPrefix>")
        return em
    def purge_embed():
        em = discord.Embed(title=":negative_squared_cross_mark: | Purge",description="This command deletes a bulk of messages. Just enter a number and that many messages would be deleted.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*purge <amount>")
        return em
    
#---------------------------- Fun commands help embeds ----------------------------
    def fight_embed():
        em = discord.Embed(title = ":boxing_glove: | Fight", description = "See who's more powerful. The one deafeted is muted for 20-60 seconds.",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*fight <user>")
        return em
    def shoot_embed():
        em = discord.Embed(title = ":gun: | Shoot", description = "Shoot someone with a pistol but be careful u can also be shot. The person shooted will have a 50-50 chance of surviving",color=discord.Color.random())
        em.add_field(name="**Syntax**", value="*shoot <user>")
        return em
    def fact_embed():
        em = discord.Embed(title="Facts", description="This command returns a fun fact that you might not know",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*fact")
        return em

    def truth_embed():
        em = discord.Embed(title=":champagne: | Truth",description="This command give mentioned user a truth question to be answered.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*truth <user>")
        return em
    
    def dare_embed():
        em = discord.Embed(title=":champagne: | Dare",description="This command give mentioned user a dare, that is to be done.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*dare <user>")
        return em
    def spam_embed():
        em = discord.Embed(name="Spam Command",description="Spams given message the number of times entered. It also deletes the spammed message after 5 seconds")
        em.add_field(name="**Syntax**",value="*spam <number> <message>")
        return em
    
    def _8ball_embed():
        em = discord.Embed(title=":8ball: | 8ball Help",description="This command answers your yes/no questions. The responses are random",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*8ball <question>")
        return em
    def opinion_embed():
        em = discord.Embed(title="Opinion Command",description="This command tells a random opinion about the person mentioned.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*opinion <user>")
        return em

    def enable_embed():
        em = discord.Embed(title=":white_check_mark: | Enable",description="This command enables an already disabled command.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*enable <command_name>")
        em.add_field(name="**Permission required**",value="`Adminstrator`")
        return em
    def disable_embed():
        em = discord.Embed(title=":x: | Disable",description="This command disables an already enabled command.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*disable <command_name>")
        em.add_field(name="**Permission required**",value="`Adminstrator`")
        return em
    def role_embed():
        em = discord.Embed(title="Role command",color=discord.Color.random())
        em.add_field(name="***role add <user> <role/role ID>**",value="Gives the specified user the specifed role.",inline=False)
        em.add_field(name="***role remove <user> <role/role ID>**",value="Removes the specified role from the user.",inline=False)
        em.add_field(name="***role create <role name> <hoist:(True/False)> <mentionable:(True/False)>**",value="Creates a role with name specified.",inline=False)
        em.add_field(name="***role color <role name> <color:hex_value>**",value="Changes the color of the role specified")
        return em
    def train_embed():
        em = discord.Embed(title=":karate_uniform: | Train Command",description="Gives you random points for your training. These points can be exchanged for items then.")
        em.add_field(name="**Syntax**",value="*train")
        return em
    def shop_embed():
        em = discord.Embed(title=":shopping_cart: | Shop",description="You can see available items in the shop from here.")
        em.add_field(name="**Syntax**",value="*shop")
        return em
    def buy_embed():
        em = discord.Embed(title=":moneybag: | Buy",description="You can buy items from the shop in exchange of training points using this command.")
        em.add_field(name="**Syntax**",value="*buy <item> <amount(optional)>")
        return em
    def profile_embed():
        em = discord.Embed(title=":bust_in_silhouette: | Profile",description="You can see your training points and items using this command.")
        em.add_field(name="**Syntax**",value="*profile")
        return em
    def google_embed():
        em = discord.Embed(title=":mag: | Google",description="This command help you search on google for whatever you want",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*google <query>")
        return em
    def hex_embed():
        em = discord.Embed(title="Hex",description="This command gives you the hex value of the color.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*hex <color>")
        return em
    def roast_embed():
        em = discord.Embed(title=":middle_finger: | Roast Command",description="This command is used to roast the user you mentioned.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*roast <user>")
        return em
    def slap_embed():
        em = discord.Embed(title="Slap Command",description="This command is used to slap someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*slap <user>")
        return em
    def punch_embed():
        em = discord.Embed(title="Punch Command",description="This command is used to punch someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*punch <user>")
        return em
    def lick_embed():
        em = discord.Embed(title="Lick Command",description="This command is used to lick someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*lick <user>")
        return em
    def bite_embed():
        em = discord.Embed(title="Bite Command",description="This command is used to bite someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*bite <user>")
        return em
    def hug_embed():
        em = discord.Embed(title="Hug Command",description="This command is used to hug someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*hug <user>")
        return em
    def bully_embed():
        em = discord.Embed(title="Bully Command",description="This command is used to bully someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*bully <user>")
        return em
    def kick_embed():
        em = discord.Embed(title="Kick Command",description="This command is used to kick someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*kick <user>")
        return em

    def hardkick_embed():
        em = discord.Embed(title="Hard Kick Command",description="This command is used to Hard kick someone.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*hardkick <user>")
        return em
    def userinfo_embed():
        em = discord.Embed(title="Userinfo Command",description="This command gets the information of a user",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*userinfo <user>")
        return em
    def roleinfo_embed():
        em = discord.Embed(title="Roleinfo Command",description="This command gets the information about a role",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*roleinfo <user>")
        return em
    def onlineinfo_embed():
        em = discord.Embed(title="Onlineinfo Command",description="This command gets the information of what device is used by the person.",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*onlineinfo <user>")
        return em
    def avatar_embed():
        em = discord.Embed(title="Avatar Command",description="This command shows avatar of a person",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*av <user>")
        return em
    def snipe_command():
        em = discord.Embed(title=":dart: | Snipe Command",description="This command shows the recent deleted message in last 10 mins in a specific channel. Show none if message is too old",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*snipe [channel]")
        return em

    def editsnipe_command():
        em = discord.Embed(title=":dart: | Editsnipe Command",description="This command shows the recent edited message in last 10 mins in a specific channel. Show none if message is too old",color=discord.Color.random())
        em.add_field(name="**Syntax**",value="*editsnipe [channel]")
        return em
    # def multi_embed():
    #     em = discord.Embed(title="Multi Command",color=discord.Color.random())
    #     em.add_field(name="*multi <channel> <multi>",value="Sets the multi for a specific channel.")
    #     em.add_field(name="*multi <role/role_id> <multi>",value="Sets the multi for a ")

    def gayrate_embed():
        em = discord.Embed(title="Gayrate Command",description="This command tells how much gay a person is. LOL",color=discord.Color.random())
        em.add_field(name="Syntax",value="*gayrate <user>")
        return em
    def joke_embed():
        em = discord.Embed(title="Joke Command",description="This command returns a random joke")
        em.add_field(name="Syntax",value="*joke")
        return em
    def botinfo_embed():
        em = discord.Embed(title="Botinfo Command",description="This command returns info about the bot")
        em.add_field(name="Syntax",value="*botinfo")
        return em

    def wikisearch_embed():
        em = discord.Embed(title="Wikisearch Command",description="This command searches the wikipedia for the provided query.")
        em.add_field(name="Syntax",value="*wikisearch <query>")
        return em

    def wanted_embed():
        em = discord.Embed(title="Wanted Command",description="This command returns a wanted image of someone.")
        em.add_field(name="Syntax",value="*wanted <user>")
        return em
    def rip_embed():
        em = discord.Embed(title="RIP Command",description="This command returns a RIP image of someone.")
        em.add_field(name="Syntax",value="*rip <user>")
        return em
    def wallpaper_embed():
        em = discord.Embed(title="Wallpaper Command",description="This command returns a random 1080p image for wallpaper.")
        em.add_field(name="Syntax",value="*wallpaper")
        return em
    def poll_embed():
        em = discord.Embed(title="Poll Command",description="This command is used to conduct a poll.")
        em.add_field(name="Syntax",value="*poll <question>")
        return em
    def anime_embed():
        em = discord.Embed(title="Animesearch Command",description="This command returns data about an anime.")
        em.add_field(name="Syntax",value="*anime|animesearch <name>")
        return em
    def area_embed():
        em = discord.Embed(title="Area commands",description='**Values must be separated by "," **',color=discord.Color.red())
        em.add_field(name='*area <triangle> <height,base>',value='Gives the area of a  triangle',inline=False)
        em.add_field(name='*area <rectangle> <length,breadth>',value='Gives the area of a rectangle',inline=False)
        em.add_field(name='*area <square> <side>',value='Gives the area of a square with the given side.',inline=False)
        em.add_field(name='*area <circle> <radius>',value='Gives the area of the circle with the given side.',inline=False)
        return em