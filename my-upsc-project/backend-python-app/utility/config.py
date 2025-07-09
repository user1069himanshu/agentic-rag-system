# utility/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file into the environment

def get_gemini_api_key():
    return os.getenv("GEMINI_API_KEY")