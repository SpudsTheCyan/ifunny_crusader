# main.py
import discord, os

# gets bot token from env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# defines the bot obj
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.event
# prints when the bot has connected to discord
async def on_connect():
	print (f'\n{bot.user} has connected to Discord!')
	# loads the commands
	bot.load_extension('cogs.listener')
	# await bot.sync_commands()

# prints what guilds the bot is connected to
@bot.event
async def on_ready():
	await bot.wait_until_ready()
	print(
		f'Logged in as {bot.user} ID: {bot.user.id}\n{bot.user} has connected to the following guild(s):\n'
	)
	async for guild in bot.fetch_guilds(limit=None):
		print (f'{guild.name} (id: {guild.id})')

# runs the bot
bot.run(BOT_TOKEN)

# invite url
# https://discord.com/api/oauth2/authorize?client_id=1141155606963683442&permissions=274877908992&scope=bot