import json
import os

class JSONHandler:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def load_data(filename):
        path = os.path.join(JSONHandler.BASE_DIR, 'database', filename)
        
        if not os.path.exists(path):
            print(f"[!] File not found at: {path}")
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Load Error: {e}")
            return []