import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()
def connect_to_database():
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    try:
        connection = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None