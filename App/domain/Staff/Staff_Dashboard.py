from App.domain.Staff.Table_booking import TableBookingUI
from App.domain.Staff.OrderMenu import Order_Menu
from App.domain.logger.staff_logger import StaffLogger
from App.menu.All_menu import All_Menu

class StaffDashboard:
    def __init__(self, staff_id=None, email=None):
        self.staff_id = staff_id or "Unknown"
        self.email = email or "Unknown"

    def log_action(self, message, log_type="INFO", function_name="Unknown"):
        StaffLogger.log(staff_id=self.staff_id, email=self.email, log_type=log_type,
                        function=function_name, message=message)

    def run(self):
        self.log_action("Opened Staff Dashboard", function_name="run")
        
        while True:
            try:
                All_Menu().display_dashboard()
                
                choice_input = input("\nEnter choice (1-3): ").strip()
                if not choice_input:
                    print("[!] Input Error: Please enter a choice.")
                    continue
                try:
                    choice = int(choice_input)
                    
                    if choice == 1:
                        self.log_action("Selected Take Food / Order", function_name="take_order")
                        Order_Menu().order_run()
                        
                    elif choice == 2:
                        self.log_action("Selected Table Booking", function_name="table_booking")
                        TableBookingUI().run()
                        
                    elif choice == 3:
                        self.log_action("Exited Staff Dashboard", function_name="exit")
                        print("\n[✔] Logging out... Have a great day!")
                        break
                        
                    else:
                        print(f"Validation Error: '{choice}' is not a valid option (1-3).")
                        self.log_action(f"Invalid range entered: {choice}", function_name="run")
                
                except ValueError:
                    print(f"[Type Error: '{choice_input}' is not a valid number. Please enter digits only.")
                    self.log_action(f"Non-numeric input: {choice_input}", log_type="WARNING", function_name="run")

            except Exception as e:
                StaffLogger.log(staff_id=self.staff_id, email=self.email,
                                log_type=type(e).__name__,
                                function="StaffDashboard.run", message=str(e))
                print(f"\n A Critical Error Occurred: {e}")
                print("Check the logs for technical details.")