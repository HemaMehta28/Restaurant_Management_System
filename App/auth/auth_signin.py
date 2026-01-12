import uuid
import pwinput
from .Auth_Filehandler import FileHandler, AuthLogger
from ..model.Auth_model import UserRoles, FileConfigModel

class Staff:
    @classmethod
    def get_input(cls, prompt, validator_func):
        while True:
            value = pwinput.pwinput(prompt) if "Password" in prompt else input(prompt)
            error = validator_func(value)
            if error: 
                print(f"Error: {error}")
            else: 
                return value

    @classmethod
    def get_input_email(cls, prompt, auth_instance, validator):
        while True:
            email = input(prompt)
            error = validator.validate_email(email)
            if error: 
                print(f"Error: {error}")
            elif auth_instance.check_email(email): 
                print("Error: Email already exists. Please try another.")
            else: 
                return email

    @classmethod
    def get_input_department(cls):
        while True:
            print("\nSelect Department:\n1. Kitchen\n2. Service\n3. Management")
            choice = input("Enter your choice (1-3): ")
            departments = {"1": "Kitchen", "2": "Service", "3": "Management"}
            if choice in departments:
                return departments[choice]
            else:
                print("Error: Invalid choice.")

    @classmethod
    def signin(cls, auth_instance, validator, model_class, role):
        print(f"\n{'='*25} {role} Registration {'='*25}")
        try:
            user_obj = model_class()
            user_obj.name = cls.get_input("Enter Name: ", validator.validate_name)
            user_obj.email = cls.get_input_email("Enter Email: ", auth_instance, validator)
            user_obj.password = cls.get_input("Enter Password: ", validator.validate_password)
            user_obj.phone_number = cls.get_input("Enter Phone Number: ", validator.validate_phone_number)
            user_obj.address = cls.get_input("Enter Address: ", validator.validate_address)
            user_obj.department = cls.get_input_department()
            user_obj.staff_id = uuid.uuid4().hex[:4].upper()
            user_obj.role = role
            return user_obj
        except Exception as e:
            print(f"Error during input: {e}")
            return None

class auth_class:
    def __init__(self, validator_instance, model_class, config_instance):
        self.db = FileHandler(config=config_instance)
        self.validator = validator_instance
        self.model_class = model_class
        self.config = config_instance

    def check_email(self, email):
        users = self.db.read_all()
        return any(u.get('email') == email for u in users)

    def auth_main(self):
        users = self.db.read_all()
        role = UserRoles.ADMIN if not users else UserRoles.STAFF
        staff_obj = Staff.signin(self, self.validator, self.model_class, role)
        
        if staff_obj:
            if self.db.save_one(staff_obj.to_dict()):
                AuthLogger.write_log(staff_obj.staff_id, staff_obj.email, "None", "Signin", "Success", self.config)
                print(f"\n[✔] {role} Registered Successfully! ID: {staff_obj.staff_id}")