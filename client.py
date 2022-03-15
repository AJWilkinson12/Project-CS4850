#Created by AJ Wilkinson
#PawPrint: ASWD62  StudentID: 14307129

import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 17128
connections = 0
loginFlag = 0
print("")
while connections == 0:
    try:
        sock.connect((host, port))
        connections = connections + 1
    except:
        pass

print("YOU'RE CONNECTED")
print("")
print("")
print("*****COMMANDS AVAILABLE*****")
print("")
print("Type 'login [USERNAME] [PASSWORD]' to login")
print("Type 'newuser [USERNAME] [PASSWORD]' to create a newuser")
print("           username must be less than 32 characthers")
print("           password must be between 4 & 8 characters")
print("Type 'send' to send a message (MUST BE LOGGED IN)")
print("Type 'logout' to logout (MUST BE LOGGED IN)")
print("")
print("")

#While loop makes the program easier to run
while(True):
    if (loginFlag == 0):
        message = input(">> ")
        sock.send(message.encode())
        message = sock.recv(1024).decode()
        
        if message.split(" ")[0] == "Server:" and message.split(" ")[2] == "joins":
            newUsername = message.split(" ")[1]
            loginFlag = 1
       
        elif message.split(" ")[0] == "Server:" and "has decided to quit!" in message:
            print(message)
            break

        print(message)

    if(loginFlag == 1):
        message = input(newUsername+">> ")
        sock.send(message.encode())
        message = sock.recv(1024).decode()
       
        if message.split(" ")[0] == "Server:" and "left" in message:
            loginFlag = 0
        elif message.split(" ")[0] == "Server:" and "has decided to quit!" in message:
            print(message)
            break
        print(message)


sock.close()
