message=input("Type your message")
with open("messgae.txt","w") as file:
    file.write(message)

print("Message saved")