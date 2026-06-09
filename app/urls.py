import flask
from .settings import app
from auth.app import registration , auth
from auth.views import registration_view , auth_view

registration.add_url_rule('/registration', view_func=registration_view, methods=['POST', 'GET'])
auth.add_url_rule('/auth', view_func=auth_view, methods=['POST', 'GET'])

app.register_blueprint(registration)
app.register_blueprint(auth)