import os
from datetime import datetime
from tabulate import tabulate
from .file_handler import FileHandler
from App.domain.Staff.food_menu import RestaurantMenu
from App.model.order_model import OrderModel, DraftItemModel, OrderConfig as CFG
from App.menu.All_menu import All_Menu
class Order:
    def __init__(self):
        self.file_manager = FileHandler()
        self.config = self.file_manager.get_config()
        self.menu_manager = RestaurantMenu()
        self.draft_items = [] 

    def get_validated_input(self, prompt, is_digit=False, min_val=None, max_val=None):
        while True:
            u_input = input(prompt).strip()
            if not u_input:
                print("Input field cannot be empty.")
                continue
            
            if is_digit:
                if not u_input.isdigit():
                    print("Invalid input. Please enter numeric digits only.")
                    continue
                val = int(u_input)
                if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                    print(f"Out of range! Please enter a value between {min_val} and {max_val}.")
                    continue
                return val
            return u_input

    def generate_order_id(self):
        return f"{datetime.now().strftime('%d%H%M%S')}"

    def display_order_draft(self):
        if not self.draft_items:
            print("\n" + "!"*20)
            print(" Your cart is empty. ".center(20))
            print("!"*20)
            return
        
        headers = ["#", "Item Name", "Qty", "Rate", "Subtotal"]
        table = [[i+1, item.item_name, item.quantity, item.price, item.subtotal] 
                 for i, item in enumerate(self.draft_items)]
        
        print("\n" + "═"*55)
        print("C U R R E N T   O R D E R   D R A F T".center(55))
        print("═"*55)
        print(tabulate(table, headers=headers, tablefmt="grid"))
        print(f"Total Amount Payable: Rs {sum(i.subtotal for i in self.draft_items)}")
        print("═"*55)

        remove_choice = input("\nRemove item? (Enter Item # to remove or press 'Enter' to skip): ").strip()
        if remove_choice:
            if remove_choice.isdigit():
                idx = int(remove_choice) - 1
                if 0 <= idx < len(self.draft_items):
                    removed = self.draft_items.pop(idx)
                    print(f"Successfully Removed: {removed.item_name}")
                else:
                    print("Invalid index! Item number does not exist in cart.")
            else:
                print("Error: Please provide a valid numeric item number.")

    def add_item_to_order(self):
        self.menu_manager.print_food_menu()
        while True:
            search_name = self.get_validated_input("\nEnter Food Name to add : ").lower()


            menu = self.menu_manager.menu_database['restaurant']['menu']
            found_item = None
            found_category = ""
            for cat_name, content in menu.items():
                items_to_search = content.get(CFG.KEY_VEG, []) + content.get(CFG.KEY_NONVEG, []) if isinstance(content, dict) else content
                for item in items_to_search:
                    if item[CFG.KEY_NAME].lower() == search_name:
                        found_item = item
                        found_category = cat_name.lower()
                        break
                if found_item: break

            if not found_item:
                print(f"ERROR: Item '{search_name}' was not found in our menu.")
                continue
            
            current_stock = found_item.get(CFG.KEY_STOCK, 0)
            if current_stock <= 0:
                print(f"\nSORRY! {found_item[CFG.KEY_NAME].upper()} is currently out of stock.")
                continue 
            break 

        selected_price = 0
        price_label = ""
        
  
        restricted_categories = ["dessert", "drink", "drinks", "breakfast", "beverage"]
        is_restricted = any(x in found_category for x in restricted_categories)

     
        if not is_restricted and CFG.KEY_HALF in found_item and found_item[CFG.KEY_HALF] not in ["-", 0, "0", None]:
            print(f"1. Half Portion - Rs.{found_item[CFG.KEY_HALF]} | 2. Full Portion - Rs.{found_item[CFG.KEY_FULL]}")
            p_choice = self.get_validated_input("Select Portion Size (1/2): ", is_digit=True, min_val=1, max_val=2)
            if p_choice == 1:
                selected_price = found_item[CFG.KEY_HALF]
                price_label = f"({CFG.TYPE_HALF})"
            else:
                selected_price = found_item[CFG.KEY_FULL]
                price_label = f"({CFG.TYPE_FULL})"
        else:
          
            selected_price = found_item.get(CFG.KEY_FULL, found_item.get('price', 0))
            price_label = "" 

        qty = self.get_validated_input(f"Enter quantity (Available Stock: {current_stock}): ", is_digit=True, min_val=1, max_val=current_stock)
        
        draft = DraftItemModel()
        draft.food_id = found_item[CFG.KEY_ID]
       
        draft.item_name = f"{found_item[CFG.KEY_NAME].upper()} {price_label}".strip()
        draft.quantity = qty
        draft.price = float(selected_price)
        draft.subtotal = draft.price * qty
        self.draft_items.append(draft)
        print(f"Added to cart: {draft.item_name}")

    def finalize_order(self):
        if not self.draft_items:
            print("\nCart is currently blank. Cannot finalize empty order.")
            return

        print("\n1. Walk-in Customer | 2. Table Booking Reservation")
        b_choice = self.get_validated_input("Select Customer Type (1/2): ", is_digit=True, min_val=1, max_val=2)

        order_id = self.generate_order_id()
        customer_name = CFG.DEFAULT_GUEST
        table_no = CFG.DEFAULT_TABLE 
        booking_fee = 0.0

        if b_choice == 2:
            while True:
                input_id = self.get_validated_input("Enter valid Booking ID : ").upper()

                
                table_bookings = self.file_manager.read_json(os.path.join(self.config.db_folder, 'table_book.json'))
                match = next((b for b in table_bookings if b.get('booking_id') == input_id), None)
                if match:
                    order_id = input_id
                    customer_name = match.get('customer_name', 'Guest')
                    table_no = match.get('table_number', CFG.DEFAULT_TABLE) 
                    booking_fee = float(match.get('booking_fee', 0))
                    break
                else:
                    print(" " \
                    " Error: Invalid Booking ID. Please try again.")

        self.save_order_to_file(order_id, customer_name, table_no, booking_fee)

    def save_order_to_file(self, order_id, customer_name, table_no, booking_fee):
        food_total = sum(i.subtotal for i in self.draft_items)
        order_data = {
            "order_id": order_id,
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": customer_name,
            "table_no": table_no,
            "booking_fee": booking_fee,
            "food_total": food_total,
            "grand_total": food_total + booking_fee,
            "items": [{"name": i.item_name, "qty": i.quantity, "subtotal": i.subtotal} for i in self.draft_items],
            "status": CFG.STATUS_COMPLETED
        }
        
        all_orders = self.file_manager.read_json(self.config.order_file)
        all_orders.append(order_data)
        if self.file_manager.write_json(self.config.order_file, all_orders):
            for d_item in self.draft_items:
                item_obj, _, _ = self.menu_manager.get_item_by_global_id(d_item.food_id)
                if item_obj: 
                    item_obj[CFG.KEY_STOCK] -= d_item.quantity
            self.menu_manager.save_menu_data()

            print(f"\n ORDER SUCCESSFULLY CONFIRMED! Order ID: {order_id}")
            print("-" * 45)
            print(f"Customer: {customer_name} | Table: {table_no}")
            for i in self.draft_items:
                print(f"• {i.item_name} x {i.quantity} (Subtotal: Rs.{i.subtotal})")
            print(f"Grand Total: Rs.{order_data['grand_total']}")
            print("-" * 45 + "\n")

            self.draft_items = [] 

    def run(self):
        while True:
            All_Menu().Add_menu()
            choice = self.get_validated_input("Select Option (1-4): ", is_digit=True, min_val=1, max_val=4)
            if choice == 1:
                self.add_item_to_order()
            elif choice == 2: 
                self.display_order_draft()
            elif choice == 3: 
                self.finalize_order()
            elif choice == 4: 
                break