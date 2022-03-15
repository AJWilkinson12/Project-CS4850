#Created by AJ Wilkinson
#PawPrint: ASWD62  StudentID: 14307129

import socket
import re
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.getHOSTname()
PORT = 8002
isLoggedIn = 0
sock.bind((HOST,PORT))
sock.listen(3)

print ("Waiting for connection...")

conn, addr = sock.accept() #accepts connects from anyone

print("")
print("A client has connected!")
print("")


def read_users():
    with open("users.txt") as f:
        users = f.readlines()
    f.close()
    return users

def new_user(users, c_uid, c_pass):
    if check_match(users, c_uid, c_pass):
        return False
    else:
        update_users(c_uid, c_pass)
        return True

def check_match(users, c_uid, c_pass):
    for user in users:
        #Stripping each registered users extra characters
        user = re.sub("[()]", "", user);
        registered_u = user.split(", ")
        registered_u[1] = registered_u[1].replace("\n", "")
        #Check if current check variables match.
        if registered_u[0] == c_uid and registered_u[1] == c_pass:
            return True

def update_users(c_uid, c_pass):
    new_user = "("+c_uid+", "+c_pass+")"
    with open("users.txt", "a") as f:
        f.write("\n")
        f.write(new_user)
    f.close()


while True:
    data = conn.recv(1024).decode()
    commandWord = data.split(" ")[0]

    if(commandWord == "login"):
        if(isLoggedIn !=0):
            data = "Server: " + newUsername + " is already logged in!"
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
                                data = "Server: " + newUsername + " joins"
                                isLoggedIn = 1
            except:
                data = "Login failed. Please check username and password."
            finally:
                f.close()
        conn.send(data.encode())

    elif(commandWord == "send"):
        if(isLoggedIn == 0):
            data = "Server: Denied. Please Login First"
        else:
            data = newUsername + ": " + data[5:]
            print (newUsername + " " + data[5:])
        conn.send(data.encode())

    elif(commandWord == "newuser"):
        users = read_users()
        if(isLoggedIn):
            conn.send("Cannot create new user while logged  in.".encode())
            continue
        if new_user(users, data.split(" ")[1], data.split(" ")[2]):
            print("New user created.")
            users = read_users()
            conn.send("New user account created. Please login.".encode())
            continue
        else:
            conn.send("Denied. User account already exists.".encode())
            continue


    elif(commandWord == "logout"):
        if(isLoggedIn == 0):
            data = "You're not logged in"
            conn.send(data.encode())
        else:
            print(newUsername + " logout")
            data = "Server: " + newUsername + " left."
            conn.send(data.encode())
            isLoggedIn = isLoggedIn - 1

    else:
        print("Couldn't read input")
        data = "Server: couldn't read input"
        conn.send(data.encode())

    if not data:
        break


print("")
print("Client has disconnected!")
conn.close()
print("")
print("Exiting server...")
print("")
