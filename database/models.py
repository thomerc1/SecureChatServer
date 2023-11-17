"""
Course Name: CMSC495 7384
Project: CMSC495 Secure Chat Server
Group: A
Date: Nov 23'
Platform: Debian Linux
Dependency: Python 3.10 +
=======================================================
Description:
Secure Chat Server Database Models

This module defines the SQLAlchemy models for the Secure Chat Server application.
It includes the UsersModel and ChatModel classes for storing user and chat information.

Dependencies:
- Flask-SQLAlchemy
"""

# Append the source dirs to the Python Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
import traceback
import sys
import os
from typing import NoReturn
from sqlalchemy.orm import DeclarativeBase

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
    Author:
        Eric Thomas

    Description:
        SQLAlchemy Model for storing user information.

    Notes: 
        Models in python are very confusing. Each model defines the "columns" in your database.
        However, each instance of the model is a row in your database. 
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(ServerConfig.max_username_length()), unique=True, nullable=False)
    logged_in: Mapped[bool] = mapped_column(Boolean, default=False)
    ssh_key_setup: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def add_user(app: Flask, user: 'UsersModel') -> NoReturn:
        """
        Author:
            Eric Thomas

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
    def is_logged_in(app: Flask, username: str) -> bool:
        """
        Author:
            Eric Thomas

        Description:
            Static method to check if a user is logged_in.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username to check for authentication.

        Returns:
            bool: True if the user is logged_in, False otherwise.
        """
        user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.logged_in

    @staticmethod
    def has_uploaded_ssh_key(app: Flask, username: str) -> bool:
        """
        Author:
            Eric Thomas

        Description:
            Static method to check if a user has uploaded an SSH key.

        Args:
            app (Flask): The Flask application instance.
            username (str): Username to check for SSH key upload.

        Returns:
            bool: True if the user has uploaded an SSH key, False otherwise.
        """
        user = UsersModel.query.filter_by(username=username).first()
        return user is not None and user.ssh_key_setup

    @staticmethod
    def user_exists(app: Flask, username: str) -> bool:
        """
        Author:
            Eric Thomas

        Description:
            Static method to verify if a user exists.

        Args:
            app (Flask): The Flask application instance. 
            username (str): Username to check the existance of.

        Returns:
            bool: True if exists, else False

        """

        user = UsersModel.query.filter_by(username=username).first()
        return True if user is not None else False


class ChatModel(db.Model):
    """
    Model for storing chat information.

    Fields:
    - id: Primary key for the chat record.
    - message: The chat message.
    - |user | message | message_id |
    """

    """
    __tablename__ = "chat"
    __bind_key__ = "chat_db"
    """

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(ServerConfig.max_message_length()), nullable=False)

    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    # Example usage for ServerConfig class
    from config.server_config import ServerConfig
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)

    server_config = ServerConfig()
    server_config.load_config()
    server_config.print_params()
    print(f"Max Username Length: {server_config.max_username_length}")
    print(f"Max Message Length: {server_config.max_message_length}")

    # Example usage for UsersModel class
    user1 = UsersModel(username="user1")
    user2 = UsersModel(username="user7", logged_in=True)
    user3 = UsersModel(username="user8", ssh_key_setup=True)

    # Adding users to the database
    with app.app_context():
        db.create_all()

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
