from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction
import discord
from utils import db_query

class AddUserCog(Cog):

	def __init__(self, bot: Bot):
		self.bot = bot

	@app_commands.command(
		name="add_user",
		description="Add user to the list",
	)
	@app_commands.checks.has_permissions(administrator=True)
	async def add_user(self, interaction: Interaction, user: discord.User):
		user = interaction.user
		await db_query(
			db_path=self.bot.db_path,
			query="INSERT OR IGNORE INTO Users(user_id, username) VALUES(?, ?)",
			params=(user.id, user.name)
		)
		await interaction.response.send_message(f"Sucessfully added {user.name} to the list")




async def setup(bot: Bot):
	await bot.add_cog(AddUserCog(bot))
