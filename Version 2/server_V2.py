#Created by AJ Wilkinson
# March 17th, 2022
#PawPrint: ASWD62  StudentID: 14307129

import socket
import re
from time import sleep
from threading import Thread

#Rquired information for the server to connect to the client.
HOST = "127.0.0.1"
PORT = 17129
#Sets the amount of allowed clients to connect to the server
MAXCLIENTS = 3
#Stores the current clients connected for easier access for later use.
current_clients = {}

#Logs in a user from their client. Allowing them to send messages.
def login_User(users, check_UserID, check_UserPass):

        if(check_UserID in current_clients.keys()):
            return None

        if check_Users(users, check_UserID, check_UserPass):
            return check_UserID

        else:
            return None

#Function to assist in the creation of a new user account.
def new_user(users, user_ID, user_Pass):
    if check_Users(users, user_ID, user_Pass):
        return False
    else:
        update_File(user_ID, user_Pass)
        return True

#Will send a message sent by another client to all active clients
def send_Message(current_user, sent):
    for userID, client in current_clients.items():
        if(userID == current_user):
            continue
        client.send((current_user + ": " + sent).encode())
    return

#Find the active users within the server and returns it the client requesting said information.
def whoIsHere():
    sent = ""
    uids = list(current_clients.keys())
    for userID in current_clients:
        if userID == uids[-1]:
            sent += userID
        else:
            sent += userID +", "
    return sent

#Updates the user file
def update_File(user_ID, user_Pass):
    new_user = "("+user_ID+", "+user_Pass+")"

    with open("users.txt", "a") as fp:
        fp.write("\n")
        fp.write(new_user)

    fp.close()

#Will check to see if a client trying to login is already logged in or if there is an existing user when trying to create a new user.
def check_Users(users, user_ID, user_Pass):
    for user in users:
        #Stripping each registered users extra characters
        user = re.sub("[()]", "", user)
        registered_u = user.split(", ")
        registered_u[1] = registered_u[1].replace("\n", "")
        #Check if current check variables match.
        if registered_u[0] == user_ID and registered_u[1] == user_Pass:
            return True
        
#Will send a message to the current users that another user decided to logout.
def inform_Logout(current_user, sent):
    for userID, client in current_clients.items():
        if(userID == current_user):
            continue
        client.send((current_user + sent).encode())
    return

#Will send a message to the current users that another user decided to login.
def inform_Login(current_user):
    for userID, client in current_clients.items():
        if(userID == current_user):
            continue
        client.send((current_user + " joins.").encode())
    return

#Reads the 'users' file and sees which users are registerd.
def readFile():
    with open("users.txt") as fp:
        users = fp.readlines()
    fp.close()
    return users
    
#Central control that handels all the other various logic. This was needed as when all crammed together it would crash.
def ADMIN(client, address):
    isLoggedIn = False
    current_user = ""

    users = readFile()
    

    while True:

        try:
            
            data = client.recv(1024).decode()
            commandWord = data.split(" ")
            
            #Login function so that an existing user may login and send messages.
            if commandWord[0] == "login":

                if(isLoggedIn):
                    client.send("Already logged in.".encode())
                    continue

                current_user = login_User(users, commandWord[1], commandWord[2])

                if current_user is not None:
                    current_clients[current_user] = client
                    isLoggedIn = True
                    inform_Login(current_user)
                    print(current_user + " logged in.")
                    client.send("Login was a success!".encode())
                    continue
                
                else:
                    client.send("ERROR: USER OR PASS INCORRECT OR USER IS ALREADY ACTIVE".encode())
                    continue
                
            #New User function to create a new user account
            elif commandWord[0] == "newuser":

                if(isLoggedIn):
                    client.send("Cannot create new user while logged  in.".encode())
                    continue

                if new_user(users, commandWord[1], commandWord[2]):
                    print("New user created.")
                    users = readFile()
                    client.send("New user account created. Please login.".encode())
                    continue

                else:
                    client.send("ERROR: USER MUST ALREADY EXIST.".encode())
                    continue
                        

            #Send function to send the message to others                
            elif commandWord[0] == "send":
                if(not isLoggedIn):
                    client.send("ERROR: YOU MUST BE LOGGED IN TO SEND A MESSAGE".encode())
                    continue

                if len(commandWord) > 1:
                    if commandWord[1] == "all":
                        sent = data.split(' ', 2)[2]
                        send_Message(current_user, sent)
                        print(current_user + ": " + sent)
                        continue

                    elif commandWord[1] in current_clients:
                        sent = data.split(' ', 2)[2]
                        current_clients[commandWord[1]].send((current_user + ": " + sent).encode())
                        print(current_user + "(to " + commandWord[1] + "): " + sent)
                        continue

                    else:
                        client.send("Error sending sent.  Either user wasn't online or all wasn't specified.".encode())
                        continue

                else:
                    client.send("Error on send, a user or all must be specified after 'send' commandWord.".encode())
                    continue

            elif commandWord[0] == "who":
                current_users = whoIsHere()
                client.send(current_users.encode())
                        
            elif commandWord[0] == "logout":
                global threads_connected

                if(isLoggedIn == False):
                    client.send("Must be logged in to log out!".encode())
                    continue

                isLoggedIn = False
                print(current_user + " logged out.")
                inform_Logout(current_user, " logged off.")
                client.send("Logout was a success!".encode())
                threads_connected -= 1
                current_clients.pop(current_user)

                sleep(2)

                client.close()
                current_user = ""

                return
        except:
            pass

#Main function that listens for connections. Will only allow up to 3 connections as that is what the MAXCLIENTS variable is set to.
#  If more are wanted then that variables value must be increased manually.                      
if __name__ == "__main__":

    print("Waiting for connections...\n")
    threads_connected = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))

        while True:
            server.listen()
            client, address = server.accept()

            if threads_connected < MAXCLIENTS:
                threads_connected +=1
                print("A Client connected!")
                Thread(target = ADMIN,args = (client,address)).start()

            else:
                print("One to many clients tried to connect.")
                client.send("SERVER AT MAX CAPACITY".encode())
                sleep(1)
                client.close()