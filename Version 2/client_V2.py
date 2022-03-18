#Created by AJ Wilkinson
# March 17, 2022
#PawPrint: ASWD62  StudentID: 14307129

#All required imports.
import socket
from threading import Thread
from time import sleep
from server_V2 import PORT, HOST #Decided to import the host and port information from the server so that if needed there is only one place that you need to change it.


#Listens for the server. So that it may recieve any information that it sends.
#Such as this will let us know if the server is at the max capacity (Currently 3).
def listener(s):
    global threads
    while True:
        try:
            data = s.recv(1024).decode()
            print(data)
            if(data == "SERVER AT MAX CAPACITY"):
                return
            if threads:
                return
        except:
            pass
            
       

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))


    #Tell the client they are connected
    # and tells the user the available commands.
    print("")
    print("YOU'RE CONNECTED")
    print("")
    print("")
    print("*****COMMANDS AVAILABLE*****")
    print("")
    print("Type 'login [USERNAME] [PASSWORD]' to login")
    print("Type 'newuser [USERNAME] [PASSWORD]' to create a newuser")
    print("           username must be less than 32 characthers")
    print("           password must be between 4 & 8 characters")
    print("Type 'send all [MESSAGE]' to send a message (MUST BE LOGGED IN)")
    print("Type 'send [USERNAME] [MESSAGE]' to send a message to a specific user(MUST BE LOGGED IN)")
    print("Type 'logout' to logout (MUST BE LOGGED IN)")
    print("")
    print("")

    isLoggedIn = False
    threads = False
    usersThread = Thread(target = listener,args = [s])
    usersThread.daemon
    usersThread.start()

    while True:

        user_Input = input()
        commandWord = user_Input.split(" ")

        if commandWord[0] == "login":
            if len(commandWord) != 3:
                print("Invalid commandWord. Format is login Username Password")
                continue
            
            isLoggedIn = True
            s.send(user_Input.encode())

        elif commandWord[0] == "newuser":
            if len(commandWord) != 3:
                print("Invalid commandWord. Format is newuser Username Password")
                continue

            if len(commandWord[1]) <3 or len(commandWord[1]) >32:
                print("Invalid username.  Username must be between 3 and 32 characters.")
                continue

            if len(commandWord[2]) < 4 or len(commandWord[2]) >8:
                print("Invalid password. Password must be between 4 and 8 characters")
                continue

            s.send(user_Input.encode())
        
        elif commandWord[0] == "user_Input":
            if len(commandWord) > 1:
                message = user_Input.split(' ', 2)[2]
                if len(message) <1 or len(message) > 256:
                    print("ERROR: Messages must be between 1 and 256 characters")
                    continue
            s.send(user_Input.encode())
            
        elif commandWord[0] == "who" and len(commandWord) == 1:
            s.send(user_Input.encode())

        elif user_Input == "logout":
            threads = True
            s.send(user_Input.encode())
            sleep(1)
            break

        else:
            print("ERROR: commandWord not recognized.")
            continue
    

s.close()