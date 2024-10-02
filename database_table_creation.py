import psycopg2
from api_key_handling import PSQL_PASSWORD

connection = psycopg2.connect(database="game_data_storage",
                        host="localhost",
                        user="nathan",
                        password=PSQL_PASSWORD,
                        port="5432")

cursor = connection.cursor()

# Creates Game database table
create_table_query = """
CREATE TABLE IF NOT EXISTS Game (
    app_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
    );
"""

cursor.execute(create_table_query)

# Commits changes and closes the database connection
connection.commit()
cursor.close()
connection.close()