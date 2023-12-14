import sqlite3
from sqlite3 import Error

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
    
def Add_URL(url,short_url,conn):
    cur = conn.cursor()
    cur.execute('''INSERT INTO url_mappings VALUES (?, ?)''', (short_url, url))
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

def main():
    conn = create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    print(Check_URL("77025e8d",conn))
    conn.close()

if __name__ == '__main__':
    main()