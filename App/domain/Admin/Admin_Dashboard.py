import os
from App.domain.Staff.food_menu import RestaurantMenu
from App.domain.Admin.menu_management import MenuManagement
from App.menu.All_menu import All_Menu
from App.domain.Admin.order_management import AdminOrderManager
from App.domain.Admin.Staff_management import StaffManager
from App.validation.Admin_validation import AdminValidator
from App.domain.Admin.Inventory_management import Inventory
from App.domain.Admin.Report_management import ReportClass
from App.domain.logger.staff_logger import AdminLogger 

class AdminDashboard:
    def __init__(self, admin_id=None, email=None):
        self.admin_id = admin_id or "Unknown"
        self.email = email or "Unknown"
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir, '..', '..', 'database', 'food_menu.json')
        self.food_menu = RestaurantMenu(json_file_path)
        self.menu_management = MenuManagement(self.food_menu)
        self.admin_order = AdminOrderManager()

    def log_action(self, message, log_type="INFO", function_name="Unknown"):
        AdminLogger.log(admin_id=self.admin_id, email=self.email,
                        log_type=log_type, function=function_name, message=message)

    def run(self):
        self.log_action("Opened Admin Dashboard", function_name="run")
        while True:
            try:
                All_Menu().Admindashboard_menu()
                choice = AdminValidator.get_validated_input("\n>>> Selection (1-6): ", options=[1, 2, 3, 4, 5, 6])

                if choice == 1:
                    self.log_action("Selected Menu Management", function_name="menu_management")
                    self.menu_management.menu_management_sub_menu()

                elif choice == 2:
                    self.log_action("Selected Order Management", function_name="admin_order")
                    self.admin_order.run_admin_menu()

                elif choice == 3:
                    self.log_action("Selected Staff Management", function_name="staff_management")
                    StaffManager.run_staff_admin_menu()

                elif choice == 4:
                    self.log_action("Selected Inventory Management", function_name="inventory_management")
                    Inventory().run()

                elif choice == 5:
                    self.log_action("Selected Sales Report", function_name="run")
                    ReportClass().run()


                elif choice == 6:
                    self.log_action("Logged out from Admin Dashboard", function_name="exit")
                    print("\n---------\nLogout\n-----------\n")
                    break

            except Exception as e:
                self.log_action(f"Error: {str(e)}", log_type=type(e).__name__, function_name="run")
                print(" An error occurred. Check logs for details.")
