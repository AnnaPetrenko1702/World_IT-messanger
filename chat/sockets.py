import flask_socketio
import flask
from auth.models import Groups , Message 
from app.settings import app , socket
from app.database import DATABASE
import flask_login
from .app import online_users


@socket.on('connect')
def handle_connect():
    print('Connected')
    user_id = flask_login.current_user.id

    if user_id in online_users:
        online_users[user_id].add(flask.request.sid)
    else:
        online_users[user_id] = set()
        online_users[user_id].add(flask.request.sid)

    group = Groups.query.get(1)
    if group:
        data = {
            "title" : group.group_name,
            "members" : []
        }

        users = group.users

        for user in users:
            if user.id in online_users.keys():
                status = "online"
            else:
                status = "offline"
            data["members"].append({
                "status" : status,
                "email" : user.email,
            })
        print(12366666666666666)
        
        flask_socketio.emit('group_status', data)
@socket.on('disconnect')
def handle_connect():
    print('Disconnected')


@socket.on('join_room')
def handle_join_room(data):
    group_id = data.get('groupId')  # берём из data, не из request.args
    user_id = flask_login.current_user.id
    
    if not group_id:
        flask_socketio.emit('error', {'msg': 'groupId не передан'})
        return

    group = Groups.query.get(group_id)

    if not group:
        flask_socketio.emit('error', {'msg': 'группа не найдена'})
        return

    # правильная проверка
    user_in_group = any(user.id == user_id for user in group.users)

    if user_in_group:
        flask_socketio.join_room(f'room_{group.id}')
        flask_socketio.emit('joined', {'room': f'room_{group.id}'})
        print(f'Пользователь {user_id} вошёл в room_{group.id}')
    else:
        flask_socketio.emit('error', {'msg': 'нет доступа'})

@socket.on('message')
def handle_message_event(data):
    group_id = data.get('group_id')
    content = data.get('content', '').strip()
    
    if not content or not group_id:
        return

    # Получаем текущего пользователя через Flask-Login
    # (Убедись, что у твоей модели User есть поле username или name)
    current_user_name = flask_login.current_user.username 
    current_user_id = flask_login.current_user.id

    # 1. Логика One-to-Many: сохраняем сообщение в БД
    # Если ты еще не добавил user_id в модель Message, можно пока просто сохранять,
    # но для сокетов мы всё равно транслируем автора в реальном времени.
    new_message = Message(content=content, group_id=int(group_id), user_id = current_user_id)
    DATABASE.session.add(new_message)
    DATABASE.session.commit()

    # 2. Логика отправки: упаковываем автора и текст в один словарь
    payload = {
        'message': content,
        'username': current_user_name,
        'user_id': current_user_id,
        'group_id': group_id
        
    }

    # Отправляем этот словарь всем, кто находится в этой комнате
    flask_socketio.emit('message', payload, to=f'room_{group_id}')