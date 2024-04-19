import discord
from discord.ext import commands
import asyncio
import time
import logging
from utils.database_utils import connect_to_database

CHANNEL_ID = 1178709009314889750

weapon_categories = {
    "Tank": ["M6 37mm [M8 Greyhound]", "37MM CANNON [Stuart M5A1]", "COAXIAL M1919 [Sherman M4A3E2]", "75MM CANNON [Sherman M4A3(75)W]", "76MM M1 GUN [Sherman M4A3E2(76)]", "COAXIAL M1919 [Sherman M4A3E2(76)]", "75MM CANNON [PAK 40]", "HULL MG34 [Sd.Kfz.161 Panzer IV]", "Sherman M4A3(75)W", "50mm KwK 39/1 [Sd.Kfz.234 Puma]", "75MM CANNON [Sd.Kfz.161 Panzer IV]", "88 KWK 36 L/56 [Sd.Kfz.181 Tiger 1]", "COAXIAL MG34 [Sd.Kfz.161 Panzer IV]", "150MM HOWITZER [sFH 18]", "Sherman M4A3E2", "COAXIAL M1919 [Sherman M4A3(75)W]", "75MM M3 GUN [Sherman M4A3E2]", "Sd.Kfz.121 Luchs", "20MM KWK 30 [Sd.Kfz.121 Luchs]", "HULL M1919 [Sherman M4A3E2]", "HULL M1919 [Sherman M4A3(75)W]", "HULL M1919 [Sherman M4A3E2(76)]", "COAXIAL MG34 [Sd.Kfz.234 Puma]", "COAXIAL MG34 [Sd.Kfz.181 Tiger 1]", "HULL M1919 [Stuart M5A1]", "COAXIAL M1919 [M8 Greyhound]", "COAXIAL MG34 [Sd.Kfz.121 Luchs]", "Sd.Kfz.234 Puma", "HULL MG34 [Sd.Kfz.171 Panther]", "HULL MG34 [Sd.Kfz.181 Tiger 1]", "COAXIAL M1919 [Stuart M5A1]", "COAXIAL MG34 [Sd.Kfz.171 Panther]", "57MM CANNON [M1 57mm]", "Sherman M4A3E2(76)", "Stuart M5A1", "75MM CANNON [Sd.Kfz.171 Panther]", "Sd.Kfz.171 Panther", "COAXIAL MG34", "M8 Greyhound", "Sd.Kfz.161 Panzer IV", "19-K 45MM [BA-10]", "COAXIAL DT [BA-10]", "57MM CANNON [ZiS-2]", "D-5T 85MM [IS-1]", "76MM ZiS-5 [T34/76]", "COAXIAL DT [T34/76]", "T34/76", "HULL DT [T34/76]", "COAXIAL DT", "COAXIAL DT [IS-1]", "45MM M1937 [T70]", "COAXIAL DT [T70]", "HULL DT [IS-1]", "QF 75MM [Cromwell]", "COAXIAL M1919", "COAXIAL M1919 [Firefly]", "QF 17-POUNDER [Firefly]", "HULL BESA [Cromwell]", "COAXIAL BESA [Cromwell]", "COAXIAL BESA [Tetrarch]", "QF 2-POUNDER [Tetrarch]", "QF 2-POUNDER [Daimler]", "COAXIAL BESA [Daimler]", "IS-1", "T70"], 
    "Mine": ["S-MINE", "M2 AP MINE", "TELLERMINE 43"],
    "Grenade": ["M43 STIELHANDGRANATE", "MK2 GRENADE", "M24 STIELHANDGRANATE"],
    "Rocket": ["BAZOOKA", "PANZERSCHRECK", "PIAT"],
    "Melee": ["FELDSPATEN", "M3 KNIFE", "Fairbairn–Sykes"],
    "Light Vehicle": ["GMC CCKW 353 (Supply)", "Opel Blitz (Supply)", "Sd.Kfz 251 Half-track", "BA-10"],
    "AT Gun": ["QF 6-POUNDER [QF 6-Pounder]", "75MM CANNON [PAK 40]", "57MM CANNON [M1 57mm]"],
    "Artillery": ["150MM HOWITZER [sFH 18]"],
    "Flamethrower": ["M2 FLAMETHROWER", "FLAMETHROWER", "FLAMMENWERFER"]
}
categories = ["MP40","M1A1 THOMPSON","MG42","STG44","KARABINER 98K","M1 GARAND","GEWEHR 43","M97 TRENCH GUN","MG34","M1 CARBINE","SATCHEL","M3 GREASE GUN","M1918A2 BAR","BROWNING M1919","FG42 x4","WALTHER P38","KARABINER 98K x8","FG42","COLT M1911","M1903 SPRINGFIELD","LUGER P08","PRECISION STRIKE","MOSIN NAGANT 1891","SVT40","MOSIN NAGANT M38","MOSIN NAGANT 91/30","PPSH 41","PTRS-41","PPSH 41 W/DRUM","TOKAREV TT33","DP-27","MOLOTOV","NAGANT M1895","SATCHEL CHARGE","SCOPED SVT40","SCOPED MOSIN NAGANT 91/30","Rifle No.5 Mk I","Lewis Gun","Rifle No.4 Mk I","SMLE No.1 Mk III","Lanchester","Boys Anti-tank Rifle","Sten Gun","Webley MK VI","Bren Gun","Lee-Enfield Pattern 1914 Sniper","Tank","Mine","Grenade","Rocket","Melee","Light Vehicle","AT Gun","Artillery","Flamethrower"]
SPECIAL_CATEGORIES = ["Tank", "Mine", "Grenade", "Rocket", "Melee", "Light Vehicle", "AT Gun", "Artillery", "Flamethrower"]
DIRECT_CATEGORIES = ["Kills", "Deaths", "Longest Killstreak", "Longest Deathstreak"]
logger = logging.getLogger(__name__)

weapon_to_category = {}
for category, weapons in weapon_categories.items():
    for weapon in weapons:
        weapon_to_category[weapon] = category 

class StatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logger  # Assign logger to the class

    @commands.hybrid_command(description='Shows player profile.')
    async def stats(self, ctx, steam_id: str = None):
        # Your command logic here
        pass

    # Error handler for the StatCommands cog
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            # Log the error
            self.logger.error(f'In {ctx.command.qualified_name}: {original.__class__.__name__}: {original}')
        
    @commands.hybrid_command(description='Test Command')
    async def test(self, ctx):    
        await ctx.send("Test Message")
        
    @commands.hybrid_command(description='Add your own Steam ID')
    async def addprofile(self, ctx, steam_id: str):
        if not steam_id:
            await ctx.send("Please provide a Steam ID.", ephemeral=True)
            return

        connection = connect_to_database()
        if not connection:
            await ctx.send("Failed to connect to the database.", ephemeral=True)
            return

        try:
            cursor = connection.cursor()
            # check if the user's discord id already exists in the table
            discord_id = ctx.author.id  # Discord ID of the user
            cursor.execute("SELECT steam_id_64 FROM discord WHERE discord_id = %s", (discord_id,))
            result = cursor.fetchone()

            if result:
                # update the steam id if the discord id exists
                cursor.execute("UPDATE discord SET steam_id_64 = %s WHERE discord_id = %s", (steam_id, discord_id))
            else:
                # insert a new row if the discord id doesn't exist
                cursor.execute("INSERT INTO discord (discord_id, steam_id_64) VALUES (%s, %s)", (discord_id, steam_id))

            connection.commit()
            await ctx.send("Your Steam ID has been successfully added.", ephemeral=True)

        except mysql.connector.Error as err:
            await ctx.send(f"Database error: {err}", ephemeral=True)

        finally:
            cursor.close()
            connection.close()    
        

    @commands.hybrid_command(description='Shows player profile.')
    async def stats(self, ctx, steam_id: str = None):   
        await ctx.send("Test Message 1")
        connection = connect_to_database()  
        await ctx.send("Test Message 2")
        if not connection:
            await ctx.send("Failed to connect to the database.", ephemeral=True)
            return

        # If steam_id is not provided, try to get it from the discord table
        if not steam_id:
            discord_id = ctx.author.id  # discord id of the user
            cursor = connection.cursor()
            cursor.execute("SELECT steam_id_64 FROM discord WHERE discord_id = %s", (discord_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                steam_id = result[0]  # use the linked steam id
            else:
                await ctx.send("Please provide a Steam ID or link your Steam ID using /addprofile.", ephemeral=True)
                return

        cursor = connection.cursor()

        # Fetch basic player info
        player_info_query = "SELECT player_name, total_kills, total_deaths, total_time_seconds FROM players WHERE steam_id_64 = %s"
        cursor.execute(player_info_query, (steam_id,))
        player_info = cursor.fetchone()
        if not player_info:
            await ctx.send("Player not found.", ephemeral=True)
            return

        player_name, total_kills, total_deaths, total_time_seconds = player_info
        play_time_hours = total_time_seconds // 3600  # Convert seconds to hours

        # Fetch favorite weapon
        favorite_weapon_query = """
            SELECT weapon_name, SUM(kills) as total_kills
            FROM weapon_performance
            WHERE steam_id_64 = %s
            GROUP BY weapon_name
            ORDER BY total_kills DESC
            LIMIT 1
        """
        cursor.execute(favorite_weapon_query, (steam_id,))
        favorite_weapon_result = cursor.fetchone()
        favorite_weapon = favorite_weapon_result[0] if favorite_weapon_result else "N/A"

        # Fetch highest kill game
        highest_kill_game_query = "SELECT MAX(kills) FROM player_matches WHERE steam_id_64 = %s"
        cursor.execute(highest_kill_game_query, (steam_id,))
        highest_kill_game_result = cursor.fetchone()
        highest_kill_game = highest_kill_game_result[0] if highest_kill_game_result else 0

        # Fetch highest kill streak
        highest_kill_streak_query = "SELECT MAX(kills_streak) FROM player_matches WHERE steam_id_64 = %s"
        cursor.execute(highest_kill_streak_query, (steam_id,))
        highest_kill_streak_result = cursor.fetchone()
        highest_kill_streak = highest_kill_streak_result[0] if highest_kill_streak_result else 0

        profile_message = (
            f"Username: {player_name}\n"
            f"Total Kills: {total_kills}\n"
            f"Total Deaths: {total_deaths}\n"
            f"Favorite Weapon: {favorite_weapon}\n"
            f"Highest Kill Game: {highest_kill_game}\n"
            f"Highest Kill Streak: {highest_kill_streak}\n"
            f"Play Time: {play_time_hours} hours\n"
        )

        # 'total', 'highscores', last 30 games, and link to profile
        view = discord.ui.View()
        view.add_item(Button(label="Total Stats", style=discord.ButtonStyle.primary, custom_id=f"total_stats_{steam_id}"))
        view.add_item(Button(label="Highscores", style=discord.ButtonStyle.secondary, custom_id=f"highscores_{steam_id}"))
        view.add_item(Button(label="Last 10 Games", style=discord.ButtonStyle.secondary, custom_id=f"history_{steam_id}"))
        view.add_item(Button(label="Best 10 Games", style=discord.ButtonStyle.secondary, custom_id=f"best_{steam_id}"))
        view.add_item(discord.ui.Button(label="HLL Stats Profile", url=f"https://www.hllstats.dev/?steam64id={steam_id}", style=discord.ButtonStyle.link))

        await ctx.send(profile_message, view=view, ephemeral=True)

    # button clicks for additional stats
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data["custom_id"]
            steam_id = custom_id.split('_')[-1]  # extract the steam_id from the custom_id

            if "total_stats" in custom_id:
                # Calculate and send total stats
                message = await calculate_total_stats(steam_id)
                await interaction.response.send_message(message, ephemeral=True)

            elif "highscores" in custom_id:
                # Calculate and send highscores
                message = await calculate_highscores(steam_id)
                await interaction.response.send_message(message, ephemeral=True)
                
            elif "history" in custom_id:
                # Create a fake context object
                class FakeCtx:
                    def __init__(self, steam_id):
                        self.author = bot.user  # This should be the author of the interaction
                        self.channel = bot.get_channel(CHANNEL_ID)  # The channel where the interaction occurred
                        self.send = interaction.response.send_message  # Use interaction's send_message method
                        self.steam_id = steam_id
                
                # Call the history function with the fake context object
                fake_ctx = FakeCtx(steam_id)
                message = await history(fake_ctx, steam_id)
                
            elif "best" in custom_id:
                # Create a fake context object
                class FakeCtx:
                    def __init__(self, steam_id):
                        self.author = bot.user  # This should be the author of the interaction
                        self.channel = bot.get_channel(CHANNEL_ID)  # The channel where the interaction occurred
                        self.send = interaction.response.send_message  # Use interaction's send_message method
                        self.steam_id = steam_id
                
                # Call the history function with the fake context object
                fake_ctx = FakeCtx(steam_id)
                message = await best(fake_ctx, steam_id)
                
    async def calculate_total_stats(self, steam_id):
        connection = connect_to_database()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()

        # Fetch player's name
        cursor.execute("SELECT player_name FROM players WHERE steam_id_64 = %s", (steam_id,))
        name_result = cursor.fetchone()
        player_name = name_result[0] if name_result else "Unknown Player"

        total_stats_message = f"Total Stats for {player_name} ({steam_id}):\n"

        # Fetch total kills, deaths, and streaks
        cursor.execute(
            "SELECT SUM(kills), SUM(deaths), MAX(kills_streak), MAX(deaths_without_kill_streak) FROM player_matches WHERE steam_id_64 = %s",
            (steam_id,)
        )
        result = cursor.fetchone()
        if result:
            total_kills, total_deaths, longest_kill_streak, longest_death_streak = result
            total_stats_message += f"Kills: {total_kills} kills\nDeaths: {total_deaths} kills\nLongest Killstreak: {longest_kill_streak} kills\nLongest Deathstreak: {longest_death_streak} kills\n"

        # Fetch favorite weapon
        cursor.execute(
            """
            SELECT weapon_name, SUM(kills) as total_kills
            FROM weapon_performance
            WHERE steam_id_64 = %s
            GROUP BY weapon_name
            ORDER BY total_kills DESC
            LIMIT 1
            """,
            (steam_id,)
        )
        favorite_weapon_result = cursor.fetchone()
        favorite_weapon = favorite_weapon_result[0] if favorite_weapon_result else "N/A"
        total_stats_message += f"Favorite Weapon: {favorite_weapon}\n"

        # Fetch highest kill game
        cursor.execute(
            "SELECT MAX(kills) FROM player_matches WHERE steam_id_64 = %s",
            (steam_id,)
        )
        highest_kill_game_result = cursor.fetchone()
        highest_kill_game = highest_kill_game_result[0] if highest_kill_game_result else 0
        total_stats_message += f"Highest Kill Game: {highest_kill_game}\n"

        # Fetch play time
        cursor.execute(
            "SELECT SUM(time_seconds) FROM player_matches WHERE steam_id_64 = %s",
            (steam_id,)
        )
        play_time_result = cursor.fetchone()
        play_time = play_time_result[0] if play_time_result else 0
        total_stats_message += f"Play Time: {play_time // 3600} hours {play_time % 3600 // 60} minutes\n"
        
        # Fetch individual weapon stats
        for weapon in categories:
            if weapon not in weapon_categories:  # Ensure it's not a category
                cursor.execute(
                    "SELECT SUM(kills) FROM weapon_performance WHERE steam_id_64 = %s AND weapon_name = %s",
                    (steam_id, weapon)
                )
                weapon_result = cursor.fetchone()
                weapon_kills = weapon_result[0] if weapon_result and weapon_result[0] is not None else 0
                total_stats_message += f"{weapon}: {weapon_kills} kills\n"

        # Fetch category stats
        for category in weapon_categories:
            cursor.execute(
                "SELECT SUM(kills) FROM category_kills WHERE steam_id_64 = %s AND category_name = %s",
                (steam_id, category)
            )
            category_result = cursor.fetchone()
            category_kills = category_result[0] if category_result and category_result[0] is not None else 0
            total_stats_message += f"{category}: {category_kills} kills\n"

        connection.close()
        return total_stats_message

    async def calculate_highscores(self, steam_id):
        connection = connect_to_database()
        if not connection:
            return "Failed to connect to the database."

        cursor = connection.cursor()

        # Fetch player's name for highscores message
        cursor.execute("SELECT player_name FROM players WHERE steam_id_64 = %s", (steam_id,))
        name_result = cursor.fetchone()
        player_name = name_result[0] if name_result else "Unknown Player"

        message = f"Highscores for {player_name} ({steam_id}):\n"

        # Fetch player highscores for individual weapons and categories
        for item in categories:
            if item in weapon_categories.keys():  # If it's a category
                query = "SELECT MAX(kills) FROM category_kills WHERE steam_id_64 = %s AND category_name = %s"
            else:  # It's an individual weapon
                query = "SELECT MAX(kills) FROM weapon_performance WHERE steam_id_64 = %s AND weapon_name = %s"

            cursor.execute(query, (steam_id, item))
            result = cursor.fetchone()
            if result and result[0] is not None:
                message += f"{item}: {result[0]} kills\n"

        return message
        
    @commands.hybrid_command(description='Shows the 10 best games (most kills) played by a player.')
    async def best(self, ctx, steam_id: str, server: str = None):
        connection = connect_to_database()
        if not connection:
            await ctx.send("Failed to connect to the database.", ephemeral=True)
            return

        cursor = connection.cursor()

        try:
            # Get the username associated with the provided Steam ID
            cursor.execute("SELECT player_name FROM players WHERE steam_id_64 = %s", (steam_id,))
            result = cursor.fetchone()
            username = result[0] if result else "Unknown Player"

            # query modified to optionally filter by server name
            query = f"""
                    SELECT 
                        pm.match_id,
                        m.server,
                        m.start_time,
                        m.map_name,
                        pm.kills,
                        pm.deaths,
                        TIMEDIFF(m.end_time, m.start_time) AS match_length,
                        (SELECT wp.weapon_name 
                         FROM weapon_performance wp 
                         WHERE wp.match_id = pm.match_id AND wp.server = m.server AND wp.steam_id_64 = pm.steam_id_64 
                         ORDER BY wp.kills DESC LIMIT 1) AS most_used_weapon
                    FROM 
                        player_matches pm
                    JOIN 
                        matches m ON pm.match_id = m.match_id AND pm.server = m.server
                    WHERE 
                        pm.steam_id_64 = %s
                        {"AND m.server = %s" if server else ""}
                        AND (pm.kills > 0 OR pm.deaths > 0)
                    ORDER BY 
                        pm.kills DESC
                    LIMIT 10
                """
            # Execute the query with or without the server name
            cursor.execute(query, (steam_id,) if not server else (steam_id, server))
            rows = cursor.fetchall()

            if not rows:
                await ctx.send("No games found for the specified Steam ID.", ephemeral=True)
                return

            # Create a formatted message with the retrieved data
            message = f"This is {username}'s 10 best games (most kills):\n"
            message += "```Match ID  | Server | Start Time           | Map Name                         | Match Length | Kills | Deaths | Most Used Weapon\n"
            for row in rows:
                match_id, server_name, start_time, map_name, kills, deaths, match_length, most_used_weapon = row
                start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else "N/A"
                most_used_weapon_str = most_used_weapon if most_used_weapon else "N/A"  
                match_length_str = str(match_length) 
                message += f"{match_id:<9} | {server_name:<6} | {start_time_str:<20} | {map_name:<32} | {match_length_str:<12} | {kills:<5} | {deaths:<6} | {most_used_weapon_str:<40}\n"
            message += "```"
            # Send the formatted message as a response
            await ctx.send(message, ephemeral=True)

        except Exception as e:
            await ctx.send(f"Error fetching data: {e}", ephemeral=True)

        finally:
            cursor.close()
            connection.close()
            
    @commands.hybrid_command(description='Shows the last 10 games played by a player.')
    async def history(self, ctx, steam_id: str, server: str = None):
        connection = connect_to_database()
        if not connection:
            await ctx.send("Failed to connect to the database.", ephemeral=True)
            return

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT player_name FROM players WHERE steam_id_64 = %s", (steam_id,))
            result = cursor.fetchone()
            username = result[0] if result else "Unknown Player"

            # filter by server if provided
            params = (steam_id, server) if server else (steam_id,)

            query = f"""
                SELECT 
                    pm.match_id,
                    m.server,
                    m.start_time,
                    m.map_name,
                    pm.kills,
                    pm.deaths,
                    TIMEDIFF(m.end_time, m.start_time) AS match_length,
                    (SELECT wp.weapon_name 
                     FROM weapon_performance wp 
                     WHERE wp.match_id = pm.match_id AND wp.server = m.server AND wp.steam_id_64 = pm.steam_id_64 
                     ORDER BY wp.kills DESC LIMIT 1) AS most_used_weapon
                FROM 
                    player_matches pm
                JOIN 
                    matches m ON pm.match_id = m.match_id AND pm.server = m.server
                WHERE 
                    pm.steam_id_64 = %s 
                    {"AND m.server = %s" if server else ""}
                    AND (pm.kills > 0 OR pm.deaths > 0)
                ORDER BY 
                    m.start_time DESC
                LIMIT 10
            """
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                await ctx.send("No games found for the specified Steam ID.", ephemeral=True)
                return

            message = f"This is {username}'s last 10 games:\n"
            message += "```Match ID  | Server | Start Time           | Map Name                         | Match Length | Kills | Deaths | Most Used Weapon\n"
            for row in rows:
                match_id, server_name, start_time, map_name, kills, deaths, match_length, most_used_weapon = row
                start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else "N/A"
                most_used_weapon_str = most_used_weapon if most_used_weapon else "N/A"
                match_length_str = str(match_length)
                message += f"{match_id:<9} | {server_name:<6} | {start_time_str:<20} | {map_name:<32} | {match_length_str:<12} | {kills:<5} | {deaths:<6} | {most_used_weapon_str:<40}\n"
            message += "```"
            await ctx.send(message, ephemeral=True)

        except Exception as e:
            await ctx.send(f"Error fetching data: {e}", ephemeral=True)

        finally:
            cursor.close()
            connection.close()

    @commands.hybrid_command(description='Lookup player IDs based on their username.')
    async def lookup(self, ctx, username: str):
        connection = connect_to_database()
        if not connection:
            await ctx.send("Failed to connect to the database.", ephemeral=True)
            return

        cursor = connection.cursor()

        try:
            # This query selects the last played game's server by joining on a subquery that finds the max end_time for each player
            query = """
                SELECT p.player_name, p.steam_id_64, m.server, m.end_time AS last_played_time
                FROM players p
                INNER JOIN (
                    SELECT pm.steam_id_64, MAX(m.end_time) AS max_end_time
                    FROM player_matches pm
                    INNER JOIN matches m ON pm.match_id = m.match_id AND pm.server = m.server
                    GROUP BY pm.steam_id_64
                ) AS last_game ON p.steam_id_64 = last_game.steam_id_64
                INNER JOIN player_matches pm ON p.steam_id_64 = pm.steam_id_64
                INNER JOIN matches m ON pm.match_id = m.match_id AND pm.server = m.server AND m.end_time = last_game.max_end_time
                WHERE p.player_name LIKE %s
                ORDER BY m.end_time DESC
                LIMIT 15
            """
            cursor.execute(query, (f"%{username}%",))
            results = cursor.fetchall()

            if not results:
                await ctx.send("No matching usernames found.", ephemeral=True)
                return

            response = "```\nPlayer Name          | Player ID                            | Last Server | Last Played\n"
            for result in results:
                player_name, steam_id_64, last_server, last_played_time = result
                response += f"{player_name.ljust(21)}| {steam_id_64.ljust(37)}| {last_server.ljust(12)}| {last_played_time}\n"

            response += "```"
            await ctx.send(f"Matching players:\n{response}", ephemeral=True)

        except Exception as e:
            await ctx.send(f"Error fetching data: {e}", ephemeral=True)

        finally:
            cursor.close()
            connection.close()


    @commands.hybrid_command(description='Shows weapon-specific or category-specific statistics.')
    async def weapons(self, ctx, weapon_name: str, steam_id: str):
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            
            # Check if the weapon_name is a category
            if weapon_name in weapon_categories:
                # Fetch category kills
                query = "SELECT SUM(kills) FROM category_kills WHERE steam_id_64 = %s AND category_name = %s"
                cursor.execute(query, (steam_id, weapon_name))
            else:
                # Fetch specific weapon kills
                query = "SELECT SUM(kills) FROM weapon_performance WHERE steam_id_64 = %s AND weapon_name = %s"
                cursor.execute(query, (steam_id, weapon_name))

            result = cursor.fetchone()
            if result and result[0] is not None:
                total_kills = result[0]
                await ctx.send(f"Steam ID {steam_id} - Total kills with {weapon_name}: {total_kills}", ephemeral=True)
            else:
                await ctx.send(f"No data found for Steam ID {steam_id} with weapon {weapon_name}.", ephemeral=True)
        else:
            await ctx.send("Failed to connect to the database.", ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(StatCommands(bot))
