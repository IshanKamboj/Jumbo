from discord.ext import commands
from discord import utils
import discord
from Database.db_files import firebase
from .Listeners import AllListeners
import math
import asyncio
class emoji(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def getemote(self, arg):
		emoji = utils.get(self.bot.emojis, name = arg.strip(":"))

		if emoji is not None:
			if emoji.animated:
				add = "a"
			else:
				add = ""
			return f"<{add}:{emoji.name}:{emoji.id}>"
		else:
			return None

	async def getinstr(self, content):
		ret = []

		spc = content.split(" ")
		cnt = content.split(":")

		if len(cnt) > 1:
			for item in spc:
				if item.count(":") > 1:
					wr = ""
					if item.startswith("<") and item.endswith(">"):
						ret.append(item)
					else:
						cnt = 0
						for i in item:
							if cnt == 2:
								aaa = wr.replace(" ", "")
								ret.append(aaa)
								wr = ""
								cnt = 0

							if i != ":":
								wr += i
							else:
								if wr == "" or cnt == 1:
									wr += " : "
									cnt += 1
								else:
									aaa = wr.replace(" ", "")
									ret.append(aaa)
									wr = ":"
									cnt = 1

						aaa = wr.replace(" ", "")
						ret.append(aaa)
				else:
					ret.append(item)
		else:
			return content

		return ret


	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		if ":" in message.content:
			msg = await self.getinstr(message.content)
			ret = ""
			em = False
			smth = message.content.split(":")
			if len(smth) > 1:
				for word in msg:
					if word.startswith(":") and word.endswith(":") and len(word) > 1:
						emoji = await self.getemote(word)
						if emoji is not None:
							em = True
							ret += f" {emoji}"
						else:
							ret += f" {word}"
					else:
						ret += f" {word}"

			else:
				ret += msg
			

			if em:
				webhooks = await message.channel.webhooks()
				webhook = utils.get(webhooks, name = "Imposter NQN")
				if webhook is None:
					webhook = await message.channel.create_webhook(name = "Imposter NQN")

				await webhook.send(ret, username = message.author.name, avatar_url = message.author.avatar_url)
				await message.delete()
	@commands.command(name="emojisearch",aliases=["esearch","emotesearch","emoji"])
	@commands.guild_only()
	@commands.check(AllListeners.check_enabled)
	@commands.check(AllListeners.role_check)
	@commands.cooldown(1,20, commands.BucketType.user)
	async def _emojisearch(self,ctx,*,query:str):
		emoji_list =  list(map(str, [r.name for r in self.bot.emojis]))
		new_query = query.replace(" ","_")
		em = discord.Embed(title=f"Search Results for: {query}",description="",color=discord.Color.random())
		temp_dict = {}
		
		for i in self.bot.emojis:
			if new_query.lower() in str(i).lower():
				x = str(i).split(":")
				temp_dict[str(i)]=x[1]			
			
		temp = list(temp_dict.items())	
		items_per_page = 5
		current_page = 1
		pages = math.ceil(len(temp) / items_per_page)
		start = (current_page - 1) * items_per_page
		end = start + items_per_page
		buttons = ["⬅️","➡️"]
		for i in temp[start:end]:
			k,v = i
			em.add_field(name=k,value=f"`{v}`",inline=False)
		em.set_footer(text=f"Page : {current_page}/{pages}\nYou can use these as `:name:` to send emojis")
		msg = await ctx.send(embed=em)
		for button in buttons:
			await msg.add_reaction(button)
		while True:
			try:
				reaction, user = await self.bot.wait_for("reaction_add",check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=20.0)
			except asyncio.TimeoutError:
				await msg.clear_reactions()
			else:
				previous_pg = current_page
				if reaction.emoji == "⬅️":
					if current_page > 1:
						current_page -= 1
				elif reaction.emoji == "➡️":
					if current_page < pages:
						current_page += 1
				for button in buttons:
					await msg.remove_reaction(button,ctx.author)
				if previous_pg != current_page:
					pages = math.ceil(len(temp) / items_per_page)
					start = (current_page - 1) * items_per_page
					end = start + items_per_page
					em = discord.Embed(title=f"Search Results for: {query}",description="",color=discord.Color.random())
					for i in temp[start:end]:
						k,v = i
						em.add_field(name=k,value=f"`{v}`",inline=False)
					em.set_footer(text=f"Page : {current_page}/{pages}\nYou can use these as `:name:` to send emojis")
					await msg.edit(embed=em)
def setup(bot):
	bot.add_cog(emoji(bot))