from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction
import discord
from utils import db_query
from letterboxdpy.user import User
from letterboxdpy.core.exceptions import InvalidResponseError


class AddUserCog(Cog):

	def __init__(self, bot: Bot):
		self.bot = bot

	@app_commands.command(
		name="add_user",
		description="Add user to the list",
	)
	@app_commands.checks.has_permissions(administrator=True)
	async def add_user(self, interaction: Interaction, username: str):
		try:
			User(username)
			await db_query(
				db_path=self.bot.db_path,
				query="INSERT OR IGNORE INTO Users(username) VALUES(?)",
				params=(username)
			)
			await interaction.response.send_message(f"Sucessfully added {username} to the list")
		except InvalidResponseError as err:
			return await interaction.response.send_message("This user does not exist on letterboxd, the correct username is in the profile url")



async def setup(bot: Bot):
	await bot.add_cog(AddUserCog(bot))
