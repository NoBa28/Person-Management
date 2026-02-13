import os

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "database": os.environ.get("DB_NAME")
}
