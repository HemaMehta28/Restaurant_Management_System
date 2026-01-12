import re

class Validator:
    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email):
            return None
        return "Invalid email"

    def validate_name(self, name):
        pattern = r"^[a-zA-Z\s]+$"
        if re.match(pattern, name):
            return None
        return "Name should only contain letters and spaces"

    def validate_address(self, address):
        pattern = r"^[a-zA-Z0-9\s,.-]+$"
        if re.match(pattern, address):
            return None
        return "Address should only contain letters, numbers, and spaces"

    def validate_department(self, department):
        return None

    def validate_role(self, role):
        return None

    def validate_password(self, password):
        if not password:
            return "Password is required"
        if len(password) < 8:
            return "Password should be at least 8 characters"
        if not any(char.isupper() for char in password):
            return "Password should have at least one uppercase letter"
        if not any(char.islower() for char in password):
            return "Password should have at least one lowercase letter"
        if not any(char.isdigit() for char in password):
            return "Password should have at least one number"
        if not any(not char.isalnum() for char in password):
            return "Password should have at least one special symbol"
        return None

    def validate_phone_number(self, phone_number):
        pattern = re.compile(r'^[1-9]\d{9}$')
        if pattern.match(phone_number):
            return None
        else:
            return "Invalid phone number. Please enter a 10-digit phone number that does not start with 0."

   

