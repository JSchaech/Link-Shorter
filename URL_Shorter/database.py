import sqlite3
from sqlite3 import Error
import bcrypt

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def check_if_Tabel_exist(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS url_mappings (
        short_url TEXT PRIMARY KEY,
        original_url TEXT
    )'''
    cur.execute(sql)
    print("Tabel Created")
    
def Add_URL(url,short_url,user_id,conn):
    cur = conn.cursor()
    cur.execute('''INSERT INTO url_mappings VALUES (?, ?, ?)''', (short_url, url,user_id))
    conn.commit()
    print("URL Commited")

def Get_URL(short_url,conn):
    cur = conn.cursor()
    cur.execute('''SELECT original_url from url_mappings
                    WHERE short_url = ? ''', (short_url,))
    res_url = cur.fetchone()
    if res_url:
        res_url = res_url[0]
    return res_url

def Check_URL(short_url,conn):
    cur = conn.cursor()
    cur.execute('''SELECT short_url from url_mappings
                    WHERE short_url = ? ''', (short_url,))
    res_url = cur.fetchone()
    if res_url is not None:
        return True
    else:
        return False

def Add_User(Username,Password,conn):
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt())
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username=?",(Username,))
    result = cur.fetchone()
    if result:
        print("USER IS ALLREADY TAKEN")
        return False
    cur.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)",(Username,hashed_password))
    conn.commit()
    print("USER ADDED")

def Check_Password(Username,Password,conn):
    cur = conn.cursor()
    cur.execute("SELECT hashed_password FROM users WHERE username=?",(Username,))
    result = cur.fetchone()

    if result:
        hashed_password_from_db = result[0]

        Input_Password = Password
        Password_Correct = bcrypt.checkpw(Input_Password.encode("utf-8"), hashed_password_from_db)

        if (Password_Correct):
            return True
        else:
            return False
        
    else:
        return False
    
def Check_User(Username,conn):
    cur = conn.cursor()
    cur.execute("SELECT username from users WHERE username= ?",(Username,))
    result = cur.fetchone()

    if result:
        return True
    else:
        return False

def Get_User_id(Username,conn):
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username=?",(Username,))
    result = cur.fetchone()
    if result:
        return result[0]

def Load_Links(Username,conn):
    User_id = Get_User_id(Username,conn)
    cur = conn.cursor()
    cur.execute("SELECT short_url, original_url FROM url_mappings WHERE user_id =?",(User_id,))
    result = cur.fetchall()
    return result

def main():
    conn = create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    Add_User("Floo","Hallo",conn)
    print(Check_Password("Floo","Hallo",conn))
    #Add_User("Justn","12345",conn)
    conn.close()

def Del_Link(short_url,conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM url_mappings WHERE short_url =?",(short_url,))
    return "entry deleted"


if __name__ == '__main__':
    main()