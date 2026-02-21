from db.DB import DB
from db.db_config import DB_NAME

def create_database():
    with DB.connect(use_db=False) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")


def create_address_table():
    with DB.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"USE {DB_NAME}")
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS address
                           (
                               id        INT AUTO_INCREMENT PRIMARY KEY,
                               street    VARCHAR(50),
                               house_num INT,
                               zip_code  VARCHAR(5),
                               city      VARCHAR(50),
                               country   VARCHAR(50)
                           )
                           """)
            conn.commit()


def create_person_table():
    with DB.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"USE {DB_NAME}")
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS person
                           (
                               id         INT AUTO_INCREMENT PRIMARY KEY,
                               first_name VARCHAR(50),
                               last_name  VARCHAR(50),
                               birth_date DATE,
                               mail       VARCHAR(50),
                               address_id INT NOT NULL,
                               FOREIGN KEY (address_id) REFERENCES address (id)
                                   ON DELETE CASCADE
                                   ON UPDATE CASCADE
                           )
                           """)
            conn.commit()
