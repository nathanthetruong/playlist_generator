from database_input import commit_game_by_url
from steam_request import get_multiple_games

# url = input("Input a Steam Game URL: ")
# commit_game_by_url(url)

print(get_multiple_games(4)['response']['apps'][0]['appid'])