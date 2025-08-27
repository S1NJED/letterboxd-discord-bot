from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction
import discord
from utils import db_query


class DeleteUserCog(Cog):

	def __init__(self, bot: Bot):
		self.bot = bot

	@app_commands.command(
		name="delete_user",
		description="Delete user from the checklist",
	)
	@app_commands.checks.has_permissions(administrator=True)
	async def delete_user(self, interaction: Interaction, user: discord.User):
		user = interaction.user
		await db_query(
			db_path=self.bot.db_path,
			query="DELETE FROM Users WHERE user_id=?",
			params=(user.id)
		)
		await interaction.response.send_message(f"Sucessfully deleted {user.name} from the list")



async def setup(bot: Bot):
	await bot.add_cog(DeleteUserCog(bot))
