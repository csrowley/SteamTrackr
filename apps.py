from bs4 import BeautifulSoup
import json
from requests import request, Response
from steam.webapi import WebAPI
from decouple import config
import requests

KEY = config("STEAM_API_KEY")
api = WebAPI(key = KEY) 

#fix search game with python api method 
#https://store.steampowered.com/search/suggest
def searchGameID(title: str, api) -> int:
    data = api.call('ISteamApps.GetAppList')
    game_list = data['applist']['apps']

    for game in game_list:
        if game["name"] == title:
            print(game["appid"])
            return game["appid"]
    
    return 0


def checkSaleEvents() -> str:
        all_sales = {"steam spring sale", "steam summer sale", "steam autumn sale", "steam winter sale", "halloween"}
        url = "https://store.steampowered.com/"
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, "html.parser")
        meta_desc = soup.find("meta", property="og:description")

        if meta_desc:
            desc = meta_desc["content"].lower()
            for sales in all_sales:
                if sales in desc:
                    return sales.title()
                
            return ""
        
def emojize(country: str) -> str:
    flag = ''.join(chr(ord(c) + 127397) for c in country.upper())
    return flag

def game_info(title: str) -> dict:
    info = {}
    try:
        appid = searchGameID(title,api)
        title_underscores = title.replace(' ', '_')

        response = request("get", "https://store.steampowered.com/api/appdetails", params={"appids": appid})
        json_loaded_response = json.loads(response.text)

        json_data = json.dumps(json_loaded_response)

        if(appid == ""):
            return {}
        
        mydata = json.loads(json_data)

        game_discount = mydata[str(appid)]['data']['price_overview']['discount_percent']
        game_original_price = mydata[str(appid)]['data']['price_overview']['initial_formatted']
        game_price = mydata[str(appid)]['data']['price_overview']['final_formatted']
        game_link = f"https://store.steampowered.com/app/{appid}/{title_underscores}/"

        info["discount"] = game_discount
        info["price"] = game_price
        info["link"] = game_link
        info["initial"] = game_original_price

        return info


    except Exception as e:
        return {}