import os
import sys
from tabulate import tabulate
from App.model.order_model import FoodMenuModel
from .file_handler import FileHandler
class RestaurantMenu:
    def __init__(self, database_path=None):
        self.file_manager = FileHandler()
        self.config = self.file_manager.get_config()
        self.database_path = database_path if database_path else self.config.menu_file
        self.menu_database = self.load_menu_data()
        if not self.menu_database or 'restaurant' not in self.menu_database:
            self.menu_database = self.get_initial_structure()
            self.save_menu_data()
        self.reorder_global_ids()

    def load_menu_data(self):
        return self.file_manager.read_json(self.database_path)

    def save_menu_data(self):
        return self.file_manager.write_json(self.database_path, self.menu_database)

    def get_initial_structure(self):
        return {"restaurant": {"name": "My Restaurant", "location": "India", "menu": {
            "starters": {"veg": [], "nonveg": []}, "mainCourse": {"veg": [], "nonveg": []},
            "drinks": [], "bread": [], "desserts": []}}}

    def reorder_global_ids(self):

        try:
            menu = self.menu_database['restaurant']['menu']
            next_id = 1
            categories = ['starters', 'mainCourse', 'drinks', 'bread', 'desserts']
            for cat in categories:
                content = menu.get(cat, [])
                if isinstance(content, dict):
                    for sec in ['veg', 'nonveg']:
                        for item in content.get(sec, []):
                            item['id'] = next_id
                            next_id += 1
                else:
                    for item in content:
                        item['id'] = next_id
                        next_id += 1
            self.save_menu_data()
        except Exception as e:
            print(f"[!] Reorder Error: {e}")


    def get_item_by_global_id(self, item_id):
   
        menu = self.menu_database['restaurant']['menu']
        for cat_name, content in menu.items():
            if isinstance(content, dict):
                for section in ['veg', 'nonveg']:
                    for item in content.get(section, []):
                        if item.get('id') == item_id:
                            return item, cat_name, section
            else:
                for item in content:
                    if item.get('id') == item_id:
                        return item, cat_name, None
        return None, None, None

    def update_item_data(self, category, item_id, updated_dict, sub_type=None):
        menu = self.menu_database['restaurant']['menu']
        target_list = menu[category][sub_type] if sub_type else menu[category]
        for i, item in enumerate(target_list):
            if item.get('id') == item_id:
                target_list[i] = updated_dict
                return self.save_menu_data()
        return False

    def delete_item(self, category, item_id, sub_type=None):
        menu = self.menu_database['restaurant']['menu']
        target_list = menu[category][sub_type] if sub_type else menu[category]
        original_count = len(target_list)
        target_list[:] = [item for item in target_list if item.get('id') != item_id]
        
        if len(target_list) < original_count:
            self.reorder_global_ids()
            return True
        return False

    def add_item(self, category, item_dict, sub_type=None):
        menu = self.menu_database['restaurant']['menu']
        target_list = menu[category][sub_type] if sub_type else menu[category]
        if 'stock' not in item_dict: item_dict['stock'] = 0.0
        target_list.append(item_dict)
        self.reorder_global_ids()

    def print_food_menu(self):
        res_info = self.menu_database.get('restaurant', {})
        menu_sections = res_info.get('menu', {})
        
        print("\n" + "═"*70)
        print(res_info.get('name', 'RESTAURANT').upper().center(70))
        print("═"*70)

        for title, key in [("S T A R T E R S", "starters"), ("M A I N   C O U R S E", "mainCourse")]:
            print(f"\n{title.center(70)}")
            print("   " + "─"*62)
            data = menu_sections.get(key, {})
            self._display_dual_columns(data.get('veg', []), data.get('nonveg', []))

        others = [("D R I N K S", 'drinks'), ("B R E A D S", 'bread'), ("D E S S E R T S", 'desserts')]
        for title, key in others:
            print(f"\n{title.center(70)}")
            print("   " + "─"*62)
            items = menu_sections.get(key, [])
            if not items:
                print(" " * 25 + "[ NO ITEMS ]")
                continue
            display_list = []
            for i in items:
                p = i.get('price', i.get('full', 0))
                display_list.append([f"ID:{i['id']}", i['name'].upper().ljust(35, '.'), f"Rs.{p}"])
            print(tabulate(display_list, tablefmt="plain"))

    def _display_dual_columns(self, veg_list, nonveg_list):
 
        header = f"{'ID':<4} {'VEGETARIAN':<20} {'HALF':<6} {'FULL':<6} | {'ID':<4} {'NON-VEG':<18} {'HALF':<6} {'FULL'}"
        print(header)
        print("─" * len(header))
        
        max_rows = max(len(veg_list), len(nonveg_list))
        if max_rows == 0:
            print(" " * 30 + "[ NO ITEMS ]")
            return

        for i in range(max_rows):
       
            if i < len(veg_list):
                v = veg_list[i]
                v_name = v.get('name', '').upper()[:19]
                v_h = v.get('half', '-') 
                v_f = v.get('full', 0)
                v_str = f"{v.get('id',''):<4} {v_name:<20} {v_h:<6} {v_f:<6}"
            else:
                v_str = " " * 38 

            if i < len(nonveg_list):
                nv = nonveg_list[i]
                nv_name = nv.get('name', '').upper()[:17]
                nv_h = nv.get('half', '-')
                nv_f = nv.get('full', 0)
                nv_str = f"{nv.get('id',''):<4} {nv_name:<18} {nv_h:<6} {nv_f}"
            else:
                nv_str = ""

            print(f"{v_str} | {nv_str}")