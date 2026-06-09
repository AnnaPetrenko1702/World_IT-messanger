from app.database import DATABASE
import flask_login

class User(DATABASE.Model, flask_login.UserMixin):
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    email = DATABASE.Column(DATABASE.String, unique=True)
    password_hash = DATABASE.Column(DATABASE.String)
    first_name = DATABASE.Column(DATABASE.String)
    last_name = DATABASE.Column(DATABASE.String)
    avatar_path = DATABASE.Column(DATABASE.String)
    gender = DATABASE.Column(DATABASE.String)
    birth_date = DATABASE.Column(DATABASE.Date)
    is_verified = DATABASE.Column(DATABASE.Boolean, default = False)
