# smtp_server.py

import socket

# Step 1: Create a TCP socket (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Bind to localhost and port 2525
server_socket.bind(('localhost', 2525))

# Step 3: Start listening for connections (max 1 at a time for now)
server_socket.listen(1)
print("📡 Server is listening on port 2525...")

# Step 4: Accept a connection
conn, addr = server_socket.accept()
print(f"📥 Connection accepted from {addr}")

# Step 5: Receive data (max 1024 bytes)
data = conn.recv(1024).decode()
print(f"📝 Message received: {data}")

# Step 6: Save to file
with open("received_message.eml", "w") as file:
    file.write(data)

print("✅ Message saved to received_message.eml")

# Step 7: Close connection
conn.close()
server_socket.close()
