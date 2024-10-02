import psycopg2
from psycopg2 import sql
from api_key_handling import PSQL_PASSWORD
from steam_request import parse_app_id, get_game_by_app_id


# Credentials for connecting to database
connection = psycopg2.connect(database="game_data_storage",
                        host="localhost",
                        user="nathan",
                        password=PSQL_PASSWORD,
                        port="5432")


# Parses game json to get name and description
# Returns a dictionary of the name and description
def parse_game_json(app_id, game_data):
    try:
        name = game_data[app_id]['data']['name']
        description = game_data[app_id]['data']['detailed_description']
    
    # Name or Description is missing
    except:
        name = None
        description = None

    return {'name': name, 'description': description}


# Loads game into the cursor to later commit
def load_game(cursor, app_id, name, description):
    try:
        insert_query = sql.SQL("""
            INSERT INTO Game (app_id, name, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (app_id) 
            DO UPDATE SET 
                name = EXCLUDED.name,
                description = EXCLUDED.description
        """)
        cursor.execute(insert_query, (app_id, name, description))
        print("Game Loaded into the Database")

    # Default error case
    except Exception as e:
        print(f"database_input.py: load_game -> {e}")


# Handles loading a game into the database by url
def commit_game_by_url(url):
    # Starts connection to the database
    cursor = connection.cursor()

    # Handles loading the cursor with the Game table entry
    app_id = parse_app_id(url)
    if app_id != None:
        response = get_game_by_app_id(app_id)
        if response != None:
            game_data = parse_game_json(app_id, response)
            if game_data['name'] != None and game_data['description'] != None:
                load_game(cursor, app_id, game_data['name'], game_data['description'])
            else:
                print("Invalid Game URL")
        else:
            print("Invalid Game URL")
    else:
        print("Invalid Game URL")

    # Commits changes and closes the database connection
    connection.commit()
    cursor.close()
    connection.close()


# DEPRECATED CODE

# # Handles loading multiple games into the database
# def commit_all_games():
#     # Starts connection to the database
#     cursor = connection.cursor()

#     # Gets the max_results of games and then loads the cursor with each Game table entry
#     games = get_all_games()['applist']['apps']
#     for game in games:
#         if game['appid'] != None:
#             response = get_game_by_app_id(game['appid'])
#             if response != None:
#                 game_data = parse_game_json(str(game['appid']), response)
#                 if game_data['name'] != None and game_data['description'] != None:
#                     load_game(cursor, game['appid'], game_data['name'], game_data['description'])

#     # Commits changes and closes the database connection
#     connection.commit()
#     cursor.close()
#     connection.close()