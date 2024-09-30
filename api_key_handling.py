import os
from dotenv import load_dotenv

# Loads .env file
load_dotenv()

# Stores all the API keys
STEAM_KEY = os.getenv('STEAM_API_KEY')