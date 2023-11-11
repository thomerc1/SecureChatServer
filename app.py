"""
Secure Chat Server Application

This Flask application serves as the Secure Chat Server, providing
the primary landing page, user authentication, and chat functionality.

Author: Group A

Dependencies:
- pip install Flask
- pip install Flask-SQLAlchemy
"""
from flask import Flask, render_template
from database.models import db
from config.server_config import ServerConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the default database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'

# Configure a second database URI with a separate bind name
app.config['SQLALCHEMY_BINDS'] = {
    'chat_db': 'sqlite:///database/chat.db'
}

# Initialize separate SQLAlchemy instances for each database
db.init_app(app)


@app.route('/')
def home():
    """ 
    TODO: TO BE IMPLEMENTED BY ERIC THOMAS

    Primary landing page for the Secure Chat Server.

    - Provides the interface to enable and disable encryption
    and SSH authentication.
    - Provides the interface to be directed to the user authentication
    and creation page
    - Provides a mechanism to navigate to the chat page.
    """
    # Get the list of users
    users = UsersModel.query.all()

    return render_template('home.html')


@app.route('/user_auth')
def user_auth():
    """ 
    TODO: TO BE IMPLEMENTED BY ERIC THOMAS

    Page that the user is directed to when creating an account
    and / or if encryption is enabled when attempting to access the
    chat page

    Following a login / user creation, the user will be directed back
    to the home page.
    """
    return render_template('user_auth.html')


@app.route('/key_loader')
def key_loader():
    """ 
    TODO: TO BE IMPLEMENTED BY ALEXANDER LA BARGE AND SAMUEL ZELEKE
    """
    return render_template('key_loader.html')


@app.route('/chat')
def chat():
    """ 
    TODO: TO BE IMPLEMENTED BY DUNCAN AND NATHAN HOTSKO AND DUNCAN CLARK
    """
    return render_template('chat.html')


if __name__ == '__main__':
    app.run(debug=True)
