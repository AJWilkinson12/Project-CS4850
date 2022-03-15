#Created by AJ Wilkinson
#PawPrint: ASWD62  StudentID: 14307129

import socket
import sys
import time

#######################################################
###    Creating a socket using Python Socket & Sys  ###
#######################################################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8002
connections = 0
loginFlag = 0
print("")
while connections == 0:
    try:
        sock.connect((host, port))
        connections = connections + 1
    except:
        pass

#####################################################
#      Formatting for when the client connects      #
#####################################################
print("YOU'RE CONNECTED")
print("")
print("")
print("*****COMMANDS AVAILABLE*****")
print("")
print("Type 'login [USERNAME] [PASSWORD]' to login")
print("Type 'newuser [USERNAME] [PASSWORD]' to create a newuser")
print("           username must be less than 32 characthers")
print("           password must be between 4 & 8 characters")
print("Type 'send' to send a message")
print("Type 'logout' to logout")
print("")
print("")

## While loop to run the program
while(True):
    if (loginFlag == 0): ##check if logged in or not
        message = input(">> ")
        sock.send(message.encode()) # python3 defaults to UTF-8 encoding for socket
        message = sock.recv(1024).decode() # decoding what is received by the server

        ##########################
        ### checking for login ###
        ##########################
        if message.split(" ")[0] == "Server:" and message.split(" ")[2] == "joins":
            #if message.split(" ")[2] == "joins" #login message would contain these two words
            newUsername = message.split(" ")[1]
            loginFlag = 1 # if login good, pump counter to get name next to input

        ##########################
        ### checking for quit  ###
        ##########################
        elif message.split(" ")[0] == "Server:" and "has decided to quit!" in message:
            print(message)
            break

        print(message)

##################################
### if statement after log in  ###
# used to add login name to chat #
##################################
    if(loginFlag == 1): ##used for when logged in
        message = input(newUsername+">> ")
        sock.send(message.encode())
        message = sock.recv(1024).decode()
        #########################
        ## checking for logout ##
        #########################
        if message.split(" ")[0] == "Server:" and "left" in message:
            loginFlag = 0
        elif message.split(" ")[0] == "Server:" and "has decided to quit!" in message:
            print(message)
            break
        print(message)

##############################
##### while loops exited #####
## close socket and program ##
##############################
print("")
print("Please come again!")
print("")
sock.close()
