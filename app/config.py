import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    APP_NAME = os.getenv("APP_NAME")
    DEBUG = os.getenv("DEBUG")

settings = Settings()