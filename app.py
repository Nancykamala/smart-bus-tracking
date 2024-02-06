from flask import Flask, render_template, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route("/")
def index():
    dashboard = request.cookies.get("dashboard")
    username = request.cookies.get("username")
    if dashboard == "true":
        if username is not None and User.query.filter_by(username=username).first():
            return render_template("dashboard.html", username=username, app_name='Smart Bus Tracking')
        else:
            return redirect("/register")
    else:
        return redirect("/register")

@app.route("/login")
def login():
    loggedIn = request.cookies.get("dashboard")
    if loggedIn == "true":
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register")
def signup():
    dashboard = request.cookies.get("dashboard")
    if dashboard == "true":
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/loginsubmit", methods=["POST"])
def loginsubmit():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user:
        if password == user.password:
            resp = make_response(render_template('cookie.html'))
            resp.set_cookie("dashboard", "true")
            resp.set_cookie("username", username)
            return resp
        else:
            return "Wrong password."
    else:
        return "Account not found."

@app.route("/createaccount", methods=["POST"])
def createaccount():
    newusername = request.form.get("newusername")
    newpassword = request.form.get("newpassword")
    if User.query.filter_by(username=newusername).first():
        return "Username taken."
    if newusername == "":
        return "Please enter a username."
    if newpassword == "":
        return "Please enter a password."
    user = User(username=newusername, password=newpassword)
    db.session.add(user)
    db.session.commit()
    resp = make_response(render_template('cookie.html'))
    resp.set_cookie("dashboard", "true")
    resp.set_cookie("username", newusername)
    return resp

@app.route("/logout")
def logout():
    resp = make_response(render_template('cookie.html'))
    resp.set_cookie("dashboard", "false")
    resp.set_cookie("username", "")
    return resp
try:
  users = User.query.all()
except:
  with app.app_context():
      db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
