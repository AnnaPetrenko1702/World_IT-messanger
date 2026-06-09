import flask
from auth.models import User
import flask_login

def handle_chat_page():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/registration')

    return flask.render_template('chat_page.html')
    