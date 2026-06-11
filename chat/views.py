from datetime import datetime
import random
import flask
import flask_login
from app.database import DATABASE
from auth.models import Groups, User


def handle_chat_page():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/registration')

    if flask.request.method == 'POST':
        action = flask.request.form.get("action")

        # создание чата
        if action == "create_chat":
            current_user_id = int(flask_login.current_user.id)

            existing_group = Groups.query.filter_by(owner_id=current_user_id).first()
            if existing_group:
                print(f"User {current_user_id} already owns a group!")
                return flask.redirect(flask.url_for('chat_page.handle_chat_page'))

            chosen_name = flask.request.form.get('custom_group_name')
            if not chosen_name or chosen_name.strip() == "":
                user_name = flask_login.current_user.username or f"User{current_user_id}"
                unique_suffix = random.randint(1000, 9999)
                chosen_name = f"Group {user_name} #{unique_suffix}"

            group = Groups(
                group_name = chosen_name,
                owner_id = current_user_id   
            )
            group.users.append(flask_login.current_user)

            DATABASE.session.add(group)
            DATABASE.session.commit()

            return flask.redirect(flask.url_for('chat_page.handle_chat_page'))

        # обновление профиля
        elif action == "update_profile":
            first_name = flask.request.form.get('first_name')
            if first_name == '': first_name = None
            last_name = flask.request.form.get('last_name')
            if last_name == '': last_name = None
            username = flask.request.form.get('username')
            if username == '': username = None

            gender = flask.request.form.get('gender')
            birth_date_str = flask.request.form.get('birth_date')
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None

            flask_login.current_user.first_name = first_name
            flask_login.current_user.last_name = last_name
            flask_login.current_user.gender = gender
            flask_login.current_user.birth_date = birth_date

            user = User.query.filter_by(username=username).first()
            if user and user.id != flask_login.current_user.id:
                print('Username already exists')
            else:
                flask_login.current_user.username = username

            DATABASE.session.commit()
            return flask.redirect(flask.url_for('chat_page.handle_chat_page'))

    current_user_id = int(flask_login.current_user.id)

    my_group = Groups.query.filter_by(owner_id=current_user_id).first()
    other_groups = Groups.query.filter(Groups.owner_id != current_user_id).all()

    return flask.render_template(
        'chat_page.html', 
        user=flask_login.current_user, 
        my_group=my_group,
        other_groups=other_groups
    )