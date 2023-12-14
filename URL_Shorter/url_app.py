import flask
import hashlib
import database
import random
import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def shorten_url(url): # Function to Generate a Shorten URL by hashing
    timestamp = str(int(time.time()))
    random_number = str(random.randint(1, 1000))
    
    data = url + timestamp + random_number
    hash_object = hashlib.md5(data.encode())
    
    shorten_url = hash_object.hexdigest()[:4]
    return shorten_url


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
    
@app.route('/')
def home():
    return render_template("home.html")
    
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

        if database.Check_URL(C_URL,conn):
            conn.close()
            return render_template("error.html", Error_String = "Custom URL is already in use")
    
        database.Add_URL(URL,C_URL,conn)
        conn.close()
    return redirect(C_URL + "/INFO")

@app.route("/<short_url>/INFO")
def showlink(short_url):
    conn = database.create_connection(r"C:\Projects\Python\URL_Shorter\Database\Short_Url.db")
    OG_URL = database.Get_URL(short_url,conn)
    conn.close()
    short_url = "http://127.0.0.1:5000/" + str(short_url)
    return render_template("info.html", Old_URL = OG_URL, New_URL = short_url )

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host="0.0.0.0")