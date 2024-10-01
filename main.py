from database_input import commit_game_by_url, commit_multiple_games

# url = input("Input a Steam Game URL: ")
# commit_game_by_url(url)

max_results = int(float(input("Input a Max Number of Results: ")))
commit_multiple_games(max_results)