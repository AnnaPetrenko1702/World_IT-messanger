import flask_socketio
import flask
from auth.models import Groups , Message 
from app.settings import app , socket
from app.database import DATABASE
import flask_login
from .app import online_users


@socket.on('connect')
def handle_connect(auth=None):
    print('Connected')

    user_id = flask_login.current_user.id

    if user_id in online_users:
        online_users[user_id].add(flask.request.sid)
    else:
        online_users[user_id] = set()
        online_users[user_id].add(flask.request.sid)


@socket.on('disconnect')
def handle_disconnect():
    print('Disconnected')

    user_id = flask_login.current_user.id

    online_users[user_id].discard(flask.request.sid)
    if online_users[user_id] == set():
        del online_users[user_id]


@socket.on('join_room')
def handle_join_room(data):
    group_id = data.get('groupId')
    user_id = flask_login.current_user.id

    if not group_id:
        flask_socketio.emit('error', {'msg': 'groupId не передан'})
        return

    group = Groups.query.get(group_id)

    if not group:
        flask_socketio.emit('error', {'msg': 'группа не найдена'})
        return

    user_in_group = any(user.id == user_id for user in group.users)

    if user_in_group:
        flask_socketio.join_room(f'room_{group.id}')
        flask_socketio.emit('joined', {'room': f'room_{group.id}'})
        print(f'Пользователь {user_id} вошёл в room_{group.id}')

        # вот тут собираем и шлём статус участников
        data = {
            "title": group.group_name,
            "members": []
        }

        for user in group.users:
            if user.id in online_users:
                status = "online"
            else:
                status = "offline"
            data["members"].append({
    "status": status,
    "email": user.email,
    "username": user.username,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "color_r": user.color_r,
    "color_g": user.color_g,
    "color_b": user.color_b,
}) 

        flask_socketio.emit('display_status', data, to=f'room_{group.id}')

    else:
        flask_socketio.emit('error', {'msg': 'нет доступа'})

@socket.on('message')
def handle_message_event(data):
    # Безопасность
    if not flask_login.current_user.is_authenticated:
        flask_socketio.emit('error', {'msg': 'Ошибка отправки: вы не авторизованы'})
        return

    group_id = data.get('group_id')
    content = data.get('content', '').strip()
    
    if not content or not group_id:
        return

    current_user_name = flask_login.current_user.username 
    current_user_id = flask_login.current_user.id

    new_message = Message(content=content, group_id=int(group_id), user_id = current_user_id)
    DATABASE.session.add(new_message)
    DATABASE.session.commit()

    payload = {
        'message': content,
        'username': current_user_name,
        'user_id': current_user_id,
        'group_id': group_id
    }

    flask_socketio.emit('message', payload, to=f'room_{group_id}')