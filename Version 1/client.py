#Created by AJ Wilkinson
# March 17th, 2022
#PawPrint: ASWD62  StudentID: 14307129

import socket
import sys
import time

# Needed variables to cnnnect to the server.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 17129
connections = 0
loginFlag = 0
print("")
while connections == 0:
    try:
        #Connects to the server/
        sock.connect((HOST, PORT))
        connections = connections + 1
    except:
        pass


#List of functions.
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

    # Let's the program know th user is logged in.
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

#Disconnects from the server.
sock.close()
