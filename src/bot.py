import discord
from discord.ext import tasks, commands
import os
import asyncio
from dotenv import load_dotenv
import argparse
import logging
from utils import db_query
from letterboxdpy.user import User
from letterboxdpy.movie import Movie
from letterboxdpy.core.exceptions import InvalidResponseError

parser = argparse.ArgumentParser()
parser.add_argument("--mode")
args = parser.parse_args()
mode = args.mode

LOOP_INTERVAL_SECONDS = 60 if mode == "prod" else 10

class Bot(commands.Bot):
	
	def __init__(self, *args, **kwargs):
		self.letterboxd_text_channel = None
		self.loop_running = False
		super().__init__(*args, **kwargs)
	
	async def setup_hook(self):
		self.db_path = "database/db.sqlite" if mode == "prod" else "database/db_dev.sqlite"
		if not os.path.exists(self.db_path):
			raise FileNotFoundError(f"Database does not exist, create it")

		self.letterboxd_check_task.start()

		for file in os.listdir("src/cogs"):
			try:
				if file.endswith(".py"):
					await self.load_extension(f"cogs.{file.removesuffix(".py")}")
					print(f"Sucessfully loaded {file} cog")
			except discord.ext.commands.errors.ExtensionAlreadyLoaded as err:
				print(err)
				print(f"{file} cog is already loaded")
			except Exception as err:
				raise err
		

	async def on_ready(self):
		print(f"Bot is ready: {self.user}")

	@tasks.loop(seconds=LOOP_INTERVAL_SECONDS)
	async def letterboxd_check_task(self):
		if self.loop_running == True: return # 

		
		# Check if channel_id in database
		config_row = await db_query(
			db_path=self.db_path,
			query="SELECT text_channel_id FROM Config",
			fetch="one"
		)
		
		if config_row == None:
			self.letterboxd_text_channel = None
			return 
		 
		self.loop_running = True
		text_channel_id = config_row['text_channel_id']
		# Set up text channel if none or has been changed
		if self.letterboxd_text_channel == None or self.letterboxd_text_channel.id != text_channel_id:
			self.letterboxd_text_channel = self.get_channel(text_channel_id) or await self.fetch_channel(text_channel_id)
		
		# Iterate over users if any and check activity
		users_rows = await db_query(
			db_path=self.db_path,
			query="SELECT * FROM Users",
			fetch="all"
		)
		try:
			for row in users_rows:
				username = row['username']
				print(f"Checking activity for {username}")

				user = User(username)
				user_logs = user.get_activity()
				user_pfp = user.avatar.get("url")

				# Iterate over `user` activity and check each activity id if its in db or not
				# Starting from the end
				for activity_id, data in user_logs['activities'].items().__reversed__():
					
					# Check if is already logged
					activity_row = await db_query(
						db_path=self.db_path,
						query="SELECT * FROM Activities WHERE activity_id = ?",
						params=(activity_id),
						fetch="one"
					)

					if activity_row:
						continue # activity already logged in

					# Create embed
					embed = discord.Embed(description="")
					embed.set_author(name=username, url=f"https://letterboxd.com/{username}", icon_url=user_pfp)
					embed.color = discord.Color.random()

					embed.title = data['content']['description']
					
					if data['content']['action'] in ["added", "rated", "watched", "liked"]:
						movie_slug = data['content']['movie']['slug']
						try:
							movie = Movie(movie_slug)
							movie_poster = movie.get_poster()
						except InvalidResponseError:
							movie_poster = None

						movie_url = f"https://letterboxd.com/film/" + movie_slug
						embed.set_thumbnail(url=movie_poster)

						if data['content'].get("review"):
							embed.description += f"> `{data['content']['review']['content']}`"

						embed.description += f"{'\n'if len(embed.description) else ''}[link]({movie_url})"

					await self.letterboxd_text_channel.send(embed=embed)
					
					await db_query(
						db_path=self.db_path,
						query="INSERT INTO Activities(activity_id, username) VALUES(?, ?)",
						params=(activity_id, username)
					)

					await asyncio.sleep(0.5)
		except Exception as err:
			print(err)
			
		self.loop_running = False


	@letterboxd_check_task.before_loop
	async def before_letterboxd_check_task(self):
		await self.wait_until_ready()


load_dotenv()
tokens = {
	"prod": os.getenv("DISCORD_BOT_TOKEN"),
	"dev": os.getenv("DISCORD_BOT_TOKEN_DEV")	
}


# by default prod if not specified
if not mode:
	mode = "prod"


handler = logging.FileHandler(filename="log", encoding="utf-8", mode="w")
client = Bot(intents=discord.Intents.all(), log_handler=handler, command_prefix="!" ) # change all
client.run( tokens[mode] )