from discord.ext import commands
from steam.webapi import WebAPI
from decouple import config
from collections import OrderedDict
from apps import searchGameID
import json
from requests import request, Response
import requests


KEY = config("STEAM_API_KEY")
api = WebAPI(key = KEY)

class GamesCog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def checkIfSale(self, ctx, *, title):
        try:
            appid = searchGameID(title,api)
            title_underscores = title.replace(' ', '_')

            response = request("get", "https://store.steampowered.com/api/appdetails", params={"appids": appid})
            json_loaded_response = json.loads(response.text)

            json_data = json.dumps(json_loaded_response)
    
            if(appid == ""):
                await ctx.reply(f"Unfortunately {title} could not be found. Please enter the exact spelling of the game.")
                return
            mydata = json.loads(json_data)

            discount = mydata[str(appid)]['data']['price_overview']['discount_percent']
            game_price = mydata[str(appid)]['data']['price_overview']['final_formatted']
            game_link = f"https://store.steampowered.com/app/{appid}/{title_underscores}/"

            if(discount <= 0):
                await ctx.reply(f"Sorry, {title} is not on sale. The current price is {game_price}. Check the official store page for more details: {game_link}")

                return
            
            await ctx.reply(f"{title} is currently on sale for {game_price}. The discount is {discount}%. Check the official store page for more details: {game_link}")

        except Exception as e:
            await ctx.reply(f"'{title}' could not be found.")

    @commands.command()
    async def playerCount(self, ctx, *, title):

        appid = searchGameID(title,api)
        if(appid != 0):
            data = api.call(
            'ISteamUserStats.GetNumberOfCurrentPlayers',
            appid = appid)

            player_count = data["response"]["player_count"]
            await ctx.reply(f"Player count is: {player_count:,}")

        else:
            await ctx.reply(f"'{title}' could not be found.")
            

    #@commands.command()
    #async def setEventReminder(self,ctx, switch):
