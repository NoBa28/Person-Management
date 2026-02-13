import mysql.connector

from db.db_config import DB_CONFIG


def create_address_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS address
                   (
                       ID        INT AUTO_INCREMENT PRIMARY KEY,
                       STREET    VARCHAR(50),
                       HOUSE_NUM INT,
                       ZIP_CODE  VARCHAR(5),
                       CITY      VARCHAR(50),
                       COUNTRY   VARCHAR(50)
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
                       ID         INT AUTO_INCREMENT PRIMARY KEY,
                       FIRST_NAME VARCHAR(50),
                       LAST_NAME  VARCHAR(50),
                       BIRTH_DATE DATE,
                       E_MAIL     VARCHAR(50),
                       ADDRESS_ID INT NOT NULL,
                       FOREIGN KEY (ADDRESS_ID) REFERENCES address (ID)
                           ON DELETE CASCADE
                           ON UPDATE CASCADE
                   )
                   """)
