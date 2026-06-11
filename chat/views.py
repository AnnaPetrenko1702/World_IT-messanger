import flask
from auth.models import User, Groups
import flask_login
from app.database import DATABASE
from datetime import datetime

import random
# def handle_chat_page():
#     if not flask_login.current_user.is_authenticated:
#         return flask.redirect('/registration')

#     if flask.request.method == 'POST':

#         action = flask.request.form.get("action")

#         if action == "create_chat":
#             group = Groups(
#                 group_name = f"Group {flask_login.current_user}",
#                 owner_id = flask_login.current_user.id   
#             )
#             group.users.append(flask_login.current_user)

#             print("sda;;ddas[d]as;d][as;[]das[]d;as[d;sa[]d[;]as;[sada]]]")

#             DATABASE.session.add(group)
#             DATABASE.session.commit()

#         elif action == "update_profile":
#             first_name = flask.request.form.get('first_name')
#             if first_name == '':
#                 first_name = None
#             last_name = flask.request.form.get('last_name')
#             if last_name == '':
#                 last_name = None
#             username = flask.request.form.get('username')
#             if username == '':
#                 username = None


            
#             gender = flask.request.form.get('gender')
#             birth_date_str = flask.request.form.get('birth_date')

#             print(birth_date_str)

#             birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None

#             print(birth_date)

#             flask_login.current_user.first_name = first_name
#             flask_login.current_user.last_name = last_name
#             flask_login.current_user.gender = gender
#             flask_login.current_user.birth_date = birth_date

#             user = User.query.filter_by(username=username).first()

#             if user:
#                 print('Username already exists')
#             else:
#                 flask_login.current_user.username = username

#             DATABASE.session.commit()

#             print(first_name, last_name, username, gender, birth_date)

#     return flask.render_template('chat_page.html', user=flask_login.current_user)



# from datetime import datetime
# import random
# import flask
# import flask_login
# from app.database import DATABASE
# from auth.models import Groups, User


# def handle_chat_page():
#     # Если юзер не авторизован — отправляем на регистрацию/логин
#     if not flask_login.current_user.is_authenticated:
#         return flask.redirect('/registration')

#     if flask.request.method == 'POST':
#         action = flask.request.form.get("action")

#         # --- СОЗДАНИЕ ЧАТА ---
#         if action == "create_chat":
#             # ИСПРАВЛЕНО: Принудительно извлекаем числовой ID, чтобы в БД не лез текстовый объект
#             current_user_id = int(flask_login.current_user.id)

#             # Проверяем, нет ли у юзера уже созданной группы по его числовому ID
#             existing_group = Groups.query.filter_by(owner_id=current_user_id).first()
            
#             if existing_group:
#                 print(f"User {current_user_id} already owns a group!")
#                 return flask.redirect(flask.url_for('chat_page.handle_chat_page'))

#             # Получаем название чата из текстового поля формы
#             chosen_name = flask.request.form.get('custom_group_name')

#             # Запасной вариант, если инпут пришел пустым
#             if not chosen_name or chosen_name.strip() == "":
#                 user_name = flask_login.current_user.username or f"User{current_user_id}"
#                 unique_suffix = random.randint(1000, 9999)
#                 chosen_name = f"Group {user_name} #{unique_suffix}"

#             # Создаем группу (owner_id получает строго INTEGER)
#             group = Groups(
#                 group_name = chosen_name,
#                 owner_id = current_user_id   
#             )
#             group.users.append(flask_login.current_user)

#             DATABASE.session.add(group)
#             DATABASE.session.commit()

#             return flask.redirect(flask.url_for('chat_page.handle_chat_page'))

#         # --- ОБНОВЛЕНИЕ ПРОФИЛЯ ---
#         elif action == "update_profile":
#             first_name = flask.request.form.get('first_name')
#             if first_name == '':
#                 first_name = None
#             last_name = flask.request.form.get('last_name')
#             if last_name == '':
#                 last_name = None
#             username = flask.request.form.get('username')
#             if username == '':
#                 username = None

#             gender = flask.request.form.get('gender')
#             birth_date_str = flask.request.form.get('birth_date')

#             birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None

#             flask_login.current_user.first_name = first_name
#             flask_login.current_user.last_name = last_name
#             flask_login.current_user.gender = gender
#             flask_login.current_user.birth_date = birth_date

#             user = User.query.filter_by(username=username).first()

#             # Проверяем, что найденный username принадлежит кому-то другому, а не нам
#             if user and user.id != flask_login.current_user.id:
#                 print('Username already exists')
#             else:
#                 flask_login.current_user.username = username

#             DATABASE.session.commit()

#             return flask.redirect(flask.url_for('chat_page.handle_chat_page'))

#     # --- ЗДЕСЬ ОБРАБАТЫВАЕТСЯ GET-ЗАПРОС ---
#     # ИСПРАВЛЕНО: Ищем по числовому ID текущего пользователя
#     current_user_id = int(flask_login.current_user.id)
#     user_group = Groups.query.filter_by(owner_id=current_user_id).first()

#     # Передаем и пользователя (user), и его группу (my_group) в HTML
#     return flask.render_template(
#         'chat_page.html', 
#         user=flask_login.current_user, 
#         my_group=user_group
#     )

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

        # --- СОЗДАНИЕ ЧАТА ---
        if action == "create_chat":
            current_user_id = int(flask_login.current_user.id)

            # Ограничение: один пользователь — один личный чат под заголовком
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

        # --- ОБНОВЛЕНИЕ ПРОФИЛЯ ---
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

    # --- ЛОГИКА РАЗДЕЛЕНИЯ ЧАТОВ ДЛЯ GET-ЗАПРОСА ---
    current_user_id = int(flask_login.current_user.id)

    # 1. Находим ЛИЧНЫЙ чат текущего пользователя
    my_group = Groups.query.filter_by(owner_id=current_user_id).first()

    # 2. Находим ВСЕ ОСТАЛЬНЫЕ чаты, где owner_id НЕ равен ID текущего пользователя
    other_groups = Groups.query.filter(Groups.owner_id != current_user_id).all()

    return flask.render_template(
        'chat_page.html', 
        user=flask_login.current_user, 
        my_group=my_group,
        other_groups=other_groups
    )