import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    db = mysql.connector.connect(
        host = "localhost",
        user = f"{os.getenv('USER')}",
        passwd = f"{os.getenv('PASSWORD')}",
        database = f"{os.getenv('DATABASE')}"
    )

    return db