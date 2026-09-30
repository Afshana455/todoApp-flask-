from config.mariadb_con import get_db_conn
from datetime import datetime

def create_todo(user_id,title,description):
    con = get_db_conn()
    cursor = con.cursor()
    query = "Insert into todos(user_id,title,description) values(?,?,?)"
    try:
        cursor.execute(query,(user_id,title,description))
        con.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        con.close()
        
def get_todos(user_id,search=""):
    con = get_db_conn()
    cursor = con.cursor(dictionary=True)
    query = "select id ,title, description,completed,created_at,updated_at from todos where user_id=? and (title like ? or description like ?) order by created_at desc"
    search_text = f"%{search}%"
    try:
        cursor.execute(query,(user_id,search_text,search_text))
        return cursor.fetchall()
    finally:
        cursor.close()
        con.close()
    

def get_todo(todo_id, user_id):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, title, description, completed, created_at, updated_at FROM todos WHERE id = ? AND user_id = ?"
    try:
        cursor.execute(query, (todo_id, user_id))
       
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    

def update_todo(todo_id, user_id, title, description, completed):
    conn = get_db_conn()
    cursor = conn.cursor()
    query = " UPDATE todos SET title = ?,  description = ?, completed = ?,  updated_at = ? WHERE id = ?AND user_id = ?"
    try:
        cursor.execute(query, (title, description, completed,datetime.now(), todo_id, user_id))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
    

def delete_todo(todo_id, user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    query = " DELETE FROM todos WHERE id = ? AND user_id = ?"
    try:
        cursor.execute(query, (todo_id, user_id))
        affected_rows = cursor.rowcount
        conn.commit()
        return affected_rows
    finally:
        cursor.close()
        conn.close()

