import sqlite3 as sql
import os

name_db = 'users.db'
cur_dir = os.path.dirname(os.path.abspath(__file__))
path_db = os.path.join(cur_dir, name_db)

def create_db():
    if not os.path.exists(path_db):
        try:
            con = sql.connect(path_db)
            cur = con.cursor()
            cur.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        password TEXT,
                        temp_code INTEGER,
                        email TEXT
                        )
                ''')
            con.commit()
        except sql.Error as e:
            print('Ошибка БД: ' + str(e))

def create_user(username, password, email):
    try:
        con = sql.connect(path_db)
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", [username, password, email])
        con.commit()
    except sql.Error as e:
        print('Ошибка БД: ' + str(e))

def check_user(username):
    try:
        con = sql.connect(path_db)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", [username])
        user = cur.fetchone()
        con.close()
        return user
    except:
        return False
        
def get_users_data():
    con = sql.connect(path_db)
    cur = con.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    con.close()
    return users

def set_temp_code(username, temp_code):
    con = sql.connect(path_db)
    cur = con.cursor() 
    cur.execute("UPDATE users SET temp_code = ? WHERE username = ?", [temp_code, username])
    con.commit()
    con.close()

def get_temp_code(username):
    con = sql.connect(path_db)
    cur = con.cursor()
    cur.execute("SELECT temp_code FROM users WHERE username = ?", [username])
    temp_code = cur.fetchall()
    con.close()
    return temp_code