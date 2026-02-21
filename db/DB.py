import mysql.connector

from db.db_config import DB_CONFIG, DB_NAME


class DB:

    @staticmethod
    def connect(use_db=True):
        cfg = DB_CONFIG.copy()
        if use_db:
            cfg["database"] = DB_NAME
        return mysql.connector.connect(**cfg)
