from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from instance.config import app_config

# --------------------------------
# -- User
# --------------------------------


class User(db.Model):



    __tablename__ = 'users'

    # Define the columns / user attributes

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    bucketlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):

        try:
            # Set up a payload with an experation time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            # Create the byte string token using the payload and secret key
            jwt_string = jwt.encode(
                payload,
                app_config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:

            # Return an error in string format
            return str(e)

    @staticmethod
    def decode_token(token):

        try:
            payload = jwt.decode(token, app_config.get('SECRET'))
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"

        except jwt.InvalidTokenError:
            return "Invalid Token. Please register or login"


# --------------------------------
# The Bucketlist
# --------------------------------

class Bucketlist(db.Model):

    __tablename__ = 'bucketlists' #Should always be plural

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    # Instantiate New Database with User Id
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)

    @staticmethod
    def get_all(user_id):
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)
