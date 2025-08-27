from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction
import discord
from utils import db_query


class ConfigCog(Cog):

	def __init__(self, bot: Bot):
		self.bot = bot

	@app_commands.command(
		name="set_channel",
		description="Set the channel where you want to send the logs",
	)
	@app_commands.checks.has_permissions(administrator=True)
	async def set_channel(self, interaction: Interaction, channel: discord.TextChannel):
		await db_query(
			db_path=self.bot.db_path,
			query="INSERT OR IGNORE INTO Config(text_channel_id) VALUES(?)",
			params=(channel.id)
		)
		await interaction.response.send_message(f"Sucessfully set <#{channel.id}>")


	@app_commands.command(
		name="delete_channel",
		description="Delete the channel where you send the logs",
	)
	@app_commands.checks.has_permissions(administrator=True)
	async def delete_channel(self, interaction: Interaction):
		await db_query(
			db_path=self.bot.db_path,
			query="DELETE FROM Config"
		)
		await interaction.response.send_message(f"Sucessfully deleted channel")


async def setup(bot: Bot):
	await bot.add_cog(ConfigCog(bot))
