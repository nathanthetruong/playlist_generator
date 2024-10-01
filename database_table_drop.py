import psycopg2
from api_key_handling import PSQL_PASSWORD

connection = psycopg2.connect(database="game_data_storage",
                        host="localhost",
                        user="nathan",
                        password=PSQL_PASSWORD,
                        port="5432")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Game;")

# Commits changes and closes the database connection
connection.commit()
cursor.close()
connection.close()