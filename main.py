import json
import os

user_file=os.path.join("login","users.json")

def load_user():#Reads users from the file

    if not os.path.exists(user_file):#if file doesnt exist
        return{}

    with open(user_file, "r") as f:
        try:
            return json.load(f)#reads file
        except json.JSONDecodeError:#if empty
            return {}

def save_user(users):
    os.makedirs(os.path.dirname(user_file), exist_ok=True)
    with open(user_file, "w") as f:
        json.dump(users, f)#converts users to json

def register_user():
    users=load_user()

    username=input("Enter your username: ")

    if username=="":#check if username is empty
        print("Please enter a username.")
        return

    if username in users:#check if username already in file
        print("Username already in use.")
        return

    password=input("Enter your password: ")

    if password=="":#check if password empty
        print("Please enter a password.")
        return

    passwordcheck=input("Please Enter your password again: ")#user has to reenter password
    if passwordcheck!=password:
        print("Passwords do not match.")
        return

    users[username]=password#adds new user
    save_user(users)#saves
    print(f'{username}' " registered successfully")

def login_user():
    users=load_user()

    username=input("Enter your username ")
    password=input("Please enter your password ")

    if username in users and users[username]==password:
        print("Login successful")
        return username
    else:
        print("Login unsuccessful")
        return None

def loginmenu():
    while True:
        print("Welcome to the bug tracker \n 1. Register a new user\n 2. Log In\n 3. Exit ")
        Selection=input("Please select a number (1-3) ")

        if Selection=="1":
            register_user()

        elif Selection=="2":
            login_user()

        elif Selection=="3":
            break

        else:
            print("Invalid selection")

loginmenu()