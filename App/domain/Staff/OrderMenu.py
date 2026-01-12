import os
from tabulate import tabulate
from App.model.order_model import OrderModel, DraftItemModel
from .file_handler import FileHandler
from App.domain.Staff.food_menu import RestaurantMenu
from App.menu.All_menu import All_Menu
from .add_order import Order
from .Bill_generate import BillGenerator
from App.validation.Staff_validation import InputValidator

class Order_Menu:
    def __init__(self):
        self.file_manager = FileHandler()
        self.config = self.file_manager.get_config()
        self.restaurant_menu = RestaurantMenu(self.config.menu_file)
        self.validator = InputValidator()
    def load_orders(self):
        return self.file_manager.read_json(self.config.order_file)
    def show_all_orders(self):
        orders_data = self.load_orders()
        if not orders_data:
            print("\n" + "!"*45 + "\n INFORMATION: NO ACTIVE ORDERS FOUND \n" + "!"*45)
            return        
            
        print("\n" + "="*65)
        print(f"{'KITCHEN ACTIVE ORDERS':^65}")
        print("="*65)
        
        for i, data in enumerate(orders_data, start=1):
            o_id = data.get('order_id', 'N/A')
            o_date = data.get('order_date', 'N/A')
            c_name = data.get('customer_name', 'Guest')
            print(f"\n[ ORDER NO: {i:02d} ] | ID: {o_id}") 
            print(f"Customer: {c_name} | Time: {o_date}")
            
            table_data = []
            for item in data.get('items', []):
                name = item.get('name', 'Unknown')
                qty = item.get('qty', 0) 
                total = item.get('subtotal', 0)
                
                table_data.append([name, qty, f"Rs {total}"])
            print(tabulate(table_data, headers=['Item Name', 'Qty', 'Total Amount'], tablefmt='grid'))
            print("-" * 65)

    def handle_choice(self, choice):
        if choice == 5: 
            return False
        if choice == 1: 
            self.restaurant_menu.print_food_menu()
        elif choice == 2: 
            Order().run() 
        elif choice == 3: 
            self.show_all_orders()
        elif choice == 4:
            BillGenerator().generate_bill()
        return True
    def order_run(self):
        while True:
            All_Menu().Order_menu()
            choice = self.validator.get_choice("\nSelect (1-4) or press 0 to Back: ")
            if not self.handle_choice(choice):
                print("\nReturning to dashboard...")
                break