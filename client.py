#Created by Ben Bradshaw, 3/6/22.
#This file contains the client code for V2 of my simple chat room client.

import socket
from threading import Thread
from time import sleep

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 16141 # The port used by the server


#Thread that constantly listens for incoming data for the server. Prints when received.  If stop_threads is set to true from main loop or is informed that server is at max capacity, stop listenting and return. 
def listen_for_server(s):
    global stop_threads
    while True:
        data = s.recv(1024).decode()
        print(data)
        if(data == "Sorry. Max active users has been reached."):
            return
        if stop_threads:
            return
       

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("My chat room client. Version One \n")
    logged_in = False
    stop_threads = False
    th = Thread(target = listen_for_server,args = [s])
    th.daemon
    th.start()
    while True:
        send = input()
        command = send.split(" ")
        #Login logic - validates input then sends to server.
        if command[0] == "login":
            if len(command) != 3:
                print("Invalid command. Format is login Username Password")
                continue
            s.send(send.encode())
        #Newuser logic - validates input then sends to server
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
         
        #Send logic - validates message and sends to server.
        elif command[0] == "send":
            if len(command) > 1:
                message = send.split(' ', 2)[2]
                if len(message) <1 or len(message) > 256:
                    print("Invalid message.  Messages must be between 1 and 256 characters")
                    continue
            s.send(send.encode())
        elif command[0] == "who" and len(command) == 1:
            s.send(send.encode())
       
        #Logout logic - ensures user is logged in, then sends logout to server, breaks loop and closes connection.
        elif send == "logout":
            stop_threads = True
            s.send(send.encode())
            sleep(1)
            break
        else:
            print("Command not recognized.")
            continue
s.close()

