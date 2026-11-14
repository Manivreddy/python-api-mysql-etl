"""Application configuration loaded from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "20"))

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "etl_database")
DB_USER = os.getenv("DB_USER", "etl_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "etl_password")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
