# #########user_database.py########
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin
import json



login_manager = LoginManager()


with open('admin/users.json') as u:
    users_data = json.load(u)


class User(UserMixin):
    def __init__(self, user_id, password_hash):
        self.id = user_id
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_loader(user_id):
    user_data = next((user for user in users_data if user["username"] == user_id), None)
    if user_data is None:
        return None

    user = User(user_data["username"], user_data["password"])
    return user


@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('username')
    user_data = next((user for user in users_data if user["username"] == user_id), None)
    if user_data is None:
        return None

    user = User(user_data["username"], user_data["password"])
    return user


def authenticate_user(username, password):
    user_data = next((user for user in users_data if user["username"] == username), None)
    if user_data and check_password_hash(user_data["password"], password):
        return User(user_data["username"], user_data["password"])
    return None
