# SecureChatServer
Python Flask Server with encrypted messaging

## Usage

### Dependencies
- From within SecureChatServer directory
- (optional for python venv) python3 -m venv venv
- (optional for python venv) Linux: source venv/bin/activate
- (optional for python venv) Windows: venv\Scripts\activate
- (optional for python venv) After finished usage, deactivate venv by issuing: `deactivate` from within SecureChatServer directory

#### To create dependencies.txt
- dependencies.txt created using: `pip freeze > dependencies.txt` within python virtual environment.
#### To use dependencies.txt 
- pip install -r dependencies.txt

### Run
- Issue: `python3 app.py` from within the SecureChatServer directory

### Interface
- From webbrowser, navigate to url: localhost:5000
  - NOTE: If you use incognito mode for browser, you can run multiple sessions (browser
    won't share data amongst windows); therefore, you can login with multiple users
- Select 'User Actions / Login' button
- Add a username
- Enter the password: enter1the2chat3room4
  - All users have the same password
- Select "Add User" button
- Again enter the login credentials and select "Login"
- From user page, enable or disable features and navigate to chat page if permitted
  - Note, SSH authentication is not yet implemented

## Notes
- Encryption / Decryption / All User Login Password: enter1the2chat3room4

## Structure
.<br>
├── app.py<br>
├── config<br>
│   ├── config.json<br>
│   └── server_config.py<br>
├── database<br>
│   └── models.py<br>
├── README.md<br>
├── static<br>
│   ├── home.css<br>
│   └── js<br>
├── templates<br>
│   ├── chat.html<br>
│   ├── home.html<br>
│   ├── ssh_key_loader.html<br>
│   └── user_action.html<br>
├── utils<br>
│   └── encryption_tools.py<br>
└── venv<br>
    ├── bin<br>
    ├── include<br>
    ├── lib<br>
    ├── lib64 -> lib<br>
    └── pyvenv.cfg<br>
  
## TODO
- TBD

## TESTS
- TBD


