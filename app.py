"""
Secure Chat Server Application

This module implements a Flask-based web application serving as a Secure Chat Server.
It offers functionality such as user authentication, chat services, and security features
like SSH key uploading and encryption.

The application provides different endpoints for managing user sessions, SSH key uploads,
encryption settings, and the chat interface.

Dependencies:
- Flask
- Flask-SQLAlchemy

Usage:
- Run 'pip install Flask Flask-SQLAlchemy' to install dependencies.
- python3 app.py <-- to run the application
- apt install python3.10-venv
"""
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash
from database.models import db, UsersModel
from utils.encryption_tools import get_password_hash
from config.server_config import ServerConfig
from flask_sqlalchemy import SQLAlchemy
import os

# Get current working directory
cwd = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Set a secret key for your application
app.secret_key = os.urandom(24)

# Configure the default database URI
database_uri = 'sqlite:///' + os.path.join(cwd, 'database', 'server.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

# Initialize SQLAlchemy instance
db.init_app(app)

with app.app_context():
    db.create_all()

# Instantiate the server configuration
server_config = ServerConfig()

# Max users
MAX_USER_COUNT = 3

# users currently logged in
active_user_count = 0


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Author: 
        Eric Thomas

    Description:
        Serves as the landing page for the Secure Chat Server.

        This function handles the GET and POST requests on the home page. It determines user
        session status, authentication, and SSH key upload status. Based on user interactions,
        it redirects to appropriate pages or displays error messages.

    Returns:
        render_template: The rendered home page template with relevant user information and server settings.
    """

    # Set authentication value
    logged_in = False
    ssh_key_uploaded = False
    user_entry = False
    if 'username' in session:
        user_entry = UsersModel.user_exists(app, session['username'])
        logged_in = UsersModel.is_logged_in(app, session['username'])
        ssh_key_uploaded = UsersModel.has_uploaded_ssh_key(app, session['username'])

    global active_user_count

    # Init function vars
    error_message = ""

    print(f"Logged in: {logged_in}")

    # React to user action button selection
    if request.method == 'POST':
        if 'add_ssh_key' in request.form:
            return redirect(url_for('ssh_key_loader'))
        elif 'user_auth' in request.form:
            return redirect(url_for('user_action'))
        elif 'enter_chat' in request.form:
            if verify_permissions():
                return redirect(url_for('chat'))
            else:
                # Create the error message(s)
                error_message += f"Please resolve the following permissions errors to access the chat page:<br>"
                if not user_entry:
                    error_message += f"Create a username or login if you have one.<br>"
                if server_config.ssh_enabled and not ssh_key_uploaded:
                    error_message += "SSH is enabled, but you haven't enabled SSH for your account.<br>"
                if server_config.encryption_enabled and not authentication:
                    error_message += "Encryption is enabled, but you haven't authenticated.<br>"

    return render_template('home.html', logged_in=logged_in, ssh_key_uploaded=ssh_key_uploaded, server_config=server_config, error_message=error_message, active_user_count=active_user_count, max_user_count=MAX_USER_COUNT)


@app.route('/user_action', methods=['GET', 'POST'])
def user_action():
    """
    Author:
        Eric Thomas

    Description:
        Function handles user actions such as login, adding a new user,
        user logout, and user deletion. It processes the incoming POST request,
        validates user information, and performs the requested action based on
        the 'action' parameter in the form data.

    Returns:
        Response: A Flask Response object containing the appropriate HTML
        template to render based on the user action.

    Global Variables:
        - active_user_count (int): Tracks the number of active users.
          It is incremented when a user logs in and decremented when they log out.
    """

    global active_user_count

    if request.method == 'POST':
        # Get username and password from the form
        username = request.form['username']
        password = request.form['password']
        action = request.form.get('action')

        # Check if the username exists in the database
        user = None
        if (UsersModel.user_exists(app, username)):
            user = UsersModel.get_user_entry(app, username)
        password_match = (get_password_hash(password) == server_config.password_hash)

        # If validated
        if not password_match:  # username limits controlled by html
            flash('Invalid password', 'error')
            return render_template('user_action.html')

        # If logging in
        if action == 'login':

            # If chat not full
            if MAX_USER_COUNT <= active_user_count:
                flash('Chat room is full. Please try again later', 'error')
                return render_template('user_action.html')

            # If user exist
            if user:
                session['username'] = username
                UsersModel.set_logged_in(app, username, True)
                active_user_count += 1
                return redirect(url_for('home'))
            else:
                flash(f'Username: {username} does not exist. Please add user.')
                return render_template('user_action.html')

        # If adding user
        if action == 'add_user':
            if user:
                flash('User exists', 'error')
                return render_template('user_action.html')
            else:
                new_user = UsersModel(username=username)
                UsersModel.add_user(app, new_user)
                flash(f'User account created for: {username}. You may now login!')
                return render_template('user_action.html')

        # User logout
        if action == 'logout':
            if 'username' in session:
                session.pop('username', None)
                UsersModel.set_logged_in(app, username, False)
                active_user_count -= 1
                flash(f'User {username} has been logged out.', 'success')
                return render_template('user_action.html')
            else:
                flash(f'Username {username} does not have an active session.')
                return render_template('user_action.html')

        # Delete user
        if action == 'delete_user':
            if UsersModel.user_exists(app, username):

                # Remove database entry for user
                UsersModel.remove_user(app, username)

                # Pop if in an active flask session
                if 'username' in session:
                    session.pop('username', None)
                    active_user_count -= 1

                flash(f'User account {username} has been deleted.', 'success')
                return render_template('user_action.html')
            else:
                flash(f'Username {username} does not have an account.')
                return render_template('user_action.html')

    return render_template('user_action.html')


@app.route('/ssh_key_loader')
def ssh_key_loader():
    """ 
    Renders the SSH key uploading interface.

    This endpoint enables users to upload their SSH keys as part of the server's security measures.

    Returns:
        render_template: The rendered SSH key uploader page template.
    """
    return render_template('ssh_key_loader.html')


@app.route('/chat')
def chat():
    """ 
    Renders the chat interface for the Secure Chat Server.

    This endpoint provides the main chat functionality of the application, allowing users to
    interact in a secure environment.

    Returns:
        render_template: The rendered chat page template.
    """
    return render_template('chat.html')


@app.route('/update_ssh', methods=['POST'])
def update_ssh():
    """
    Author: 
        Eric Thomas

    Description:
        Handles the updates to the server's SSH configuration.

        This function processes POST requests to toggle the SSH setting on or off. It updates
        the server configuration accordingly.

    Returns:
        jsonify: A JSON response indicating the success or failure of the update operation.
    """

    if request.method == 'POST':
        new_ssh_enabled = request.json.get('ssh_enabled', False)
        server_config.ssh_enabled = new_ssh_enabled
        server_config.save_config()
        return jsonify(success=True)
    return jsonify(success=False), 400


@app.route('/update_encryption', methods=['POST'])
def update_encryption():
    """
    Author: 
        Eric Thomas

    Description:
        Manages updates to the server's encryption settings.

        This function processes POST requests to enable or disable encryption. It updates the
        server configuration based on the received data.

    Returns:
        jsonify: A JSON response indicating the success or failure of the update operation.
    """
    if request.method == 'POST':
        new_encryption_enabled = request.json.get('encryption_enabled', False)
        server_config.encryption_enabled = new_encryption_enabled
        server_config.save_config()
        return jsonify(success=True)
    return jsonify(success=False), 400


def verify_permissions():
    """
    Author: 
        Eric Thomas

    Description:
        Verifies user permissions by assessing session status and server configurations.

        It checks if the user is in the session, and then, based on the server's SSH and
        encryption settings, verifies if the user has uploaded an SSH key and authenticated.

    Returns:
        bool: True if all required permissions are satisfied, False otherwise.
    """

    # Check if the user session has been established
    if 'username' not in session:
        return False
    else:

        # If server config has ssh enabled
        if server_config.ssh_enabled:
            # Check if user has entered the encryption password
            if not UsersModel.has_uploaded_ssh_key(app, session['username']):
                return False

        # If the server config has encryption enabled
        if server_config.encryption_enabled:
            # Check if encryption is enabled and if the user is authenticated
            if not UsersModel.is_logged_in(app, session['username']):
                return False

    # If function made it to this point, permissions are satisfied
    return True


if __name__ == '__main__':
    # Log all users out on startup
    UsersModel.set_all_users_logged_out(app)
    app.run(debug=True)
    # app.run(host="192.168.1.122", port=8080, debug=True)
