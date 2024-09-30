import requests
from api_key_handling import STEAM_KEY

csgo_api = "https://api.steampowered.com/IStoreService/GetAppList/v1/?include_games=true"
params = {
    'key': STEAM_KEY,
    'include_games': True,
    'max_results': 50000
}

response = requests.get(csgo_api, params=params)
data = response.json()