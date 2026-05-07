import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "AI System")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

settings = Settings()
