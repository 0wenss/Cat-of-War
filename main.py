import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio  
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger('discord')

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN_TEST')  

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    await bot.load_extension('cogs.database_connect')
    await bot.load_extension('cogs.vip_commands')
    await bot.load_extension('cogs.stat_commands')

async def main():
    await load_extensions() 
    await bot.start(DISCORD_BOT_TOKEN) 

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')

if __name__ == "__main__":
    asyncio.run(main())