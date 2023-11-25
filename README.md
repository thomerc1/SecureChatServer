# SecureChatServer
Python Flask Server with encrypted messaging

## Local Usage
For usage on your local machine / network

### Install dependencies.txt 
- pip install -r dependencies.txt

#### To create dependencies.txt
- dependencies.txt created using: `pip freeze > dependencies.txt` within python virtual environment.

### Virtual Env 
- From within SecureChatServer directory
- (optional for python venv) python3 -m venv venv
- (optional for python venv) Linux: source venv/bin/activate
- (optional for python venv) Windows: venv\Scripts\activate
- (optional for python venv) After finished usage, deactivate venv by issuing: `deactivate` from within SecureChatServer directory

### Run
- Issue: `python3 app.py` from within the SecureChatServer directory
- (Optional) `python3 app.py --ip [ip address] --port [port]`

## Gitlab Usage
For usage when installing and running within gitlab environment

### Install
- Run: config/gitlab-server-setup.sh

### Run
- Run: gitlab-server-start.sh

## Interface
### Gitlab
- host: gitlab.labarge.dev (24.144.104.215)
- username: dev
- password: [To be provided]
- gitlab portal: https://gitlab.labarge.dev
  
### Local 
- From webbrowser, navigate to url: localhost:5000 (or whatever IP and port you ran the server with)
  - NOTE: If you use incognito mode for browser, you can run multiple sessions (browser
    won't share data amongst windows); therefore, you can login with multiple users

### Common
- Select 'User Actions / Login' button
- Add a username
- Enter the password: enter1the2chat3room4
  - All users have the same password
- Select "Add User" button
- Again enter the login credentials and select "Login"
- From user page, enable or disable features and navigate to chat page if permitted

## Notes
- Encryption / Decryption / All User Login Password: enter1the2chat3room4

## Structure
.<br>
├── app.py<br>
├── config<br>
│   ├── gitlab-server-setup.sh<br>
│   ├── server_config.py<br>
│   └── version.txt<br>
├── database<br>
│   └── models.py<br>
├── dependencies.txt<br>
├── gitlab-server-start.sh<br>
├── README.md<br>
├── static<br>
│   ├── home.css<br>
│   └── js<br>
│       └── home.js<br>
├── templates<br>
│   ├── chat.html<br>
│   ├── home.html<br>
│   ├── ssh_key_loader.html<br>
│   └── user_action.html<br>
└── utils<br>
    └── encryption_tools.py<br>

## TODO
- SSH authentication page
- Chat page

## TESTS
- TBD


