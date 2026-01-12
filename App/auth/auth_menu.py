import sys
from .auth_signin import auth_class
from .auth_login import Staff_login 
from ..model.Auth_model import class_model, FileConfigModel
from ..validation.auth_validation import Validator
from ..menu.All_menu import All_Menu

class Auth_Menu:
    @staticmethod
    def main_menu():
        config = FileConfigModel()
        validator = Validator()
        auth_service = auth_class(validator, class_model, config)
        login_service = Staff_login(config)
        while True:
            All_Menu.display_menu()
            while True:
                try:
                    choice = int(input("\nEnter choice (1-3): "))
                    
                    if choice in [1, 2, 3]:
                        break 
                    else:
                        print("Please enter 1,2 and 3.")
                except ValueError:
                    print("Please enter 1,2 and 3.")
            if choice == 1:
                login_service.login()
            elif choice == 2:
                auth_service.auth_main()
            elif choice == 3:
                print("Exiting...................!")
                sys.exit()