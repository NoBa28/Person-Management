import mysql.connector

from db.db_config import DB_CONFIG


def create_address_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
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
    cursor.close()
    conn.close()


def create_person_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS person
                   (
                       id         INT AUTO_INCREMENT PRIMARY KEY,
                       first_name VARCHAR(50),
                       last_name  VARCHAR(50),
                       birth_date DATE,
                       mail     VARCHAR(50),
                       address_id INT NOT NULL,
                       FOREIGN KEY (address_id) REFERENCES address (id)
                           ON DELETE CASCADE
                           ON UPDATE CASCADE
                   )
                   """)
    conn.commit()
    cursor.close()
    conn.close()
