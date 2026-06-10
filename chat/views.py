import flask
from auth.models import User, Groups
import flask_login
from app.database import DATABASE
from datetime import datetime


def handle_chat_page():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/registration')

    if flask.request.method == 'POST':

        action = flask.request.form.get("action")

        if action == "create_chat":
            group = Groups(
                group_name = f"Group {flask_login.current_user}",
                owner_id = flask_login.current_user.id   
            )
            group.users.append(flask_login.current_user)

            print("sda;;ddas[d]as;d][as;[]das[]d;as[d;sa[]d[;]as;[sada]]]")

            DATABASE.session.add(group)
            DATABASE.session.commit()

        elif action == "update_profile":
            first_name = flask.request.form.get('first_name')
            if first_name == '':
                first_name = None
            last_name = flask.request.form.get('last_name')
            if last_name == '':
                last_name = None
            username = flask.request.form.get('username')
            if username == '':
                username = None


            
            gender = flask.request.form.get('gender')
            birth_date_str = flask.request.form.get('birth_date')

            print(birth_date_str)

            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None

            print(birth_date)

            flask_login.current_user.first_name = first_name
            flask_login.current_user.last_name = last_name
            flask_login.current_user.gender = gender
            flask_login.current_user.birth_date = birth_date

            user = User.query.filter_by(username=username).first()

            if user:
                print('Username already exists')
            else:
                flask_login.current_user.username = username

            DATABASE.session.commit()

            print(first_name, last_name, username, gender, birth_date)

    return flask.render_template('chat_page.html', user=flask_login.current_user)
    