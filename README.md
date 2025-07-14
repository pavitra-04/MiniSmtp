# MiniSMTP Server (Python)

- A minimal, beginner-friendly SMTP server built from scratch in Python.  
- It listens on port **2525**, handles basic SMTP commands (`HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`), and saves incoming messages locally as `.eml` files — all while using just Python’s socket programming and logging.

---

##  Features

- Accepts basic SMTP protocol commands
- Parses and logs `Subject:` headers
- Saves messages in `inbox/YYYY-MM-DD/` folders
- Filenames include subjects + timestamps
- Fully annotated and easy to understand
- Built without any external libraries (just `socket`, `logging`, `os`, etc.)

---

## Learning Goals Behind the Project
- Understand how basic internet protocols work (SMTP)
- Learn socket programming in Python
- Handle raw text parsing, logging, and file handling



