from discord.ext.commands import Cog, Bot
from discord.ext import commands
from discord import app_commands, Interaction
import discord
import os
from utils import db_query


class SyncCog(Cog):

	def __init__(self, bot: Bot):
		self.bot = bot

	@commands.command(name="sync")
	@commands.is_owner()
	@commands.guild_only()
	async def sync(self, ctx: commands.Context):
		synced = await self.bot.tree.sync()
		await ctx.send(f"✅ Synced {len(synced)} command(s) for this guild")


	@commands.command(name="reload")
	@commands.is_owner()
	@commands.guild_only()
	async def reload_cogs(self, ctx: commands.Context):
		cogs = []
		for file in os.listdir("src/cogs"):
			if file.endswith(".py"):
				await self.bot.reload_extension(f"cogs.{file.removesuffix(".py")}")
				cogs.append(file)
		
		if len(cogs):
			await ctx.send(f"Sucessfully reloaded {len(cogs)} cogs ({', '.join(cogs)})")
		else:
			await ctx.send("Didnt reloaded any cogs ...")


	@commands.command(name="test")
	@commands.is_owner()
	@commands.guild_only()
	async def test(self, ctx: commands.Context):	
		row = await db_query(
			db_path=self.bot.db_path,
			query="SELECT text_channel_id FROM Config",
			fetch="one"
		)
		print(row, row)
		print(row['text_channel_id'])

async def setup(bot: Bot):
	await bot.add_cog(SyncCog(bot))
