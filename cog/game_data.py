from discord.ext import commands
from discord import app_commands,Interaction,Embed

from steam.webapi import WebAPI
from decouple import config
from apps import searchGameID
import json
from requests import request, Response

import requests
from bs4 import BeautifulSoup

KEY = config("STEAM_API_KEY")
api = WebAPI(key = KEY) 

class GamesCog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games Cog On")

    @app_commands.command(name = "checkifsale", description = "Check if a game is on sale!")
    @app_commands.describe(title = "Enter a game title with exact spelling")
    async def checkifsale(self, interaction: Interaction, title: str):
        try:
            appid = searchGameID(title,api)
            title_underscores = title.replace(' ', '_')

            response = request("get", "https://store.steampowered.com/api/appdetails", params={"appids": appid})
            json_loaded_response = json.loads(response.text)

            json_data = json.dumps(json_loaded_response)
    
            if(appid == ""):
                await interaction.response.send_message(f"Unfortunately {title} could not be found. Please enter the exact spelling of the game.")
                return
            
            mydata = json.loads(json_data)

            discount = mydata[str(appid)]['data']['price_overview']['discount_percent']
            game_price = mydata[str(appid)]['data']['price_overview']['final_formatted']
            game_link = f"https://store.steampowered.com/app/{appid}/{title_underscores}/"

            if(discount <= 0):
                await interaction.response.send_message(f"Sorry, {title} is not on sale. The current price is {game_price}. Check the official store page for more details: {game_link}")

                return
            
            await interaction.response.send_message(f"{title} is currently on sale for {game_price}. The discount is {discount}%. Check the official store page for more details: {game_link}")

        except Exception as e:
            await interaction.response.send_message(f"'{title}' could not be found.")


    @app_commands.command(name = "playercount", description = "Enter game title for current player count!")
    @app_commands.describe(title = "Game title must be spelled exactly")
    async def playercount(self, interaction: Interaction, title: str):

        appid = searchGameID(title,api)
        if(appid != 0):
            data = api.call(
            'ISteamUserStats.GetNumberOfCurrentPlayers',
            appid = appid)

            player_count = data["response"]["player_count"]
            await interaction.response.send_message(f"Player count is: {player_count:,}")

        else:
            await interaction.response.send_message(f"'{title}' could not be found.")


    @app_commands.command(name = "mostplayed", description = "Lists top n most played games. 35 MAX")
    @app_commands.describe(ceiling = "Amount of games to list. Max = 35")
    @app_commands.choices(hidden = [
        app_commands.Choice(name = "Hide", value = 1),
        app_commands.Choice(name = "Public", value = 2)
    ])
    async def mostplayed(self, interaction: Interaction, ceiling: str, hidden : app_commands.Choice[int]):
        max_titles = 35
        url = "http://steamspy.com/api.php?request=top100in2weeks"
        response  = requests.get(url)
        
        if response.status_code == 200:
            games = json.loads(response.content)

            rank = 1
            message = ""
            for id, data in games.items():
                if(rank > int(ceiling) or rank > max_titles): break

                if(len(message) >= 1850):
                    await interaction.response.send_message(message)
                    message = ""

                formatted_price = float(data['price']) / 100.0
                message += f"{rank}: {data['name']} - Price: ${formatted_price}"
                message += "\n"

                rank += 1
            
            await interaction.response.send_message(message, ephemeral= True if hidden.value == 1 else False)
        else:
            await interaction.response.send_message("Sorry, this command is currently down :(")
            print("error")
        
    
    @commands.command()
    async def topRated(self, ctx, ceiling):
        return


    @app_commands.command(name = "patchnotes", description = "Retrieves the most recent 'patch notes' news for a game")
    @app_commands.describe(gametitle = "Enter your game title with exact spelling")
    async def patchnotes(self, interaction: Interaction, gametitle: str):
        try:
            appids = searchGameID(gametitle, api)
            #https://store.steampowered.com/api/appdetails?appids={id} possibly use for thumbail

            news = api.call(
                "ISteamNews.GetNewsForApp",
                appid = appids,
                maxlength = 200,
                count = 1,
                tags = "patchnotes"
                )
            
            news_url = news['appnews']['newsitems'][0]['url']
            news_title = news['appnews']['newsitems'][0]['title']
            news_content = news['appnews']['newsitems'][0]['contents']

            if news_content == "":
                await interaction.response.send_message("No patch notes could be found.")
                return

            embed = Embed(title = gametitle, url = news_url, color = 0x774299)
            embed.set_thumbnail(url = "https://clan.akamai.steamstatic.com/images/4145017/5d65f58bf860dc2c64e56e0f440a5168afb4228c.png")
            embed.add_field(name = news_title, value = news_content, inline=False)
            embed.set_footer(text="Image does not represent acutal download size.")
            await interaction.response.send_message(embed=embed)
            

        except:
            await interaction.response.send_message("Error")

    

    #eventually implement epic games price tracking