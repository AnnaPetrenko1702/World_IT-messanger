from app.database import DATABASE
import flask_login

class User(DATABASE.Model, flask_login.UserMixin):
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    email = DATABASE.Column(DATABASE.String, unique=True)
    password_hash = DATABASE.Column(DATABASE.String)
    first_name = DATABASE.Column(DATABASE.String)
    last_name = DATABASE.Column(DATABASE.String)
    username = DATABASE.Column(DATABASE.String, unique=True)
    avatar_path = DATABASE.Column(DATABASE.String)
    gender = DATABASE.Column(DATABASE.String)
    birth_date = DATABASE.Column(DATABASE.Date)
    is_verified = DATABASE.Column(DATABASE.Boolean, default = False)

    groups = DATABASE.relationship("Groups", secondary = "user_group", back_populates = "users")


class Groups(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    group_name = DATABASE.Column(DATABASE.String, unique = True)

    owner_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
    owner = DATABASE.relationship("User")

    users = DATABASE.relationship("User", secondary = "user_group", back_populates = "groups")


class UserGroup(DATABASE.Model):
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)

    user_id = DATABASE.Column(
    DATABASE.Integer,
    DATABASE.ForeignKey("user.id", name="fk_usergroup_user")
    )

    group_id = DATABASE.Column(
        DATABASE.Integer,
        DATABASE.ForeignKey("groups.id", name="fk_usergroup_group")
    )
