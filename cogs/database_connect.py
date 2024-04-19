import discord
from discord.ext import commands
from utils.database_utils import connect_to_database

class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_database_connection(self):
        return connect_to_database()

async def setup(bot):
    await bot.add_cog(DatabaseCog(bot))