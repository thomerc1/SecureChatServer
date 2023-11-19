# SecureChatServer
Python Flask Server with encrypted messaging

## Usage
### Run
- python3 - m venv venv
- Linux: source venv/bin/activate
- Windows: venv\Scripts\activate

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

## Notes
- Encryption / Decryption Password: enter1the2chat3room4
  
## TODO

| REQUIREMENT                                              | POC           | Status                                  | Test |
| -------------------------------------------------------- | ------------- | --------------------------------------- | ---- |
| Basic Project Structure                                  | Eric Thomas   | Done                                    | TBD  |
| Homepage / landing page                                  | Eric Thomas   | Done                                    | TBD  |
| Login / Authentication Webpage (HTML)                    | Eric Thomas   | Done                                    | TBD  |
| Login / Authentication Backend                           | Eric Thomas   | Done                                    | TBD  |
| Basic SHA packet encryption / decryption functions       | Eric Thomas   | Done                                    | TBD  |
| Message packetization                                    | TBD           | TBD                                     | TBD  |
| Message presentation                                     | TBD           | TBD                                     | TBD  |
| Multi-user data contention prevention (shared resources) | TBD           | TBD                                     | TBD  |
| Primary chat front-end (HTML)                            | Duncan/Nathan | TBD                                     | TBD  |
| Database support (sqlalchemy)                            | Eric Thomas   | User Table complete, chat table started | TBD  |
| Primary chat back-end (flask support for sql?)           | TBD           | TBD                                     | TBD  |
| Test - Test on phone                                     | Eric Thomas   | Complete                                | TBD  |
| Test - multi users (up to 3)                             | Eric Thomas   | Complete                                | TBD  |
| Test - on PC                                             | Eric Thomas   | Complete                                | TBD  |
| Test failure to authenticate prevents access             | Eric Thomas   | Complete                                | TBD  |


## TESTS

| TEST                                                      | POC         | Status |
| --------------------------------------------------------- | ----------- | ------ |
| app.py - home()                                           | Eric Thomas | TBD    |
| 1. Verify default settings of ssh and encryption switches | Eric Thomas | TBD    |
| 2. Verify that settings are non-volatile                  | Eric Thomas | TBD    |

## TODO
- Add count of users on the page(s)



