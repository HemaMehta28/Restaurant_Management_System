import uuid
import pwinput
import os
import json
from .auth_validation import *
from ..model.restromodel import class_model

class Staff:
    @classmethod
    def get_input(cls, prompt, validator):
        while True:
            if "Password" in prompt:
                value = pwinput.pwinput(prompt)
            else:
                value = input(prompt)
            error = validator(value)
            if error:
                print("Error:", error)
            else:
                return value

    @classmethod
    def get_input_email(cls, prompt, validator, auth):
        while True:
            email = input(prompt)
            error = validator(email)
            if error:
                print("Error:", error)
            elif auth.check_email(email):
                print("Email already exists. Please try another email.")
            else:
                return email

    @classmethod
    def get_input_department(cls, prompt, validator):
        while True:
            print("Select Department:")
            print("1. Kitchen")
            print("2. Service")
            print("3. Management")
            choice = input(prompt)
            if choice.isdigit() and 1 <= int(choice) <= 3:
                departments = {1: "Kitchen", 2: "Service", 3: "Management"}
                return departments[int(choice)]
            else:
                print("Error: Invalid choice")

 

    @classmethod
    def signin(cls, auth):
        name = cls.get_input("Enter the name: ", validate_name)
        id = uuid.uuid4().hex[:4]
        email = cls.get_input_email("Enter the email: ", validate_email, auth)
        password = cls.get_input("Enter the Password:", validate_password)
        address = cls.get_input("Enter the address: ", validate_address)
        department = cls.get_input_department("Enter your choice: ", validate_department)
        experience = cls.get_input("Enter the experience (in years): ", validate_experience)
        role = "Staff"
        staff = class_model()
        staff.name = name
        staff.id = id
        staff.email = email
        staff.address = address
        staff.department = department
        staff.experience = experience
        staff.role = role
        staff.password = password
        return staff

class auth_class:
    def __init__(self):
        self.db_folder = 'App/database'
        self.db_file = 'staff.json'

    def check_email(self, email):
        file_path = os.path.join(self.db_folder, self.db_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
                for data in existing_data:
                    if data['email'] == email:
                        return True
        return False

    def save_to_db(self, data):
        file_path = os.path.join(self.db_folder, self.db_file)
        if os.path.exists(file_path):
            with open(file_path, 'r+') as file:
                existing_data = json.load(file)
                existing_data.append(data)
                file.seek(0)
                json.dump(existing_data, file, indent=4)
                file.truncate()
        else:
            with open(file_path, 'w') as file:
                json.dump([data], file, indent=4)

    def auth_main(self):
        staff = Staff.signin(self)
        if staff:
            print("Staff signed in successfully")
            staff_data = staff.__dict__
            if not os.path.exists(self.db_folder):
                os.makedirs(self.db_folder)
            self.save_to_db(staff_data)
            print("Data saved to database successfully")




