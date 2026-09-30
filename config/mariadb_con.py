import os
import mariadb
from dotenv import load_dotenv

load_dotenv()

pool = mariadb.ConnectionPool(pool_name="todo_pool",pool_size=5,host= os.getenv("db_host"),port=int(os.getenv("db_port")),user=os.getenv("db_user"),password=os.getenv("db_password"),database=os.getenv("db_name"))

def get_db_conn():
    return pool.get_connection()

