"""
Author: Eric Thomas
Project: Secure Chat Server
Group: A
Date: Nov 23'
Platform: Debian Linux
Dependency: Python 3.10 +
=======================================================
Description:
Secure Chat Server Database Models

This module defines the SQLAlchemy models (tables) for the Secure Chat Server application.
It includes the UsersModel and ChatModel classes for storing user and chat information.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
import traceback
import sys
import os
from typing import NoReturn
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

# append system path and import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# autopep8: off
from utils.encryption_tools import get_password_hash
from config.server_config import ServerConfig
# autopep8: on

#############################################################################
# SqlAlchemy setup per:
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#initialize-the-extension


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class UsersModel(db.Model):
    """
    SQLAlchemy Model for storing user information.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(ServerConfig.max_username_length()), unique=True, nullable=False)
    logged_in: Mapped[bool] = mapped_column(Boolean, default=False)
    ssh_key_setup: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        """
        Description:
            Provides a string representation of the UsersModel instance.

        Returns:
            str: A string representation of the user instance.
        """
        return (f"<User(id={self.id}, username='{self.username}', "
                f"logged_in={self.logged_in}, ssh_key_setup={self.ssh_key_setup})>")

    @staticmethod
    def add_user(app: Flask, user: 'UsersModel') -> NoReturn:
        """
        Description:
            Static method to add a new user to the database.

        Args:
            app (Flask): The Flask application instance.
            user (UsersModel): An instance of UsersModel representing the new user.

        Raises:
            Exception: If any database operation fails.
        """
        try:
            with app.app_context():
                if not UsersModel.query.filter_by(username=user.username).first():
                    db.session.add(user)
                    db.session.commit()
        except Exception as e:
            db.session.rollback()
            # TODO: Handle the exception here (e.g., log the error)
            traceback.print_exc()

    @staticmethod
    def remove_user(app: Flask, username: str) -> None:
        """
        Description:
            Remove a user from the database by their username.

        Args:
            app (Flask): The Flask application instance.
            username (str): The username of the user to remove.

        Returns:
            None
        """
        try:
            with app.app_context():
                user = UsersModel.query.filter_by(username=username).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
        except Exception as e:
            db.session.rollback()
            # TODO: Handle exception
            traceback.print_exc()

    @staticmethod
    def is_logged_in(app: Flask, username: str) -> bool:
        """
        Description:
            Static method to check if a user is logged_in.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username to check for authentication.

        Returns:
            bool: True if the user is logged_in, False otherwise.
        """
        with app.app_context():
            user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.logged_in

    @staticmethod
    def has_uploaded_ssh_key(app: Flask, username: str) -> bool:
        """
        Description:
            Static method to check if a user has uploaded an SSH key.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username to check for SSH key upload.

        Returns:
            bool: True if the user has uploaded an SSH key, False otherwise.
        """

        with app.app_context():
            user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.ssh_key_setup

    @staticmethod
    def get_user_entry(app: Flask, username: str) -> bool:
        """
        Description:
            Retrieve a user's database entry by username.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username to check for SSH key upload.

        Returns:
            UsersModel or None: Database entry for the user if found, else None.

        """

        with app.app_context():
            user = UsersModel.query.filter_by(username=username).first()
        return user

    @staticmethod
    def user_exists(app: Flask, username: str) -> bool:
        """
        Description:
            Static method to verify if a user exists.

        Args:
            app (Flask): The Flask application instance. 
            username (str): Username to check the existance of.

        Returns:
            bool: True if exists, else False

        """
        with app.app_context():
            user = UsersModel.query.filter_by(username=username).first()
        return True if user is not None else False

    @staticmethod
    def set_ssh_key_setup(app: Flask, username: str, ssh_key_setup: bool) -> None:
        """
        Description:
            Static method to set the SSH key setup status for a user.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username of the user to update.
            ssh_key_setup (bool): The new SSH key setup status.

        Returns:
            None
        """
        try:
            with app.app_context():
                user = UsersModel.query.filter_by(username=username).first()
                if user:
                    user.ssh_key_setup = ssh_key_setup
                    db.session.commit()
        except Exception as e:
            db.session.rollback()
            # TODO: Handle exception
            traceback.print_exc()

    @staticmethod
    def set_logged_in(app: Flask, username: str, logged_in: bool) -> None:
        """
        Description:
            Static method to set the logged-in status for a user.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username of the user to update.
            logged_in (bool): The new logged-in status.

        Returns:
            None
        """
        try:
            with app.app_context():
                user = UsersModel.query.filter_by(username=username).first()
                if user:
                    user.logged_in = logged_in
                    db.session.commit()
        except Exception as e:
            db.session.rollback()
            # TODO: Handle exception
            traceback.print_exc()

    @staticmethod
    def set_all_users_logged_out(app: Flask) -> NoReturn:
        """
        Description:
            Static method to set the logged_in status to False for all
            users in the database.

        Args:
            app (Flask): The Flask application instance.

        Returns:
            NoReturn
        """
        with app.app_context():
            # Get all users from the database
            users = UsersModel.query.all()

            # Update the logged_in status for each user to False
            for user in users:
                user.logged_in = False
            db.session.commit()


class ChatModel(db.Model):
    """
    SQLAlchemy model for storing chat information.
    """
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(ServerConfig.max_username_length()),
                        nullable=False)
    message = db.Column(db.String(ServerConfig.max_message_length()), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Description:
            Provides a string representation of a ChatModel instance.

        Returns:
            str: A string representation of the chat message.
        """
        MSG_SNIPPET_LENGTH = 25
        msg_snippet = (self.message[:MSG_SNIPPET_LENGTH] +
                       '...') if len(self.message) > MSG_SNIPPET_LENGTH else self.message
        return f'<Chat {self.id} - User {self.user_id} - {self.timestamp}: "{msg_snippet}">'

    @staticmethod
    def check_and_remove_oldest_message(app: Flask):
        """
        Description:
            Checks if the number of messages in the database has reached a limit and,
            if so, removes the oldest message.

        Args:
            app (Flask): The Flask application instance.
        """
        with app.app_context():
            if ChatModel.query.count() >= ServerConfig.max_message_count():
                oldest_message = ChatModel.query.order_by(ChatModel.timestamp).first()
                db.session.delete(oldest_message)
                db.session.commit()

    @staticmethod
    def add_new_message(app: Flask, user_id: str, message_content: str):
        """
        Description:
            Adds a new message to the database and ensures that the total number of
            messages does not exceed the set message count limit.

        Args:
            app (Flask): The Flask application instance.
            user_id (str): The ID of the user sending the message.
            message_content (str): The content of the message being sent.
        """
        with app.app_context():
            ChatModel.check_and_remove_oldest_message(app)
            new_message = ChatModel(user_id=user_id, message=message_content)
            db.session.add(new_message)
            db.session.commit()


if __name__ == '__main__':
    # Example usage for ServerConfig class
    from config.server_config import ServerConfig
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import shutil

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)

    server_config = ServerConfig()
    server_config.load_config()
    server_config.print_params()
    print(f"Max Username Length: {server_config.max_username_length()}")
    print(f"Max Message Length: {server_config.max_message_length()}")

    # Adding users to the database
    with app.app_context():
        db.create_all()

    # USERS MODEL TEST---------------------------------------------

    # Example usage for UsersModel class
    user1 = UsersModel(username="user1")
    user2 = UsersModel(username="user2")
    user3 = UsersModel(username="user3")

    # Add the users
    UsersModel.add_user(app, user1)
    UsersModel.add_user(app, user2)
    UsersModel.add_user(app, user3)

    # Check if a user exists
    username = "user1"
    user = UsersModel.get_user_entry(app, username)
    if user:

        # Print user settings
        print(f"Username: {user.username}")
        print(f"SSH Key Setup: {user.ssh_key_setup}")
        print(f"Logged In: {user.logged_in}")

        # Set ssh_key_setup to False for the user
        UsersModel.set_ssh_key_setup(app, username, False)

        # Set logged_in to False for the user
        UsersModel.set_logged_in(app, username, False)

        # Print settings again
        print(f"Username: {user.username}")
        print(f"SSH Key Setup: {UsersModel.has_uploaded_ssh_key(app, username)}")
        print(f"Logged In: {UsersModel.is_logged_in(app, username)}")

        # Set ssh_key_setup to True for the user
        UsersModel.set_ssh_key_setup(app, username, True)

        # Set logged_in to True for the user
        UsersModel.set_logged_in(app, username, True)

        # Print settings again
        print(f"Username: {user.username}")
        print(f"SSH Key Setup: {UsersModel.has_uploaded_ssh_key(app, username)}")
        print(f"Logged In: {UsersModel.is_logged_in(app, username)}")
    else:
        print(f"User {username} not found.")

    UsersModel.remove_user(app, username)
    if not UsersModel.user_exists(app, username):
        print(f"User entry: {username} was successfully removed.")

    # CHAT MODEL TEST-------------------------------------------------------
    user_id = 1
    message_content = "Hello, chat!"

    # Add a new chat message to the chat database
    ChatModel.add_new_message(app, user_id, message_content)

    # Retrieve and print the chat messages from the chat database
    with app.app_context():
        messages = ChatModel.query.all()
        for message in messages:
            print(f"Message ID: {message.id}")
            print(f"User ID: {message.user_id}")
            print(f"Message: {message.message}")
            print(f"Timestamp: {message.timestamp}")
            print()

    # Show message count control
    exceed_value = 20
    for i in range(ServerConfig.max_message_count() + exceed_value):
        ChatModel.add_new_message(app, user_id, message_content)

    with app.app_context():
        messages = ChatModel.query.all()
        msg_cnt = len(messages)
        print(f"Added {exceed_value} in excess of the message storage limit of {ServerConfig.max_message_count()}")
        print(f"There are {msg_cnt} messages in the database.")

    # Delete the test database file
    cwd = os.path.abspath(os.path.dirname(__file__))
    db_dir_path_1 = os.path.join(cwd, '..', 'instance')
    db_dir_path_2 = os.path.join(cwd, 'instance')
    if os.path.exists(db_dir_path_1):
        shutil.rmtree(db_dir_path_1)
        print(f"Deleted the test database dir: {db_dir_path_1}")

    if os.path.exists(db_dir_path_2):
        shutil.rmtree(db_dir_path_2)
        print(f"Deleted the test database dir: {db_dir_path_2}")
