from config.mariadb_con import get_db_conn
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

def get_user(email):
    con = get_db_conn()
    cursor = con.cursor()
    query = "select id, name,email,password_hash from users where email = ?"
    try:

        cursor.execute(query,(email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        con.close()
    

def create_user(name,email,password):
    password_hash = password_hasher.hash(password)
    con = get_db_conn()
    cursor = con.cursor()
    query = "Insert into users (name,email,password_hash) values(?,?,?)"
    try:
        cursor.execute(query,(name,email,password_hash))
        con.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        con.close()

def email_validation(email):
    con = get_db_conn()
    try:
        cursor = con.cursor()
        query = "select email from users where email = ?"
        cursor.execute(query,(email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        con.close()
    
def verify_password(password_hash,password):
    password_hasher.verify(password_hash,password)
    return True