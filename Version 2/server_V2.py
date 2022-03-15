#Created by AJ Wilkinson
#PawPrint: ASWD62  StudentID: 14307129

import socket
import re
from time import sleep
from threading import Thread

HOST = "127.0.0.1"
PORT = 17123
MAXCLIENTS = 3
connectedUsers = {}

def login(users, user_id, user_pass):
        if(user_id in connectedUsers.keys()):
            return None
        if check_file(users, user_id, user_pass):
            return user_id
        else:
            return None

def check_file(users, user_ID, password):
    for user in users:
        user = re.sub("[()]", "", user)
        registered_user = user.split(", ")
        registered_user[1] = registered_user[1].replace("\n", "")
        if registered_user[0] == user_ID and registered_user[1] == password:
            return True
        
def new_user(users, user_ID, password):
    if check_file(users, user_ID, password):
        return False

    else:
        new_user = "("+user_ID+", "+password+")"
        with open("users.txt", "a") as fp:
            fp.write("\n")
            fp.write(new_user)
        fp.close()
        return True   

def admin(conn, addr):
    isLoggedIn = False
    activeUsers = ""

    with open("users.txt") as fp:
        users = fp.readlines()
    fp.close()
    

    while True:
        data = conn.recv(1024).decode()
        commandWord = data.split(" ")
        if commandWord[0] == "login":

            if(isLoggedIn):
                conn.send("Already logged in.".encode())
                continue

            else:
                activeUsers = login(users, commandWord[1], commandWord[2])
                if activeUsers is not None:
                    connectedUsers[activeUsers] = conn
                    isLoggedIn = True
                    for userID, conn in connectedUsers.items():
                        if(userID == activeUsers):
                            continue

                        conn.send((activeUsers + " joins.").encode())

                    print(activeUsers + " logged in.")
                    conn.send("login confirmed".encode())
                    continue

                else:
                    conn.send("ERROR: Username or Password incorrect or the user is already logged in.".encode())
                    continue
            
        elif commandWord[0] == "newuser":

            if(isLoggedIn):
                conn.send("Cannot create new user while logged  in.".encode())
                continue

            if new_user(users, commandWord[1], commandWord[2]):
                print("New user created.")
                with open("users.txt") as fp:
                    users = fp.readlines()
                fp.close()
                conn.send("New user account created. Please login.".encode())
                continue

            else:
                conn.send("ERROR: User account exists.".encode())
                continue
                      
                            
        elif commandWord[0] == "send":

            if(not isLoggedIn):
                conn.send("ERROR: You must be logged in to use the send a message".encode())
                continue

            if len(commandWord) > 1:
                if commandWord[1] == "all":
                    message = data.split(' ', 2)[2]
                    for userID, conn in connectedUsers.items():
                        if(userID == activeUsers):
                            continue
                        conn.send((activeUsers + ">> " + message).encode())
                    print(activeUsers + ">> " + message)
                    continue

                elif commandWord[1] in connectedUsers:

                    message = data.split(' ', 2)[2]
                    connectedUsers[commandWord[1]].send((activeUsers + ": " + message).encode())
                    print(activeUsers + "(to " + commandWord[1] + "): " + message)
                    continue

                else:
                    conn.send("Error sending message.  Either user wasn't online or all wasn't specified.".encode())
                    continue

            else:
                conn.send("Error on send, a user or all must be specified after 'send' commandWord.".encode())
                continue

        elif commandWord[0] == "who":
            message = ""
            user_IDs = list(connectedUsers.keys())
            for userID in connectedUsers:

                if userID == user_IDs[-1]:
                    message += userID

                else:
                    message += userID +", "

            conn.send(message.encode())
                    
        elif commandWord[0] == "logout":
            
            global active_threads
            if(not isLoggedIn):
                conn.send("Must be logged in to log out!".encode())
                continue

            isLoggedIn = False

            print(activeUsers + " log out.")

            for userID, conn in connectedUsers.items():
                if(userID == activeUsers):
                    continue

                conn.send((activeUsers + message).encode())

            conn.send("Successfully logged out.".encode())
            active_threads -= 1
            connectedUsers.pop(activeUsers)

            sleep(1)

            conn.close()
            activeUsers = ""
            return
            
                       
if __name__ == "__main__":
    
    print("Waiting for connections...")
    active_threads = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        while True:
            s.listen()
            conn, addr = s.accept()

            if active_threads < MAXCLIENTS:
                print("A client connected!")
                active_threads +=1
                Thread(target = admin,args = (conn,addr)).start()

            else:
                conn.send("Sorry. Max active users has been reached. Please logout and try again later".encode())
                conn.close()