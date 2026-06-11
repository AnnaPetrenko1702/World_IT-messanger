import flask_socketio
import flask
from auth.models import Groups
from app.settings import app , socket
from app.database import DATABASE
import flask_login

@socket.on('connect')
def handle_connect():
    print('Connected')



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