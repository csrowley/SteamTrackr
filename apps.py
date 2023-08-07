from bs4 import BeautifulSoup
import requests

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