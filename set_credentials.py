import utils
import os

# utils.install("cryptography")
"""
    central place to manage the credentials for the 
"""
import yaml

"""create menu system """

from cryptography.fernet import Fernet

# pswd = input("Profile password?")

menu = """

1. Add Credentials?
    - what is the name of the credential,
    - what is the username 
    - what is the password
2. View/Edit Password?
    - display list of credentials from file, index represents line number x is for exit
    - select index
    - enter old password, 
    - enter new password
    - display credentials 
"""
# print(pswd)


running = True

while running:
    main_menu = "Welcome to PasswordManager-v1 \n\n1. Add Credential.\n2. View/Edit Credential."
    print(main_menu)
    opt = input(">>")

    if opt in "Xx":

        print("you chose to exit the application")
    elif opt == "1":
        os.system('cls')
        sub_menu11 = "Name of Credential?"
        print(sub_menu11)
        opt11 = input(">>")
        sub_menu12 = "Username??"
        print(sub_menu12)
        opt12 = input(">>")
        sub_menu13 = "Username??"
        print(sub_menu13)
        opt13 = input(">>")

        # save and display credential
        print("you chose the first option")
    elif opt == "2":
        print("you chose the second option")
    else:
        print(f"incorrect input, {opt}. Please enter correct input")







# name of credentials (uname, password)
