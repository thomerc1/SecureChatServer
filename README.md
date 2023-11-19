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
├── app.py <br>
├── config<br>
│   ├── server_config.py<br>
│   └── server_state.json<br>
├── database<br>
│   └── models.py<br>
├── instance<br>
├── README.md<br>
├── resource<br>
│   └── stored_hash.txt<br>
├── static<br>
│   └── home.css<br>
├── templates<br>
│   ├── chat.html<br>
│   └── home.html<br>
├── test<br>
└── utils<br>
    └── encryption_tools.py<br>

## Notes
- Encryption / Decryption Password: enter1the2chat3room4
  
## TODO

| REQUIREMENT                                              | POC           | Status | Test |
| -------------------------------------------------------- | ------------- | ------ | ---- |
| Basic Project Structure                                  | Eric Thomas   | Done   | TBD  |
| Login / Authentication Webpage (HTML)                    | Eric Thomas   | Done   | TBD  |
| Login / Authentication Backend                           | Eric Thomas   | Done   | TBD  |
| Basic SHA packet encryption / decryption functions       | Eric Thomas   | Done   | TBD  |
| Message packetization                                    | TBD           | TBD    | TBD  |
| Message presentation                                     | TBD           | TBD    | TBD  |
| Multi-user data contention prevention (shared resources) | TBD           | TBD    | TBD  |
| Primary chat front-end (HTML)                            | Duncan/Nathan | TBD    | TBD  |
| Primary chat back-end (sqlalchemy?)                      | Duncan/Nathan | TBD    | TBD  |
| Primary chat back-end (flask support for sql?)           | TBD           | TBD    | TBD  |
| Test - Test on phone                                     | TBD           | TBD    | TBD  |
| Test - multi users (up to 5?)                            | TBD           | TBD    | TBD  |
| Test - on PC                                             | TBD           | TBD    | TBD  |
| Test failure to authenticate prevents access             | TBD           | TBD    | TBD  |


## TESTS

| TEST                                                      | POC         | Status |
| --------------------------------------------------------- | ----------- | ------ |
| app.py - home()                                           | Eric Thomas | TBD    |
| 1. Verify default settings of ssh and encryption switches | Eric Thomas | TBD    |
| 2. Verify that settings are non-volatile                  | Eric Thomas | TBD    |

## TODO
- Add count of users on the page(s)



