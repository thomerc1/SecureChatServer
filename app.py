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

Functions:
- verify_permissions: Checks user permissions based on server configurations.
- home: Renders the home page and handles user actions.
- user_auth: Renders the user authentication page.
- ssh_key_loader: Renders the page for SSH key uploading.
- chat: Renders the chat interface.
- update_ssh: Handles updates to SSH configuration via POST requests.
- update_encryption: Handles updates to encryption settings via POST requests.
"""
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash
from database.models import db, UsersModel
from config.server_config import ServerConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set a secret key for your application
app.secret_key = 'I still dont understand the secret key...'

# Configure the default database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'

# Configure a second database URI with a separate bind name
app.config['SQLALCHEMY_BINDS'] = {
    'chat_db': 'sqlite:///database/chat.db'
}

# Initialize SQLAlchemy instance
db.init_app(app)

# Instantiate the server configuration
server_config = ServerConfig()


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
    authentication = False
    ssh_key_uploaded = False
    user_session = False
    if 'username' in session:
        user_session = True
        authentication = UsersModel.is_authenticated(session['username'])
        ssh_key_uploaded = UsersModel.has_uploaded_ssh_key(session['username'])

    # Init function vars
    error_message = ""

    # React to user action button selection
    if request.method == 'POST':
        if 'add_ssh_key' in request.form:
            return redirect(url_for('ssh_key_loader'))
        elif 'user_auth' in request.form:
            return redirect(url_for('user_auth'))
        elif 'enter_chat' in request.form:
            if verify_permissions():
                return redirect(url_for('chat'))
            else:
                # Create the error message(s)
                error_message += f"Please resolve the following permissions errors to access the chat page:<br>"
                if not user_session:
                    error_message += f"Create a username or login if you have one.<br>"
                if server_config.ssh_enabled and not ssh_key_uploaded:
                    error_message += "SSH is enabled, but you haven't enabled SSH for your account.<br>"
                if server_config.encryption_enabled and not authentication:
                    error_message += "Encryption is enabled, but you haven't authenticated.<br>"

    return render_template('home.html', authentication=authentication, ssh_key_uploaded=ssh_key_uploaded, server_config=server_config, error_message=error_message)


@app.route('/user_auth')
def user_auth():
    """
    Author: 
        Eric Thomas

    Description:
        Renders the user authentication page.

        This is an endpoint resolution function that is used for account creation or 
        user authentication, which is necessary for when encryption is enabled.
        After successful login or user creation, it redirects back to the home page.

    Returns:
        render_template: The rendered user authentication page template.
    """
    return render_template('user_auth.html')


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
            if (UsersModel.has_uploaded_ssh_key(session['username']) == False):
                return False

        # If the server config has encryption enabled
        if server_config.encryption_enabled:
            # Check if encryption is enabled and if the user is authenticated
            if (UsersModel.is_authenticated(session['username']) == False):
                return False

    # If function made it to this point, permissions are satisfied
    return True


if __name__ == '__main__':
    app.run(debug=True)
