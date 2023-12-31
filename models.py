from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        db.CheckConstraint("LENGTH(password) >= 2"),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        db.CheckConstraint("LENGTH(email) >= 2"),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        db.CheckConstraint("LENGTH(first_name) >= 2"),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        db.CheckConstraint("LENGTH(last_name) >= 2"),
        nullable=False
    )

    notes = db.relationship('Note', backref='user')

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed pwd and return user"""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, pwd):
        """Authenticates user"""

        user = User.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user

        return False


class Note(db.Model):
    """Note"""

    __tablename__ = 'notes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),
        nullable=False,
    )


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)