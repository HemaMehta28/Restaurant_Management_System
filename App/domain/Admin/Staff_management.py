import json
import os
from tabulate import tabulate
from App.validation.Admin_validation import AdminValidator
from App.model.Auth_model import UserRoles 
from App.model.database_model import DBFiles
from App.File_Handler.File_manager import JSONHandler
from App.menu.All_menu import All_Menu
class StaffManager:
    validator = AdminValidator()
    FILE_NAME = os.path.basename(DBFiles.AUTH)

    @staticmethod
    def load_all_staff():
        """Loads data via JSONHandler and filters by Staff role."""
        data = JSONHandler.load_data(StaffManager.FILE_NAME)
        if not data:
            return []
        return [u for u in data if str(u.get('role')).upper() == str(UserRoles.STAFF).upper()]

    @staticmethod
    def view_staff():
        staff = StaffManager.load_all_staff()
        if not staff:
            print(f"\nAccess Error: No {UserRoles.STAFF} records found in database.")
            return
        
        table_data = []
        for s in staff:
            sid = s.get('staff_id') or s.get('id') or 'N/A'
            name = s.get('name', 'N/A').upper()
            dept = s.get('department', 'N/A').upper()
            phone = s.get('phone_number') or 'N/A'
            email = s.get('email', 'N/A')
            table_data.append([sid, name, dept, phone, email])
        
        print("\n" + "═"*80)
        print(f" {UserRoles.STAFF.upper() + ' MASTER DIRECTORY' : ^74}")
        print("═"*80)
        print(tabulate(table_data, headers=['ID', 'NAME', 'DEPARTMENT', 'PHONE', 'EMAIL'], tablefmt='fancy_grid'))

    @staticmethod
    def remove_staff():
        staff_list = StaffManager.load_all_staff()
        if not staff_list:
            print(f"\nSystem Message: No staff members available to remove.")
            return

        StaffManager.view_staff()
        
        raw_id = input(f"\nEnter {UserRoles.STAFF} ID to remove (or '0' to cancel): ").strip()
        if raw_id == '0': return

        target = next((s for s in staff_list if str(s.get('staff_id')) == raw_id 
                       or str(s.get('id')) == raw_id), None)

        if target:
            print(f"\n  Are you sure you want to permanently delete {target.get('name')}?")
            confirm = input("Select Action (1: Confirm Delete | 2: Cancel): ").strip()
            
            if confirm == '1':
                all_users = JSONHandler.load_data(StaffManager.FILE_NAME)
                final_list = [u for u in all_users if not (
                    (str(u.get('staff_id')) == raw_id or str(u.get('id')) == raw_id)
                    and str(u.get('role')).upper() == str(UserRoles.STAFF).upper()
                )]
                
                if JSONHandler.save_data(StaffManager.FILE_NAME, final_list):
                    print(f"\n[SUCCESS] Staff member '{target.get('name')}' has been removed.")
            else:
                print("\nOperation cancelled by user.")
        else:
            print(f"\nError: No staff member found with ID '{raw_id}'.")

    @staticmethod
    def run_staff_admin_menu():
        while True:
            All_Menu.ManageStaff()
            
            choice_input = input("\nEnter selection (1-3): ").strip()
            
            if not choice_input:
                print("Input Error: Selection cannot be empty.")
                continue

            try:
                choice = int(choice_input)
                if choice == 1:
                    StaffManager.view_staff()
                elif choice == 2:
                    StaffManager.remove_staff()
                elif choice == 3:
                    print("[*] Returning to Admin Dashboard...")
                    break
                else:
                    print(f"Validation Error: '{choice}' is out of range. Please choose 1, 2, or 3.")
            
            except ValueError:
                print(f"Input Error: '{choice_input}' is not a valid number. Please enter a digit.")