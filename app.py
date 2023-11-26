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
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash, abort
from database.models import db, UsersModel, ChatModel
from utils.encryption_tools import get_password_hash
from config.server_config import ServerConfig
from flask_sqlalchemy import SQLAlchemy
from socket import inet_aton
import argparse
import traceback
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
        Serves as the landing page for the Secure Chat Server. Handles the GET and POST requests
        on the home page. It determines user session status, authentication, and SSH key upload
        status. Based on user interactions, it redirects to appropriate pages or displays
        error messages.

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
                if server_config.encryption_enabled and not logged_in:
                    error_message += "Encryption is enabled, but you haven't authenticated.<br>"

    return render_template('home.html', logged_in=logged_in, ssh_key_uploaded=ssh_key_uploaded, server_config=server_config, error_message=error_message,
                           active_user_count=active_user_count, max_user_count=MAX_USER_COUNT, version=server_config.version)


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
          Incremented on user login and decrements on logout.
    """

    global active_user_count

    # Get necessary server configuration values
    max_username_length = server_config.max_username_length()

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

        # If logging in
        elif action == 'login':

            # If chat not full
            if MAX_USER_COUNT <= active_user_count:
                flash('Chat room is full. Please try again later', 'error')

            # If user exist
            elif user:
                if 'username' not in session:
                    session['username'] = username
                    UsersModel.set_logged_in(app, username, True)
                    active_user_count += 1
                return redirect(url_for('home'))

            else:
                flash(f'Username: {username} does not exist. Please add user.')

        # If adding user
        elif action == 'add_user':
            if user:
                flash('User exists', 'error')

            else:
                new_user = UsersModel(username=username)
                UsersModel.add_user(app, new_user)
                flash(f'User account created for: {username}. You may now login!')

        # User logout
        elif action == 'logout':
            if 'username' in session:
                session.pop('username', None)
                UsersModel.set_logged_in(app, username, False)
                active_user_count -= 1
                flash(f'User {username} has been logged out.', 'success')

            else:
                flash(f'Username {username} does not have an active session.')

        # Delete user
        elif action == 'delete_user':
            if UsersModel.user_exists(app, username):

                # Remove database entry for user
                UsersModel.remove_user(app, username)

                # Pop if in an active flask session
                if 'username' in session:
                    session.pop('username', None)
                    active_user_count -= 1

                flash(f'User account {username} has been deleted.', 'success')

            else:
                flash(f'Username {username} does not have an account.')

    return render_template('user_action.html', max_username_length=max_username_length)


@app.route('/ssh_key_loader')
def ssh_key_loader():
    """ 
    Renders the SSH key uploading interface. This endpoint enables users to
    upload their SSH keys.

    Returns:
        render_template: The rendered SSH key uploader page template.
    """

    return render_template('ssh_key_loader.html')


@app.route('/chat')
def chat():
    """
    Author:
        Eric Thomas

    Description:
        Renders the chat interface for the Secure Chat Server. This endpoint
        provides the main chat functionality of the application.

    Returns:
        render_template: The rendered chat page template with the user's username
                         and maximum message length, if the user has permissions.
        redirect: A redirection to the home page if the user does not have permissions.
    """

    # Get the username
    username = ''
    if 'username' in session:
        username = session['username']

    if verify_permissions():
        return render_template('chat.html', username=username, max_message_length=server_config.max_message_length(),
                               encryption_enabled=server_config.encryption_enabled)
    else:
        return redirect(url_for('home'))


@app.route('/update_ssh', methods=['POST'])
def update_ssh():
    """
    Author: 
        Eric Thomas

    Description:
        Handles the updates to the server's SSH configuration. This function
        processes POST requests to toggle the SSH setting on or off. It updates
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
        Manages updates to the server's encryption settings. This function processes 
        POST requests to enable or disable encryption. It updates the server
        configuration based on the received data.

    Returns:
        jsonify: A JSON response indicating the success or failure of the update operation.
    """
    if request.method == 'POST':
        new_encryption_enabled = request.json.get('encryption_enabled', False)
        server_config.encryption_enabled = new_encryption_enabled
        server_config.save_config()
        return jsonify(success=True)
    return jsonify(success=False), 400


@app.route('/submit_message', methods=['POST'])
def submit_message():
    """
    Author:
        Eric Thomas

    Description:
        Handles the submission of new chat messages sent from the client.

    Returns:
        jsonify: A JSON object indicating the success status of the message submission.
    """
    if not request.is_json:
        # If the request does not contain JSON, return an error
        return jsonify({"success": False, "error": "Invalid JSON format"}), 400

    data = request.get_json()
    user_id = data.get('user_id')
    message_content = data.get('message_content')
    message_encrypted = data.get('message_encrypted') == True  # will be false unless the string is 'True'

    if not user_id or not message_content:
        # If user_id or message_content is missing, return an error
        return jsonify({"success": False, "error": "Missing user_id or message_content"}), 400

    try:
        ChatModel.add_new_message(app, user_id, message_content, message_encrypted)
        return jsonify({"success": True})
    except Exception as e:
        # Log the exception and return an error message
        print(f"Error adding message: {e}")
        return jsonify({"success": False, "error": "Internal Server Error"}), 500


@app.route('/get_messages', methods=['GET'])
def get_messages():
    """
    Author:
        Eric Thomas

    Description:
        Fetches and returns all chat messages from the database chat table.

    Returns:
        jsonify: A JSON list of dictionaries, each representing a chat message.
    """

    messages = ChatModel.query.order_by(ChatModel.timestamp.asc()).all()
    messages_list = [{'user_id': message.user_id, 'message': message.message,
                      'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                      'encrypted': message.encrypted} for message in messages]
    return jsonify(messages_list)


def verify_permissions():
    """
    Author: 
        Eric Thomas

    Description:
        Verifies user permissions by assessing session status and server configurations.
        It checks if the user is in the session, and then, based on the server's SSH and
        encryption settings, verifies if the user has uploaded an SSH key and authenticated.

    Returns:
        bool: True if required permissions are satisfied, False otherwise.
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

    # Setup argument parser
    parser = argparse.ArgumentParser(description="Run the web application.")
    parser.add_argument('--ip', type=str, help='The IP address to bind to.', default='127.0.0.1')
    parser.add_argument('--port', type=int, help='The port to listen on.', default=5000)
    args = parser.parse_args()

    # Validate IP address
    try:
        inet_aton(args.ip)
    except OSError:
        print("Error: Invalid IP address format.")
        sys.exit(1)

    # Validate port number
    if not (0 <= args.port <= 65535):
        print("Error: Port number must be between 0 and 65535.")
        sys.exit(1)

    # Run the application
    app.run(host=args.ip, port=args.port, debug=True)
