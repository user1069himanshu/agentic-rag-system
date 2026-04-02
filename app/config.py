from dotenv import load_dotenv
import os

load_dotenv()  # THIS is critical

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("DEBUG KEY:", OPENAI_API_KEY[:10] if OPENAI_API_KEY else "NOT FOUND")