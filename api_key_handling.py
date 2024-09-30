import os
from dotenv import load_dotenv

# Loads .env file
load_dotenv()

# Stores all the API keys
steam_key = os.getenv('STEAM_API_KEY')