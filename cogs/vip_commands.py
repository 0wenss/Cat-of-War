import discord
from discord.ext import commands
import aiohttp
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

class VIPCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def fetch_vip_data(self, url, headers):
        print("Making an API request to:", url)
        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    print("API request successful")
                    return await response.json()
                else:
                    print(f"Failed to fetch data, status code: {response.status}")
                    return None
        except Exception as e:
            print(f"An error occurred during API request: {e}")
            return None

    @commands.hybrid_command(description="Fetch and display VIPs earned through seeding")
    async def seed(self, ctx):
        url = "https://west.hll-merc.org/api/get_vip_ids"
        headers = {'Authorization': 'bearer your_api_key'}  # Ensure your API key is securely handled
        data = await self.fetch_vip_data(url, headers)
        if data:
            seed_vips = [
                f"{vip['name'].replace('-SEED-', '').strip()} - Expires on <t:{int((datetime.fromisoformat(vip['vip_expiration'].replace('Z', '')) - timedelta(hours=7)).timestamp())}:f>"
                for vip in data['result'] if '-SEED-' in vip['name']
            ]
            message = "\n".join(seed_vips) if seed_vips else "No VIPs with '-SEED-' found."
            await ctx.send(message, ephemeral=True)
        else:
            await ctx.send("Failed to fetch VIP data.", ephemeral=True)

    @commands.hybrid_command(description="Check the VIP status of a specific Steam ID")
    async def vip(self, ctx, steam_id: str):
        url = "https://west.hll-merc.org/api/get_vip_ids"
        headers = {'Authorization': 'bearer your_api_key'}
        data = await self.fetch_vip_data(url, headers)
        if data:
            vip_status = [
                f"{vip['name']} - Expires on <t:{int((datetime.fromisoformat(vip['vip_expiration'].replace('Z', '')) - timedelta(hours=7)).timestamp())}:f>"
                for vip in data['result'] if vip['steam_id_64'] == steam_id
            ]
            message = "\n".join(vip_status) if vip_status else f"No VIP status found for Steam ID {steam_id}."
            await ctx.send(message, ephemeral=True)
        else:
            await ctx.send("Failed to fetch VIP data.", ephemeral=True)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

async def setup(bot):
    await bot.add_cog(VIPCommands(bot))