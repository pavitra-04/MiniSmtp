# MiniSMTP Server 

A minimal custom SMTP server built in Python to simulate the core working of email communication.

## Features
- Listens on port `2525`
- Accepts standard SMTP commands: `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`
- Logs all activity using Python’s logging module
- Saves incoming emails as .eml files
- Organizes inbox into folders by date with timestamped filenames


##  Built With
- Python 
- `socket` – for low-level networking
- `logging` – for structured logs
- `datetime` – for timestamps
- `telnet` – for testing client interaction


