# Example usage for ServerConfig class
# append system path and import utils
from models import db, UsersModel
import sys
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# autopep8: off
from config.server_config import ServerConfig
# autopep8: on

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

server_config = ServerConfig()
server_config.load_config()
server_config.print_params()
print(f"Max Username Length: {server_config.max_username_length()}")
print(f"Max Message Length: {server_config.max_message_length()}")

# Adding users to the database
with app.app_context():
    db.create_all()

# Example usage for UsersModel class
user1 = UsersModel(username="user1")
user2 = UsersModel(username="user7", logged_in=True)
user3 = UsersModel(username="user8", ssh_key_setup=True)

UsersModel.add_user(app, user1)
UsersModel.add_user(app, user2)
UsersModel.add_user(app, user3)

with app.app_context():

    # Check if a user exists
    username_to_check = "user1"
    if UsersModel.user_exists(app, username_to_check):
        print(f"{username_to_check} exists in the database.")

    # Check if a user is logged_in
    if UsersModel.is_logged_in(app, username_to_check):
        print(f"{username_to_check} is logged_in.")

    # Check if a user has uploaded an SSH key
    if UsersModel.has_uploaded_ssh_key(app, username_to_check):
        print(f"{username_to_check} has uploaded an SSH key.")
