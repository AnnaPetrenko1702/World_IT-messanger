import flask
from .settings import app
from auth.app import registration , auth , email_confirm
from auth.views import registration_view , auth_view, confirm_email_view , confirm_email_page
from chat.app import chat_blueprint
from chat.views import handle_chat_page

registration.add_url_rule('/registration', 
                        view_func=registration_view, 
                        methods=['POST', 'GET'])

auth.add_url_rule('/auth', 
                view_func=auth_view, 
                methods=['POST', 'GET'])

auth.add_url_rule('/confirm', 
                view_func=confirm_email_view,
                methods=['GET'])

email_confirm.add_url_rule('/confirm_page', 
                        view_func=confirm_email_page,
                        methods=['GET'])

# chat_blueprint.add_url_rule('/', 
#                             view_func=handle_chat_page, 
#                             methods = ["GET", "POST"])
chat_blueprint.add_url_rule('/', view_func=handle_chat_page, defaults={'chat_id': None}, methods=['GET', 'POST'])
chat_blueprint.add_url_rule('/chat/', view_func=handle_chat_page, defaults={'chat_id': None}, methods=['GET', 'POST'])
chat_blueprint.add_url_rule('/chat/<int:chat_id>', view_func=handle_chat_page, methods=['GET', 'POST'])
app.register_blueprint(registration)
app.register_blueprint(auth)
app.register_blueprint(email_confirm)
app.register_blueprint(chat_blueprint)