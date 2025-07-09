# smtp_server.py
import socket
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Create base inbox folder if not exists
if not os.path.exists("inbox"):
    os.makedirs("inbox")

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 2525))
    server_socket.listen(1)
    logging.debug("Socket bound to localhost on port 2525")

    conn, addr = server_socket.accept()
    logging.info(f"Connection from {addr}")
    conn.sendall(b"220 MiniSMTP Server Ready\r\n")

    in_data_mode = False
    helo_received = False
    mail_from_received = False
    rcpt_to_received = False
    sender = ""
    recipient = ""
    message_lines = []

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        for line in data.split("\r\n"):
            logging.debug(f"Received: {line}")

            if in_data_mode:
                if line == ".":
                    # Combine headers + message body
                    header = f"From: {sender}\nTo: {recipient}\n\n"
                    full_message = header + "\n".join(message_lines)

                    # Create dated folder
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    time_str = datetime.now().strftime("%H-%M-%S")
                    folder_path = os.path.join("inbox", date_str)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    # Create full filename
                    filename = os.path.join(folder_path, f"msg_{time_str}.eml")

                    # Save the message
                    try:
                        with open(filename, "w") as file:
                            file.write(full_message)
                        logging.info(f"Message saved to {filename}")
                        conn.sendall(b"250 Message accepted\r\n")
                    except Exception as e:
                        logging.error(f"Failed to save message: {e}", exc_info=True)
                        conn.sendall(b"451 Requested action aborted. Local error.\r\n")

                    # Reset session state
                    helo_received = False
                    mail_from_received = False
                    rcpt_to_received = False
                    in_data_mode = False
                    message_lines = []

                else:
                    message_lines.append(line)

            else:
                # Handle SMTP commands
                if line.upper().startswith("HELO"):
                    helo_received = True
                    conn.sendall(b"250 Hello\r\n")
                    logging.info("HELO command received")

                elif line.upper().startswith("MAIL FROM:"):
                    if not helo_received:
                        conn.sendall(b"503 Bad sequence of commands\r\n")
                        logging.warning("MAIL FROM received before HELO")
                    else:
                        sender = line[10:].strip()
                        mail_from_received = True
                        conn.sendall(b"250 OK\r\n")
                        logging.info(f"MAIL FROM accepted: {sender}")

                elif line.upper().startswith("RCPT TO:"):
                    if not mail_from_received:
                        conn.sendall(b"503 Bad sequence of commands\r\n")
                        logging.warning("RCPT TO received before MAIL FROM")
                    else:
                        recipient = line[8:].strip()
                        rcpt_to_received = True
                        conn.sendall(b"250 OK\r\n")
                        logging.info(f"RCPT TO accepted: {recipient}")

                elif line.upper() == "DATA":
                    if not rcpt_to_received:
                        conn.sendall(b"503 Bad sequence of commands\r\n")
                        logging.warning("DATA received before RCPT TO")
                    else:
                        in_data_mode = True
                        message_lines = []
                        conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                        logging.info("DATA mode started")

                elif line.upper() == "QUIT":
                    conn.sendall(b"221 Bye\r\n")
                    logging.info("Client disconnected with QUIT")
                    break

                else:
                    conn.sendall(b"500 Syntax error: command unrecognized\r\n")
                    logging.warning(f"Unrecognized command: {line}")

except Exception as e:
    logging.error(f"Unexpected server error: {e}", exc_info=True)

finally:
    try:
        conn.close()
        logging.info("Connection closed.")
    except:
        pass
    try:
        server_socket.close()
        logging.info("Server shutdown.")
    except:
        pass
