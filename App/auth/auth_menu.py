from .auth_signin import auth_class
from .auth_login import Staff_login

class MainMenu:
    def __init__(self):
        self.auth_signin = auth_class()
        self.auth_login = Staff_login()

    def display_menu(self):
        print("1. Login")
        print("2. Signin")
        print("3. Exit")

    def main_menu(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.auth_login.login()
            elif choice == "2":
                self.auth_signin.auth_main()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

