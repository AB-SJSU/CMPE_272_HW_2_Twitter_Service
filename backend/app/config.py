import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    API_BASE_URL = os.getenv("MASTODON_API_URL", "https://mastodon.social")
    ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN", "")