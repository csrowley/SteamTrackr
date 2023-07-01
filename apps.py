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



'''
import requests

def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]["success"]:
            game_data = data[str(app_id)]["data"]
            # Extract the information you need from game_data dictionary
            name = game_data["name"]
            price = game_data["price_overview"]["final_formatted"]
            discount_percent = game_data["price_overview"]["discount_percent"]
            # ...
            return name, price, discount_percent
        else:
            # Game data retrieval failed
            return None
    else:
        # Request failed
        return None

# Example usage
app_id = 730  # App ID for Counter-Strike: Global Offensive
game_info = get_game_details(app_id)
if game_info:
    name, price, discount_percent = game_info
    print("Game Name:", name)
    print("Price:", price)
    print("Discount:", discount_percent)
else:
    print("Failed to retrieve game information.")
'''