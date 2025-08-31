import mysql.connector
from getpass import getpass
import random
#connect to Mysql 
db = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "Aswin@1636",
    database = "password_generator"
)
cursor = db.cursor()
# global variable is very important for this code  
logged_in_user = None
#Create account
def create_account():
    global logged_in_user
    username = input("Enter a Username : ")
    email = input("Enter your email : ")
    password = getpass("Enter Password : ")
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email , password))
    db.commit()
    query = "SELECT id FROM users WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    if result :
        logged_in_user = result[0]
        print ("\nAccount Created Successfully!! ")
        after_login()

#Login
def login():
        global logged_in_user
        email = input("Enter your email : ")
        password = getpass("Enter your password : ")
        query = "SELECT id FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        if result :
            logged_in_user = result[0]
            print ("\nLogin Successfully!! ")
        else:
            print ("\nInvalid password or email")

def after_login():
    global logged_in_user
    while logged_in_user:
        print("\n------Welcome to password manager------\n")
        print("1. Generate Password")
        print("2. Show saved password")
        print("3. Save your own password")
        print("4. Delete saved password")
        print("5. Update your saved password")
        print("6. Logout")
        print("7. Delect account\n")
        sub_choice = input("Enter your choice : ")

        # -----generate password-----

        if sub_choice == "1":
                char = (
                    "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM7896541230!@#$%^&*"
                )
                generated_password = ""
                length = int(input("\nEnter the length of requried password : "))
                for i in range(length):
                    generated_password += random.choice(char)
                print ("\n -----Generated Password-----\n ", generated_password)
                sav = input("\n Do you want to save this Password ?--[yes/no] : ").lower()
                if sav == "yes" :
                    password_name = input("\nEnter name of your passwaord : ")
                    query = "INSERT INTO passwords (user_id, password_name , generated_password) VALUES (%s,%s,%s)"
                    cursor.execute(query,(logged_in_user, password_name , generated_password)) 
                    db.commit()
                    print ("\n Password for ",password_name," is saved")
                elif sav == "no" :
                    print ("\nComeback again")        
                else :
                    print ("\n Invalid option")

        #------show saved password------

        elif sub_choice == "2":
            print("\n--- Saved Passwords ---\n")
            query = "SELECT password_name, generated_password, created_at FROM passwords WHERE user_id=%s ORDER BY created_at DESC"
            cursor.execute(query,(logged_in_user,))
            rows = cursor.fetchall()
            if not rows:
                print("\nNo saved password found.")
            else:
                for idx, row in enumerate(rows, 1):
                    print(f"\n {idx}. {row[0]}  |<->|  {row[1]}  |<->|  {row[2].strftime('%d/%m/%Y %I:%M %p')}")
        
        #-------save own password---------

        elif sub_choice == "3":
            password_name = input("\nEnter the name for your password : ")
            custom_password = input("Enter the password you want to save : ")
            query = "INSERT INTO passwords (user_id, password_name , generated_password) VALUES (%s,%s,%s)"
            cursor.execute(query, (logged_in_user, password_name, custom_password))
            db.commit()
            print("\n Your password for", password_name, "has been saved successfully!")

        #-------delete saved password-------

        elif sub_choice == "4":
            name_to_delete = input("\n Enter the password name to delete : ")
            query = "DELETE FROM passwords WHERE user_id=%s AND password_name=%s"
            cursor.execute(query,(logged_in_user,name_to_delete))
            db.commit()
            if cursor.rowcount > 0:
                print("\n Password deleted successfully!")
            else:
                print("\n No password found with that name.")  

        # -------Update saved password-------
        elif sub_choice == "5":
            name_to_update = input("\nEnter the password name to update: ")
            new_password = input("Enter the new password: ")
            query = "UPDATE passwords SET generated_password=%s, created_at=NOW() WHERE user_id=%s AND password_name=%s"
            cursor.execute(query, (new_password, logged_in_user, name_to_update))
            db.commit()
            if cursor.rowcount > 0:
                print("\n Password updated successfully!")
            else:
                print("\n No password found with that name.")

        #-------Logout------

        elif sub_choice == "6":
            logged_in_user = None
            print ("\n Logged out Successfully!!")

        #---------Delete account---------

        elif sub_choice == "7":
            delete_account()
            return

        else:
            print ("\n Invalid choice")



#Delete account 
def delete_account():
    global logged_in_user
    email = input("Enter your email : ")
    password = getpass("Enter your password : ")
    reenter = getpass("Re-enter your password : ")
    if password != reenter:
        print ("\n Password do not match!!")
        return
    query = "SELECT id FROM users WHERE email=%s AND password=%s"
    cursor.execute(query,(email, password))
    result = cursor.fetchone()
    if result and result[0] == logged_in_user:
        # Delete user’s passwords first (foreign key constraint safety)
        query1 = "DELETE FROM passwords WHERE user_id=%s"
        cursor.execute(query1, (logged_in_user,))
        # delete user account
        query2 = "DELETE FROM users WHERE id=%s"
        cursor.execute(query2, (logged_in_user,))
        db.commit()
        print("\nAccount Deleted Successfully!!")
        logged_in_user = None   
    else:
        print ("\n No account is found with this cretentials")


def password_generator():
    global logged_in_user
    char = (
            "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM7896541230!@#$%^&*"
        )
    generated_password = ""
    length = int(input("\nEnter the length of requried password : "))
    for i in range(length):
        generated_password += random.choice(char)
    print ("\n -----Generated Password-----\n \n", generated_password)
    sav = input("\n Do you want to save this Password ?--[yes/no] : ").lower()
    if sav == "yes" :
        if not logged_in_user:
            print("\n You must login first to save your password!")
            return
        password_name = input("\nEnter name of your passwaord : ")
        query = "INSERT INTO passwords (user_id, password_name , generated_password) VALUES (%s,%s,%s)"
        cursor.execute(query,(logged_in_user, password_name , generated_password)) 
        db.commit()
        print ("\n Password for ",password_name," is saved")
    elif sav == "no" :
        print ("\n Okay come again")        
    else :
        print ("\n Invalid option") 

def menu():
        global logged_in_user
        while True:
            if not logged_in_user:
                print ("\n-----Welcome to Password Manager-----\n")
                print ("1. Generate password")
                print ("2. Create Account")
                print ("3. Loign")
                print ("4. Exit\n")    
                select_option = input("Enter your choice : ")
                if select_option == "1":
                    password_generator()
                elif select_option == "2":
                    create_account()
                elif select_option == "3":
                    login()
                elif select_option == "4":
                    print ("\n Good Bye!!")
                    break
                else:
                    print ("\n Invalid choice")
            else:
                after_login()
menu()