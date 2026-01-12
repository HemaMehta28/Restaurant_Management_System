
import os
from datetime import datetime

class StaffLogger:

    @staticmethod
    def _log_path():
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        log_dir = os.path.join(base_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, "staff.txt")

    @staticmethod
    def log(staff_id=None, email=None, log_type="INFO", function="Unknown", message=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff_id = staff_id or "Unknown"
        email = email or "Unknown"
        log_line = f"[{timestamp}] | ID: {staff_id} | Email: {email} | Type: {log_type} | Function: {function} | Message: {message}\n"
        with open(StaffLogger._log_path(), "a", encoding="utf-8") as f:
            f.write(log_line)

class AdminLogger:

    @staticmethod
    def _log_path():
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        log_dir = os.path.join(base_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, "admin.txt")

    @staticmethod
    def log(admin_id=None, email=None, log_type="INFO", function="Unknown", message=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        admin_id = admin_id or "Unknown"
        email = email or "Unknown"
        log_line = f"[{timestamp}] | ID: {admin_id} | Email: {email} | Type: {log_type} | Function: {function} | Message: {message}\n"
        with open(AdminLogger._log_path(), "a", encoding="utf-8") as f:
            f.write(log_line)
