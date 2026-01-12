
from App.report.Food_report import ReportManager  
from App.report.Table_report import BookingReportManager
from App.report.Bill_report import BillReportManager
from App.menu.All_menu import All_Menu
class ReportClass:
    """Handles the menu for various system reports with integer validation.""" 
    def __init__(self):
        self.food_manager = ReportManager()

    def run(self):
        while True:
            All_Menu.Report_menu()   
            try:
                user_input = input("\nEnter Choice (1-4): ").strip()
                if not user_input:
                    print("[!] Input cannot be empty. Please enter a number.")
                    continue
                
                choice = int(user_input)
                if choice == 1:
                    self.food_manager.show_report()
                elif choice == 2:
                    BookingReportManager.display_report()
                elif choice == 3:
                    BillReportManager.display_report()
                elif choice == 4:
                    print(" Returning to Main Menu...")
                    break
                else:
                    print(f" {choice} is out of range. Please select 1, 2, 3, or 4.")

            except ValueError:
                print("Invalid Input. Please enter a numeric value (1-4).")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
