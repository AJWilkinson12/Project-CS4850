#Created by Ben Bradshaw, 3/6/22.
#This file contains the server code for V2 of my simple chat room client.

import socket
import re
from time import sleep
from threading import Thread

HOST = "127.0.0.1"
PORT = 17129
MAXCLIENTS = 3
active_connections = {}

#Reads exisiting users from users.txt file and returns to chat_control.
def read_users():
    with open("users.txt") as f:
        users = f.readlines()
    f.close()
    return users

#Formatting new_user to match existing users and writing to the users.txt file.
def update_users(c_uid, c_pass):
    new_user = "("+c_uid+", "+c_pass+")"
    with open("users.txt", "a") as f:
        f.write("\n")
        f.write(new_user)
    f.close()

#Login logic for login command, returns None if no match is found or user is already logged in.
def login(users, la_uid, la_pass):
    #Login Logic
        #
        if(la_uid in active_connections.keys()):
            return None
        if check_match(users, la_uid, la_pass):
            return la_uid
        #If no match is found, inform user and return NULL
        else:
            return None
#Checks if current given uid and pass matches existing users in users,txt.  Used in new_user and login.
def check_match(users, c_uid, c_pass):
    for user in users:
        #Stripping each registered users extra characters
        user = re.sub("[()]", "", user);
        registered_u = user.split(", ")
        registered_u[1] = registered_u[1].replace("\n", "")
        #Check if current check variables match.
        if registered_u[0] == c_uid and registered_u[1] == c_pass:
            return True
        
#Logic for a New user for new_user command.
def new_user(users, c_uid, c_pass):
    if check_match(users, c_uid, c_pass):
        return False
    else:
        update_users(c_uid, c_pass)
        return True

#Sends message to all active connections.
def send_all(active_u, message):
    for uid, conn in active_connections.items():
        if(uid == active_u):
            continue
        conn.send((active_u + ": " + message).encode())
    return
        
#Informs all other active connections that a user has logged out.
def send_all_logout(active_u, message):
    for uid, conn in active_connections.items():
        if(uid == active_u):
            continue
        conn.send((active_u + message).encode())
    return

#Informs all other active connections that a user has logged in.
def send_all_login(active_u):
    for uid, conn in active_connections.items():
        if(uid == active_u):
            continue
        conn.send((active_u + " joins.").encode())
    return
   
#Returns a string listing each active connections UID.
def who():
    message = ""
    uids = list(active_connections.keys())
    for uid in active_connections:
        if uid == uids[-1]:
            message += uid
        else:
            message += uid +", "
    return message
    
#Main chat loop for each currently active thread/client.
def chat_control(conn, addr):
    logged_in = False
    active_u = ""

    users = read_users()
    

    while True:
        #Listening for a command to come through from the connected client.
        data = conn.recv(1024).decode()
        command = data.split(" ")
        #Login Logic - If user is already logged in, inform them.  If not and credentials are validated and user isn't already an active connection, set the active user and add to active connections.  Inform other currently actice connections.
        if command[0] == "login":
            if(logged_in):
                conn.send("Already logged in.".encode())
                continue
            else:
                active_u = login(users, command[1], command[2])
                if active_u is not None:
                    active_connections[active_u] = conn;
                    logged_in = True
                    send_all_login(active_u)
                    print(active_u + " logged in.")
                    conn.send("login confirmed".encode())
                    continue
                else:
                    conn.send("Denied.  Username or Password incorrect or user is already logged in.".encode())
                    continue
            
        #Newuser Logic - If the user is already logged in, inform them. If not and credentials do not already exist in users.txt, create the new user and add it to users.txt, then inform the user to login.
        elif command[0] == "newuser":
            if(logged_in):
                conn.send("Cannot create new user while logged  in.".encode())
                continue
            if new_user(users, command[1], command[2]):
                print("New user created.")
                users = read_users()
                conn.send("New user account created. Please login.".encode())
                continue
            else:
                conn.send("Denied. User account already exists.".encode())
                continue
                      
                            
        #Send logic - If not logged in, inform the user.  If command is all, send their message to all active connections.  If a UID is specified, send to only that active connection.
        elif command[0] == "send":
            if(not logged_in):
                conn.send("Denied. Must be logged in to use the send command.".encode())
                continue
            #Stripping send from command and appending active user to the beginning.
            if len(command) > 1:
                if command[1] == "all":
                    message = data.split(' ', 2)[2]
                    send_all(active_u, message)
                    print(active_u + ": " + message)
                    continue
                elif command[1] in active_connections:
                    message = data.split(' ', 2)[2]
                    active_connections[command[1]].send((active_u + ": " + message).encode())
                    print(active_u + "(to " + command[1] + "): " + message)
                    continue
                else:
                    conn.send("Error sending message.  Either user wasn't online or all wasn't specified.".encode())
                    continue
            else:
                conn.send("Error on send, a user or all must be specified after 'send' command.".encode())
                continue
        elif command[0] == "who":
            active_us = who()
            conn.send(active_us.encode())
                    
        #Logout Logic - Removes active user, closes connection and breaks back to listenting for a connection from client.  Informs other active connections of user logout.
        elif command[0] == "logout":
            global active_threads
            if(not logged_in):
                conn.send("Must be logged in to log out!".encode())
                continue
            logged_in = False
            print(active_u + " log out.")
            send_all_logout(active_u, " left.")
            conn.send("Successfully logged out.".encode())
            active_threads -= 1
            active_connections.pop(active_u)
            sleep(2)
            conn.close()
            active_u = ""
            return
            
#Main for server, listens for new connections up to 3.  When a new connection is found create a Thread whos target is the main chat loop.  if max is met, inform user and prompt them to logout.
                        
if __name__ == "__main__":
    print("My chat room client. Version One\n");
    active_threads = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            if active_threads < MAXCLIENTS:
                active_threads +=1
                Thread(target = chat_control,args = (conn,addr)).start()
            else:
                conn.send("Sorry. Max active users has been reached. Please logout and try again later".encode())
                sleep(1)
                conn.close()
            
                
        




