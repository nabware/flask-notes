import os

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def home():
    """Redirects to register page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Returns register form or handles register form submit"""

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.register(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect(f"/users/{user.username}")

    return render_template("register.html", form=form)