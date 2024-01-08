import flask
import hashlib
import database
import random
import time
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'key'

def shorten_url(url): # Function to Generate a Shorten URL
    timestamp = str(int(time.time()))
    random_number = str(random.randint(1, 1000))
    data = url + timestamp + random_number
    hash_object = hashlib.md5(data.encode())
    shorten_url = hash_object.hexdigest()[:5]
    return shorten_url

def create_session(username):
    session['username'] = username

def get_session_name():
    Username = session.get('username')
    return Username

@app.route('/<path:short_url>')
def red_2_Org(short_url):
    print(short_url)
    conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    url = database.Get_URL(short_url,conn)
    conn.close()
    if url:
        return flask.redirect(url)
    else:
        return render_template("error.html", Error_String = "NO URL FOUND")
    
@app.route('/Links')
def Load_List():
    conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    Links = database.Load_Links(get_session_name(),conn)
    return render_template("List.html", links = Links)


@app.route('/')
def home():
    Username = session.get('username')
    if Username:
        return render_template("home.html", Username_HTML = Username)
    else:
        return redirect(url_for("Login"))

@app.route('/DEL')
def Logout():
    session.pop('username', None)
    return render_template("error.html", Error_String = "Logout Complete")

@app.route('/Login',methods =["GET", "POST"])
def Login():
    if request.method == "POST":
        Username = request.form.get("USERNAME")
        Input_Password = request.form.get("PASSWORD")
        conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
        if database.Check_User(Username,conn):
            if database.Check_Password(Username,Input_Password,conn):
                create_session(Username)
                return redirect(url_for('home'))
            else:
                render_template("error.html", Error_String = "Wrong Password")
        else:
            if Input_Password:
                database.Add_User(Username,Input_Password,conn)
                create_session(Username)
                return redirect(url_for('home'))
            else:
                return render_template("error.html", Error_String = "No Password given")
    return render_template("login.html")

@app.route('/addroute',methods =["GET", "POST"])
def addroute():
    if request.method =="POST":
        URL = request.form.get("uURL")
        C_URL = request.form.get("uC_URL")
        if not(C_URL):    # Check if Custom URL Was Given if not give generated one
            C_URL = shorten_url(URL)      
        if not(URL):
            return render_template("error.html", Error_String = "There was no URL Given")
        conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
        database.check_if_Tabel_exist(conn)
        Username = get_session_name()
        User_ID = database.Get_User_id(Username,conn)
        if database.Check_URL(C_URL,conn):
            #conn.close()
            return render_template("error.html", Error_String = "Custom URL is already in use")
        database.Add_URL(URL, C_URL,User_ID,conn)
        conn.close()
    return redirect(C_URL + "/INFO")

@app.route("/<short_url>/INFO")
def showlink(short_url):
    conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    OG_URL = database.Get_URL(short_url,conn)
    conn.close()
    short_url = "http://127.0.0.1:5000/" + str(short_url)
    return render_template("info.html", Old_URL = OG_URL, New_URL = short_url )

@app.route('/delete_entry/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    database.Del_Link(entry_id,conn)
    conn.commit()
    conn.close()
    return redirect(url_for('Load_List'))


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host="0.0.0.0")
    #app.run()