import psycopg2
from psycopg2 import sql
from api_key_handling import PSQL_PASSWORD

connection = psycopg2.connect(database="game_data_storage",
                        host="localhost",
                        user="nathan",
                        password=PSQL_PASSWORD,
                        port="5432")

cursor = connection.cursor()


# Parses game json to get name and description
# Returns a dictionary of the name and description
def parse_game_json(app_id, game_data):
    name = game_data[app_id]['data']['name']
    description = game_data[app_id]['data']['detailed_description']
    return {'name': name, 'description': description}


# Loads game into the database
def load_game(cursor, app_id, name, description):
    try:
        insert_query = sql.SQL("""
            INSERT INTO Game (app_id, name, description)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, app_id, name, description)
    
    # Case where game is already in the Game table
    except psycopg2.IntegrityError:
        print(f"database_input.py: load_game -> Game with app_id {app_id} already exists")

    # Default error case
    except Exception as e:
        print(f"database_input.py: load_game -> {e}")

# Commits changes and closes the database connection
connection.commit()
cursor.close()
connection.close()