import requests
from api_key_handling import STEAM_KEY

# Parses a steam link to get the game's app_id
def parse_app_id(url):
    try:
        app_id = url.split('/')[4]
        if app_id.isdigit():
            return app_id
        else:
            return None
    
    # Default error case
    except:
        return None


# Calls the steam api to get information on inputted games
def get_game_by_app_id(app_id):
    game_api = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(game_api, params={"language": "english"})

    # Check if request was successful
    if response.status_code == 200:
        try:
            return response.json()

        # Default error case
        except:
            return None
    
    elif response.status_code == 429:
        print("steam_request.py: get_game_by_app_id -> Rate limit exceeded")
        return None

    else:
        return None


# DEPRECATED CODE

# # Calls the steam api to get all games
# def get_all_games():
#     steam_api = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
#     response = requests.get(steam_api)
#     return response.json()