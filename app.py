from flask import Flask, render_template, g, request, session
import sqlite3 as sql
import json
import requests

API_HOME = "https://www.dnd5eapi.co/api/"

from werkzeug.utils import redirect

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Open and use SQLITE3 database connection with FLASK
DATABASE = 'buildbadguy.db'

@app.route("/")
def index():

    try:
        con = sql.connect(DATABASE)
        con.row_factory = sql.Row
        db = con.cursor()
        db.execute("SELECT * FROM monsters")
        my_monsters = db.fetchall()

    except:
        return render_template("oops.html")

    return render_template("index.html", my_monsters=my_monsters)

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":
        try:
            con = sql.connect(DATABASE)
            db = con.cursor()

            bg_name = request.form.get("bg_name")
            bg_class = request.form.get("bg_class")

            db.execute("INSERT INTO monsters (name, class) VALUES (?,?)", (bg_name, bg_class))
            con.commit()
            db.close()
        except:
            return redirect ("oops")

        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/oops")
def oops():

    return render_template("oops.html")

@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":
        monster = request.form.get("search_monster")

        monster_result = find_monster(monster)

        return render_template("search.html", monster_result=monster_result)

    else:
        return render_template("search.html")

def find_monster(monster_name):
    try:
        response = requests.get(f"{API_HOME}/monsters/")
        monster_list = response.json()

        for item in monster_list["results"]:
            if monster_name == item["name"]:
                monster = item["index"]
                new = requests.get(f"{API_HOME}/monsters/{monster}")
                return new.json()
    except:
        print("No Response")