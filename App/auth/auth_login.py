import pwinput
import os
import json
from .auth_validation import validate_email

class Staff_login:
    def __init__(self):
        self.db_folder = 'App/database'
        self.db_file = 'staff.json'
        self.admin_email = 'admin@gmail.com'
        self.admin_password = 'admin123'

    def check_email(self, email):
        file_path = os.path.join(self.db_folder, self.db_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
            for data in existing_data:
                if data['email'] == email:
                    return True
        return False

    def check_credentials(self, email, password):
        if email == self.admin_email and password == self.admin_password:
            return True
        file_path = os.path.join(self.db_folder, self.db_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
            for data in existing_data:
                if data['email'] == email and data['password'] == password:
                    return True
        return False

    def login(self):
        while True:
            print("1. Staff Login")
            print("2. Admin Login")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    email = input("Enter your email: ")
                    if not self.check_email(email):
                        print("Invalid email.Please enter a valid email.")
                        continue
                    while True:
                        password = pwinput.pwinput("Enter your password: ")
                        if self.check_credentials(email, password):
                            print("--------------------\nLOGIN sUCCESSFUL\n--------------------")
                            return
                        else:
                            print("Invalid password. Please try again.")
                elif choice == 2:
                    email = input("Enter admin email: ")
                    password = pwinput.pwinput("Enter admin password: ")
                    if email == self.admin_email and password == self.admin_password:
                        print("Admin login successful!")
                        return
                    else:
                        print("Invalid admin credentials.")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")