from config.mariadb_con import get_db_conn
con = get_db_conn()
cursor = con.cursor()

cursor.execute("insert into users (name,email,password_hash) values (?,?,?)",("Mary","mary@gmail.com","sdfghjiuyt"))
con.commit()
print("executed")

cursor.close()
con.close()