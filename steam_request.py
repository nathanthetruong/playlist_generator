import requests
from api_key_handling import STEAM_KEY

# Parses a steam link to get the game's app_id
def parse_app_id(url):
    app_id = url.split('/')[4]
    if app_id.isdigit():
        return app_id
    else:
        return None

# Calls the steam api to get a list up to 50000 game requests
def get_multiple_games(max_results):
    # Handling out of bounds cases
    if max_results < 0:
        print("steam_request.py: get_multiple_games -> Minimum of 1 request, no action taken")
        return
    if max_results > 50000:
        print("steam_request.py: get_multiple_games -> Max of 50000 requests, setting max_results to 50000")
        max_results = 50000

    # Sets up request
    steam_api = "https://api.steampowered.com/IStoreService/GetAppList/v1/?include_games=true"
    params = {
        'key': STEAM_KEY,
        'include_games': True,
        'max_results': max_results
    }

    response = requests.get(steam_api, params=params)
    return response.json()

def get_game_by_app_id(app_id):
    game_api = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    response = requests.get(game_api)

    # Check if request was successful
    if response.status_code == 200:
        try:
            return response.json()

        # Default error case
        except:
            return None
    
    else:
        return None
    