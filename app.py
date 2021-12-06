from flask import Flask, render_template, g, request, session
import sqlite3 as sql

from werkzeug.utils import redirect

from helpers import find_monster

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
        monsters = db.fetchall()

        for monster in monsters:
            print(monster["name"])

    except:
        return render_template("oops.html")

    return render_template("index.html", monsters=monsters)

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