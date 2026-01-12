import os
from datetime import datetime

class UserRoles:
    ADMIN = "Admin"
    STAFF = "Staff"

class class_model:
    def __init__(self):
        self.name = None
        self.staff_id = None
        self.email = None
        self.address = None
        self.phone_number = None
        self.department = None
        self.role = None
        self.password = None

    def to_dict(self):
        return self.__dict__

class FileConfigModel:
    def __init__(self, folder='database', auth_file='auth_user.json', log_folder='logs', log_file='auth_logs.txt'):
        self.folder = folder
        self.auth_file = auth_file
        self.log_folder = log_folder
        self.log_file = log_file

    def get_auth_path(self, base_path):
        return os.path.normpath(os.path.join(base_path, '..', self.folder, self.auth_file))

    def get_log_path(self, base_path):
        return os.path.normpath(os.path.join(base_path, '..', self.log_folder, self.log_file))

class LogModel:
    def __init__(self, uid, email, exc_type, func_name, message):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.uid = uid 
        self.email = email
        self.exc_type = exc_type
        self.func_name = func_name
        self.message = message

    def to_log_string(self):
        return (f"[{self.timestamp}] | ID: {self.uid} | Email: {self.email} | "
                f"Type: {self.exc_type} | Message: {self.message}\n")