import flask
import werkzeug.security as security
from .models import User
from app.db import db
import flask_login


def registration_view():
    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        filtred_user = User.query.filter_by(email=email).scalar()

        if not filtred_user:
            hashed_password = security.generate_password_hash(password)

            if password and email and len(password) >= 8:
                user = User(password_hash=hashed_password, email=email)
        
                db.session.add(user)
                db.session.commit()


                return flask.redirect('/auth')

    return flask.render_template('registration.html')

def auth_view():

    if flask.request.method == 'POST':

        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        filtred_user = User.query.filter_by(email=email).scalar()

        if filtred_user and security.check_password_hash(filtred_user.password_hash, password):
            flask_login.login_user(filtred_user)

            return flask.redirect('/')

    return flask.render_template('auth.html')