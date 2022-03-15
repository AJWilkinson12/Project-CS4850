#Created by AJ Wilkinson
#PawPrint: ASWD62  StudentID: 14307129

import socket
import re
import sys
import time
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 17120
MAXCLIENTS = 3
isLoggedIn = 0
sock.bind((HOST,PORT))
sock.listen(3)
connections = 0

print ("Waiting for connection...")

conn, addr = sock.accept() #accepts connects from anyone

# if connections < MAXCLIENTS:
#     connections += 1
#     Thread(target = main(), args = (conn, addr)).start()


print("")
print("A client has connected!")
print("")


def read_users():

    with open("users.txt") as f:
        users = f.readlines()

    f.close()
    return users

def new_user(users, user_id, password):

    if check_file(users, user_id, password):
        return False

    else:
        update_file(user_id, password)
        return True

def check_file(users, user_id, password):

    for user in users:
        user = re.sub("[()]", "", user);
        existing_User = user.split(", ")
        existing_User[1] = existing_User[1].replace("\n", "")
        if existing_User[0] == user_id and existing_User[1] == password:
            return True

def update_file(user_id, password):

    new_user_info = "("+user_id+", "+password+")"
    with open("users.txt", "a") as f:
        f.write("\n")
        f.write(new_user_info)
    f.close()

def main():
    while True:
        data = conn.recv(1024).decode()
        commandWord = data.split(" ")[0]

        if(commandWord == "login"):
            if(isLoggedIn !=0):
                data = newUsername + " is already logged in!"
            else:
                try:
                    newUsername = data.split(" ")[1]
                    newPassword = data.split(" ")[2]
                    print("Login Failed.")
                    data = "Login failed. Please check username and password."
                    with open("users.txt", "r") as f:
                        for line in f:
                            if newUsername in line:
                                if newPassword in line:
                                    print(newUsername + " login")
                                    data = "Login Confirmed"
                                    isLoggedIn = 1
                except:
                    data = "Login failed. Please check username and password."
                finally:
                    f.close()
            conn.send(data.encode())

        elif(commandWord == "send"):

            if(isLoggedIn == 0):
                data = "Denied. Please Login First"

            elif(len(data.split(" ")[1]) > 256):
                data = "Message to log. Must be less than 256 characters"

            else:
                data = newUsername + ": " + data[5:]
                print (newUsername + " " + data[5:])

            conn.send(data.encode())

        elif(commandWord == "newuser"):
            users = read_users()

            if(isLoggedIn):
                conn.send("Cannot create new user while logged in.".encode())
                continue

            if new_user(users, data.split(" ")[1], data.split(" ")[2]):

                print("New user created.")
                users = read_users()
                conn.send("New user account created. Please login.".encode())
                continue

            else:

                conn.send("User account already exists.".encode())
                continue


        elif(commandWord == "logout"):

            if(isLoggedIn == 0):
                data = "You're not logged in"
                conn.send(data.encode())

            else:
                print(newUsername + " logout")
                data = newUsername + " left."
                conn.send(data.encode())
                isLoggedIn = isLoggedIn - 1

        else:
            print("Couldn't read input")
            data = "ERROR: Couldn't read input"
            conn.send(data.encode())

        if not data:
            break


conn, addr = sock.accept() #accepts connects from anyone

if connections < MAXCLIENTS:
    connections += 1
    Thread(target = main(), args = (conn, addr)).start()
else:
    conn.send("Sorry, there is max amount of active users".encode())

conn.close()
