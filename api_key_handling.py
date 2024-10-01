import os
from dotenv import load_dotenv

# Loads .env file
load_dotenv()

# Stores all the keys and credentials
PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
STEAM_KEY = os.getenv('STEAM_API_KEY')