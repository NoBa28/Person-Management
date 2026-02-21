from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = "person_management_db"

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS")
}
