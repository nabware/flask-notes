from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    """Form for registering user"""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(min=2, max=20)])

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=2, max=100)])

    email = EmailField(
        "Email",
        validators=[
            Email(),
            InputRequired(),
            Length(min=2, max=50)])

    first_name = StringField(
        'First Name',
        validators=[
            InputRequired(),
            Length(min=2, max=30)])

    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(),
            Length(min=2, max=30)])


class LoginForm(FlaskForm):
    """Form for logging a user in"""

    # validating length here may give attackers too much info

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(min=2, max=20)])

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=2, max=100)])

class CSRFProtectForm(FlaskForm):
    """Form for logging out"""

class NoteForm(FlaskForm):
    """Form for adding new note"""

    title = StringField(
        "Title",
        validators=[
            InputRequired(),
            Length(max=100)])

    content = TextAreaField(
        "Content",
        validators=[
            InputRequired()])
