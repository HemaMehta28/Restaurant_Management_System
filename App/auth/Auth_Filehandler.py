import os
import json
from App.model.Auth_model import LogModel, FileConfigModel

class FileHandler:
    def __init__(self, config: FileConfigModel):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = config.get_auth_path(self.current_dir)

    def read_all(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return []
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_one(self, data_dict):
        folder = os.path.dirname(self.file_path)
        if not os.path.exists(folder): os.makedirs(folder)
        data = self.read_all()
        data.append(data_dict)
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True

class AuthLogger:
    @staticmethod
    def write_log(uid, email, exc_type, func_name, message, config):
        log_obj = LogModel(uid, email, exc_type, func_name, message)
        path = config.get_log_path(os.path.dirname(os.path.abspath(__file__)))
        folder = os.path.dirname(path)
        if not os.path.exists(folder): os.makedirs(folder)
        with open(path, 'a') as f:
            f.write(log_obj.to_log_string())