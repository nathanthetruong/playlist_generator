import psycopg2
from psycopg2 import sql
from api_key_handling import PSQL_PASSWORD
from steam_request import parse_app_id, get_multiple_games, get_game_by_app_id


# Parses game json to get name and description
# Returns a dictionary of the name and description
def parse_game_json(app_id, game_data):
    name = game_data[app_id]['data']['name']
    description = game_data[app_id]['data']['detailed_description']
    return {'name': name, 'description': description}


# Loads game into the cursor to later commit
def load_game(cursor, app_id, name, description):
    try:
        # Used to see if this game is already in the database
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM Game WHERE app_id = %s"), (app_id,))
        count = cursor.fetchone()[0]

        # Game is already in the database
        if int(count) > 0:
            update_query = sql.SQL("""
                UPDATE Game
                SET name = %s, description = %s
                WHERE app_id = %s
            """)
            cursor.execute(update_query, (name, description, app_id))
            
        # Game isn't in the database yet
        else:
            insert_query = sql.SQL("""
                INSERT INTO Game (app_id, name, description)
                VALUES (%s, %s, %s)
            """)
            cursor.execute(insert_query, (app_id, name, description))

    # Default error case
    except Exception as e:
        print(f"database_input.py: load_game -> {e}")


# Handles loading multiple games into the database
def commit_multiple_games(max_results):
    # Starts connection to the database
    connection = psycopg2.connect(database="game_data_storage",
                            host="localhost",
                            user="nathan",
                            password=PSQL_PASSWORD,
                            port="5432")

    cursor = connection.cursor()

    # Gets the max_results of games and then loads the cursor with each Game table entry
    games = get_multiple_games(max_results)['response']['apps']
    for game in games:
        get_game_by_app_id(game['appid'])

    # Commits changes and closes the database connection
    connection.commit()
    cursor.close()
    connection.close()


# Handles loading a game into the database by url
def commit_game_by_url(url):
    # Starts connection to the database
    connection = psycopg2.connect(database="game_data_storage",
                            host="localhost",
                            user="nathan",
                            password=PSQL_PASSWORD,
                            port="5432")

    cursor = connection.cursor()

    # Handles loading the cursor with the Game table entry
    response = get_game_by_url(url)
    data = parse_game_json(response['app_id'], response['data'])
    load_game(cursor, response['app_id'], data['name'], data['description'])

    # Commits changes and closes the database connection
    connection.commit()
    cursor.close()
    connection.close()
