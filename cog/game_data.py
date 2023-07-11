from discord.ext import commands
from steam.webapi import WebAPI
from decouple import config
from collections import OrderedDict
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
            
    #possibly use "on_scheduled_event" ?
    #scrape the steam official news tab for possible sales
    @commands.command()
    async def setEventReminder(self,ctx, switch):
        all_sales = {"steam spring sale", "steam summer sale", "steam autumn sale", "steam winter sale", "halloween"}
        url = "https://store.steampowered.com/"
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, "html.parser")
        meta_desc = soup.find("meta", property="og:description")

        

        if meta_desc:
            desc = meta_desc["content"].lower()
            for sales in all_sales:
                if sales in desc:
                    await ctx.reply(sales.title())
                    return

    #DB method
    @commands.Cog.listener()
    async def on_steam_event_sale(self,ctx,user):
        months_active = [1,3,6,7,10,11,12]
            
    #DB method
    @commands.Cog.listener()
    async def on_game_sale(self,ctx,user,title):
        print("")


    @commands.command()
    async def mostPlayed(self, ctx, ceiling):
        max_titles = 35
        url = "https://steamspy.com/api.php?request=top100in2weeks"
        response  = requests.get(url)
        games = json.loads(response.content)

        rank = 1
        message = ""
        for id, data in games.items():
            if(rank > int(ceiling) or rank > max_titles): break

            if(len(message) >= 1850):
                await ctx.reply(message)
                message = ""

            formatted_price = float(data['price']) / 100.0
            message += f"{rank}: {data['name']} - Price: ${formatted_price}"
            message += "\n"

            rank += 1
        
        await ctx.reply(message)

    
    @commands.command()
    async def topRated(self, ctx, ceiling):
        return
    
    #implement a news functionality
    #eventually implement epic games price tracking