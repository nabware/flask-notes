from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
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

    email = StringField(
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


# class LoginForm(FlaskForm):
#     """Form for logging a user in"""

#     # photo_url = StringField("Photo URL", validators=[URL()])

#     # notes = TextAreaField(
#     #     "Notes",
#     #     validators=[Optional()])

#     # available = BooleanField("Available")