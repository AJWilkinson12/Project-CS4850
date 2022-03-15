#Created by AJ Wilkinson
#PawPrint: ASWD62  StudentID: 14307129

import socket
from threading import Thread
from time import sleep
from server_V2 import PORT, HOST



def listen_for_server(s):
    global threads
    while True:
        data = s.recv(1024).decode()
        print(data)
        if(data == "Sorry. Max active users has been reached."):
            return
        if threads:
            return
       

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

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
    print("Type 'send' to send a message (MUST BE LOGGED IN)")
    print("Type 'logout' to logout (MUST BE LOGGED IN)")
    print("")
    print("")

    isLoggedIn = False
    threads = False
    th = Thread(target = listen_for_server,args = [s])
    th.daemon
    th.start()

    while True:
        send = input()
        command = send.split(" ")

        if command[0] == "login":
            if len(command) != 3:
                print("Invalid command. Format is login Username Password")
                continue
            
            isLoggedIn = True
            s.send(send.encode())

        elif command[0] == "newuser":
            if len(command) != 3:
                print("Invalid command. Format is newuser Username Password")
                continue

            if len(command[1]) <3 or len(command[1]) >32:
                print("Invalid username.  Username must be between 3 and 32 characters.")
                continue

            if len(command[2]) < 4 or len(command[2]) >8:
                print("Invalid password. Password must be between 4 and 8 characters")
                continue

            s.send(send.encode())
         
        elif command[0] == "send":
            if len(command) > 1:
                message = send.split(' ', 2)[2]
                if len(message) <1 or len(message) > 256:
                    print("ERROR: Messages must be between 1 and 256 characters")
                    continue
            s.send(send.encode())
            
        elif command[0] == "who" and len(command) == 1:
            s.send(send.encode())

        elif send == "logout":
            threads = True
            s.send(send.encode())
            sleep(1)
            break

        else:
            print("ERROR: Command not recognized.")
            continue

s.close()