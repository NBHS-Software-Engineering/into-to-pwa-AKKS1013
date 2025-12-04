from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import database_manager as dbHandler
import hugging as hf
import json
import signal
import jinja2

app = Flask(__name__)

loggedinuser = "Fallback"

with open("tags.json", "r") as f:
    tags = json.load(f)


@app.route("/add.html", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if dbHandler.insertContact(email, password) == 0:
            return render_template("/add.html", is_done=True)
        else:
            return render_template("/add.html", unique=False)
    else:
        return render_template("/add.html")


@app.route("/dashboard.html", methods=["POST", "GET"])
def dashboard():
    if request.method == "POST":
        search = request.form["search"]
        tag = request.form["newtag"]
        global tags
        if tag != "" and tag not in tags:
            tags.append(tag)
        data = dbHandler.search(search, tag)
        return render_template(
            "/dashboard.html", content=data, user=loggedinuser, tags=tags)
    else:
        data = dbHandler.listNotes()
        for i in data:
            if i[4] == None:
                print(i)
                tag = hf.tag("Title: " + i[3] + " Text: " + i[2], tags)
                if tag["score"] > 0.5:
                    print(tag)
                    dbHandler.updatetag(i[0], tag["label"])
        data = dbHandler.listNotes()
        return render_template(
            "/dashboard.html", content=data, user=loggedinuser, tags=tags
        )


@app.route("/login.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if dbHandler.checkContact(email, password):
            global loggedinuser
            loggedinuser = email
            return redirect("/dashboard.html")
        else:
            loggedinuser = "Fallback"
            return render_template("/login.html", login=False)
    else:
        loggedinuser = "Fallback"
        return render_template("/login.html")


@app.route("/addnote.html", methods=["POST", "GET"])
def addnote():
    if request.method == "POST":
        text = request.form["text"]
        title = request.form["title"]
        if dbHandler.addnote(loggedinuser, text, title) == 0:
            data = dbHandler.listNotes()
            return redirect("/dashboard.html")
        else:
            return render_template("/addnote.html", error=True)
    else:
        return render_template("/addnote.html")


def save(signalNumber, frame):
    with open("tags.json", "w") as f:
        json.dump(tags, f)
    raise KeyboardInterrupt


signal.signal(signal.SIGINT, save)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
