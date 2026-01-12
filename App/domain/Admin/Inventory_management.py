import os
from tabulate import tabulate
from App.domain.Staff.file_handler import FileHandler 
from App.model.order_model import InventoryModel
from App.menu.All_menu import All_Menu
class Inventory:
    def __init__(self):
        self.handler = FileHandler()
        self.config = self.handler.get_config()
        self.menu_path = self.config.menu_file

    def load_inventory_objects(self):
        data = self.handler.read_json(self.menu_path)
        if not data: return [], None
        obj_list = []
        menu = data.get('restaurant', {}).get('menu', {})
        for cat, items in menu.items():
            content = items.values() if isinstance(items, dict) else [items]
            for sub_list in content:
                for i in sub_list:
                    obj = InventoryModel(i.get('id'), i.get('name'), i.get('stock', 0))
                    obj.category = cat 
                    obj_list.append(obj)
        return obj_list, data

    def view_stock(self):
        objs, _ = self.load_inventory_objects()
        if not objs: return
        objs.sort(key=lambda x: int(x.id) if x.id.isdigit() else 999)
        table = [[o.id, o.name.upper(), o.category.upper(), o.current_stock, o.status_tag] for o in objs]
        print("\n" + "═"*78 + f"\n{'I N V E N T O R Y   R E P O R T':^78}\n" + "═"*78)
        print(tabulate(table, headers=["ID", "Item Name", "Category", "Qty", "Status"], tablefmt="fancy_grid"))

    def add_stock(self):
        objs, full_data = self.load_inventory_objects()
        
        print("\n" + "─"*40)
        query = input("Enter Full Item Name or ID: ").strip().lower()
        print("─"*40)

        if not query:
            print("Input cannot be empty.")
            return

        sel = None
        for o in objs:
            if o.name.lower() == query or str(o.id) == query:
                sel = o
                break
        if not sel:
            print(f"Invalid Selection: No exact match found for '{query}'.")
            print("(Tip: Please enter the complete name as shown in the report)")
            return
        try:
            print(f"\nITEM FOUND: {sel.name.upper()}")
            print(f"Current Stock: {sel.current_stock}")
            
            qty_input = input(f"Enter Qty to add: ").strip()
            if not qty_input:
                print("Quantity is required.")
                return

            add_qty = float(qty_input)
            
            if add_qty < 0:
                print("Error: Cannot add negative stock.")
                return

            sel.current_stock += add_qty

            self._update_json_file(full_data, sel)
            print(f"Success! {sel.name.upper()} updated to {sel.current_stock}")

        except ValueError:
            print(" Error: Invalid numeric value for quantity.")
        
     

    def _update_json_file(self, data, updated_obj):
        menu = data['restaurant']['menu']
        for cat, items in menu.items():
            content = items.values() if isinstance(items, dict) else [items]
            for sub_list in content:
                for i in sub_list:
                    if str(i.get('id')) == str(updated_obj.id):
                        i['stock'] = updated_obj.current_stock
        
        self.handler.write_json(self.menu_path, data)

    def run(self):
        while True:
            All_Menu.ManageInventry()
            
            choice_input = input("\nEnter your choice (1-3): ").strip()
            if not choice_input:
                print("Selection cannot be empty.")
                continue

            try:
                choice = int(choice_input)
                if choice == 1: 
                    self.view_stock()
                elif choice == 2: 
                    self.add_stock()
                elif choice == 3: 
                    print("Exiting Inventory System...")
                    break
                else:
                    print(f"Invalid Option ({choice}): Please select between 1 and 3.")
            
            except ValueError:
                print(f"Type Error: '{choice_input}' is not a valid number. Use integers only.")
            