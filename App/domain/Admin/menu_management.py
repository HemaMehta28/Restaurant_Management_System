from tabulate import tabulate
from App.validation.Admin_validation import AdminValidator
from App.menu.All_menu import All_Menu
class MenuManagement:
    def __init__(self, food_menu_obj):
        self.food_menu = food_menu_obj
        self.validator = AdminValidator()

    def menu_management_sub_menu(self):
        while True:
            All_Menu.MenuManagement_menu()
            choice_input = input("\nSelection (1-5): ").strip()
            try:
                choice = int(choice_input)
                if choice == 1: 
                    self.view_full_menu()
                elif choice == 2: 
                    self.add_new_item()
                elif choice == 3: 
                    self.update_global_item()
                elif choice == 4: 
                    self.delete_global_item()
                elif choice == 5: 
                    break
                else:
                    print(f" Invalid Option: {choice}. Please select 1 to 5.")
            except ValueError:
                print(f"Input Error: '{choice_input}' is not a number. Please enter a digit.")

    def view_full_menu(self):
        menu_ref = self.food_menu.menu_database['restaurant']['menu']
        display_table = []
        
        for category_name, content in menu_ref.items():
            if isinstance(content, dict):
                for section in ['veg', 'nonveg']:
                    for item in content.get(section, []):
                        price_info = f"H:₹{item.get('half','-')} | F:₹{item.get('full','-')}"
                        display_table.append([
                            item['id'], item['name'].upper(), 
                            f"{category_name.upper()} ({section})", 
                            price_info, f"{item.get('stock', 0.0)} Qty"
                        ])
            else:
                for item in content:
                    display_table.append([
                        item['id'], item['name'].upper(), 
                        category_name.upper(), 
                        f"Price: ₹{item.get('price','-')}", f"{item.get('stock', 0.0)} Qty"
                    ])
        
        headers = ["ID", "ITEM NAME", "CATEGORY", "PRICE DETAILS", "STOCK"]
        print("\n" + tabulate(display_table, headers=headers, tablefmt="fancy_grid"))

    def add_new_item(self):
        print("\n" + "─"*20 + " ADD NEW ITEM " + "─"*20)
        print("1.Starters | 2.Main Course | 3.Drinks | 4.Bread | 5.Desserts")
        category_map = {1:'starters', 2:'mainCourse', 3:'drinks', 4:'bread', 5:'desserts'}
        
        try:
            cat_choice = int(input("Select Category (1-5): "))
            if cat_choice not in category_map:
                print("Invalid Category Selection."); return
            
            category = category_map[cat_choice]
            sub_type = None
            
            if category in ['starters', 'mainCourse']:
                st_choice = int(input("1. Veg | 2. Non-Veg: "))
                if st_choice not in [1, 2]:
                    print("[!] Invalid Sub-type."); return
                sub_type = 'veg' if st_choice == 1 else 'nonveg'

            name = input("Enter Item Name: ").strip()
            if not name: print("Name cannot be empty."); return
            
            new_item = {"name": name, "stock": 0.0}

            if category in ['starters', 'mainCourse']:
                new_item["half"] = int(input("Half Plate Price: "))
                new_item["full"] = int(input("Full Plate Price: "))
            else:
                new_item["price"] = int(input("Price: "))

            self.food_menu.add_item(category, new_item, sub_type)
            print(f"\n✔ '{name.upper()}' added successfully to {category}!")

        except ValueError:
            print("Error: Numeric value expected for prices/selection.")

    def update_global_item(self):
        self.view_full_menu()
        try:
            item_id = int(input("\nEnter ID to Update: "))
            item, category, sub_type = self.food_menu.get_item_by_global_id(item_id)
            
            if not item:
                print("ID not found!"); return

            print(f"--- Updating: {item['name'].upper()} ---")
            new_name = input(f"New Name [{item['name']}]: ").strip()
            if new_name: item['name'] = new_name
            
            if 'price' in item:
                p = input(f"New Price [₹{item['price']}]: ").strip()
                if p: item['price'] = int(p)
            else:
                h = input(f"New Half Price [₹{item['half']}]: ").strip()
                f = input(f"New Full Price [₹{item['full']}]: ").strip()
                if h: item['half'] = int(h)
                if f: item['full'] = int(f)

            if self.food_menu.update_item_data(category, item_id, item, sub_type):
                print(f"[SUCCESS] {item['name']} updated.")
        except ValueError:
            print("Error: Invalid numeric input.")

    def delete_global_item(self):
        self.view_full_menu()
        try:
            item_id = int(input("\nEnter ID to Delete: "))
            item, category, sub_type = self.food_menu.get_item_by_global_id(item_id)
            
            if item:
                confirm = input(f"Confirm Delete '{item['name']}'? (y/n): ").lower()
                if confirm == 'y':
                    if self.food_menu.delete_item(category, item_id, sub_type):
                        print(f"[SUCCESS] '{item['name']}' removed from menu.")
            else:
                print("ID not found.")
        except ValueError:
            print(" Error: Please enter a valid numeric ID.")