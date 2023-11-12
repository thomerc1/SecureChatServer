# SecureChatServer
Python Flask Server with encrypted messaging

## Usage
- TBD

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
| Login / Authentication Webpage (HTML)                    | Eric Thomas   | TBD    | TBD  |
| Login / Authentication Backend                           | Eric Thomas   | TBD    | TBD  |
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



