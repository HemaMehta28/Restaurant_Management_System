import os
import json
from App.model.order_model import RestaurantConfigModel
class FileHandler:
    def __init__(self):
        self.config = RestaurantConfigModel()
        self._initialize_paths()

    def _initialize_paths(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
        self.config.base_dir = app_dir
        self.config.db_folder = os.path.join(app_dir, 'database')
        self.config.menu_file = os.path.join(self.config.db_folder, 'Food_menu.json')
        self.config.order_file = os.path.join(self.config.db_folder, 'order.json')
        self.config.history_file = os.path.join(self.config.db_folder, 'order_history.json')
        self.config.order_record_file = os.path.join(self.config.db_folder, 'order_record.json')

        if not os.path.exists(self.config.db_folder):
            os.makedirs(self.config.db_folder)
        for file in [
            self.config.menu_file, self.config.order_file, 
            self.config.history_file, self.config.order_record_file
        ]:
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

      

    def get_config(self):
        return self.config

    def read_json(self, file_path):
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []

    def write_json(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f" Error writing {file_path}: {e}")
            return False
