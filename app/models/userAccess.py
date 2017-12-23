from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, app


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    userName = db.Column(db.String(60), index=True, unique=True)
    firstName = db.Column(db.String(60), index=True)
    lastName = db.Column(db.String(60), index=True)
    passwordHash = db.Column(db.String(128))
    perfilImageUrl = db.column()

    genderCheck = db.CheckConstraint("gender=='M' or gender=='F'")
    gender = db.Column(db.String(1), genderCheck)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))