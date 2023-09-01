# main.py
import logging
import logging.config
import os

import discord

# sets up logging
logging.config.fileConfig('logging.conf', defaults={'logfilename': '/home/pi/Bot_Data/ifunny_crusader/log.txt'})
logger = logging.getLogger("defaultLogger")

# logs when the bot starts
logger.info(f"Program started!")

# gets bot token from env
BOT_TOKEN = os.environ["TOKEN"]
print (BOT_TOKEN)
print(type(BOT_TOKEN))

# defines the bot obj
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.event
# prints when the bot has connected to discord
async def on_connect():
	logger.info(f'{bot.user} has connected to Discord!')
	# loads the commands
	extensions_loaded = bot.load_extension('cogs.listener', store=True)
	if extensions_loaded["cogs.listener"] == True: # type: ignore
		logger.info("Listener Cog Loaded!")
	else:
		logger.error("Listener Cog not loaded!")

# prints what guilds the bot is connected to
@bot.event
async def on_ready():
	await bot.wait_until_ready()
	guild_strings = [f"{guild.name} (id:{guild.id})\n" async for guild in bot.fetch_guilds(limit=None)]
	logger.info(f"Logged in as {bot.user} ID: {bot.user.id}") # type: ignore
	logger.info(f"{bot.user} has connected to the following guild(s):\n	{''.join(guild_strings)}")

# runs the bot
bot.run(BOT_TOKEN)

# main bot invite url
# https://discord.com/api/oauth2/authorize?client_id=1141155606963683442&permissions=274877908992&scope=bot

# dev bot invite url
# https://discord.com/api/oauth2/authorize?client_id=1144056108747595897&permissions=274877908992&scope=bot