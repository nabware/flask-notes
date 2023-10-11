import os
from werkzeug.exceptions import Unauthorized

from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterUserForm, LoginForm, CSRFProtectForm, NoteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

SESSION_USERNAME_KEY = 'username'


@app.get("/")
def home():
    """Redirects to register page"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Returns register form and handles register form submit"""

    if SESSION_USERNAME_KEY in session:
        return redirect(f"/users/{session[SESSION_USERNAME_KEY]}")

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(
            username=username,
            pwd=pwd,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        session[SESSION_USERNAME_KEY] = user.username

        return redirect(f"/users/{user.username}")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Returns login form and handles login form submit"""

    if SESSION_USERNAME_KEY in session:
        return redirect(f"/users/{session[SESSION_USERNAME_KEY]}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username=username, pwd=pwd)

        if user:
            session[SESSION_USERNAME_KEY] = user.username

            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username and/or password']

    return render_template("login.html", form=form)


@app.get('/users/<string:username>')
def show_user_page(username):
    """Returns user's page or redirects to login page"""

    # this allows wekzug lib to deal with unauthorized access
    # if SESSION_USERNAME_KEY not in session:
    #     raise Unauthorized()

    if SESSION_USERNAME_KEY not in session:
        flash('You must be logged in to view!')
        return redirect('/login')

    elif session[SESSION_USERNAME_KEY] != username:
        flash("That's illegal!")
        return redirect(f'/users/{session["username"]}')

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    return render_template('user-details.html', user=user, form=form)


@app.post('/logout')
def logout():
    """Log out current user and redirect to home page"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(SESSION_USERNAME_KEY, None)
    else:
        raise Unauthorized()

    return redirect("/")

@app.post('/users/<string:username>/delete')
def delete_user(username):
    """Deletes user"""

    if SESSION_USERNAME_KEY not in session:
        flash('You must be logged in to view!')
        return redirect('/login')

    elif session[SESSION_USERNAME_KEY] != username:
        flash("That's illegal!")
        return redirect(f'/users/{session["username"]}')

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    if form.validate_on_submit():
        for note in user.notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        session.pop(SESSION_USERNAME_KEY, None)
    else:
        raise Unauthorized()

    return redirect("/")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """Returns add note form and handles note form submit"""

    if SESSION_USERNAME_KEY not in session:
        flash('You must be logged in to view!')
        return redirect('/login')

    elif session[SESSION_USERNAME_KEY] != username:
        flash("That's illegal!")
        return redirect(f'/users/{session["username"]}')

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner_username=username)

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add-note.html", form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Returns update note form and handles update note form submit"""

    note = Note.query.get_or_404(note_id)
    username = note.user.username

    if SESSION_USERNAME_KEY not in session:
        flash('You must be logged in to view!')
        return redirect('/login')

    elif session[SESSION_USERNAME_KEY] != username:
        flash("That's illegal!")
        return redirect(f'/users/{session["username"]}')

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("update-note.html", form=form, note=note)

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Deletes note"""

    note = Note.query.get_or_404(note_id)
    username = note.user.username

    if SESSION_USERNAME_KEY not in session:
        flash('You must be logged in to view!')
        return redirect('/login')

    elif session[SESSION_USERNAME_KEY] != username:
        flash("That's illegal!")
        return redirect(f'/users/{session["username"]}')

    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return redirect("/")