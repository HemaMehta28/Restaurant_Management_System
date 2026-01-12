import os
from tabulate import tabulate
from App.domain.Staff.file_handler import FileHandler 
from App.model.order_model import OrderModel, OrderItemModel
from App.menu.All_menu import All_Menu
class AdminOrderManager:
    def __init__(self):
        self.handler = FileHandler()
        self.config = self.handler.get_config()
        self.order_path = self.config.order_file
    def _map_to_models(self):
        """Maps JSON data to Objects and recalculates Unit Price if missing."""
        raw_data = self.handler.read_json(self.order_path)
        if not raw_data: return []
        
        order_list = []
        for d in raw_data:
            o = OrderModel()
            o.order_id = d.get('order_id')
            o.customer_name = d.get('customer_name')
            o.booking_fee = float(d.get('booking_fee', 0))
            
            for it in d.get('items', []):
                item = OrderItemModel()
                item.name = it.get('name')
                item.qty = int(it.get('qty', 1))
                item.subtotal = float(it.get('subtotal', 0))
                if 'price' in it and float(it['price']) > 0:
                    item.price = float(it['price'])
                else:
                    item.price = item.subtotal / item.qty if item.qty > 0 else 0
                
                o.items.append(item)
            
            self.refresh_bill(o) 
            order_list.append(o)
        return order_list

    def _save_models(self, models):
        """Saves models back to JSON format."""
        data = []
        for o in models:
            order_dict = {
                "order_id": o.order_id,
                "customer_name": o.customer_name,
                "booking_fee": o.booking_fee,
                "food_total": o.food_total,
                "grand_total": o.grand_total,
                "items": [{"name": it.name, "qty": it.qty, "price": it.price, "subtotal": it.subtotal} for it in o.items]
            }
            data.append(order_dict)
        return self.handler.write_json(self.order_path, data)

    def refresh_bill(self, order_obj):
        order_obj.food_total = sum(float(it.subtotal) for it in order_obj.items)
        order_obj.grand_total = order_obj.food_total + order_obj.booking_fee

    def manage_orders_flow(self, mode):
        orders = self._map_to_models()
        if not orders:
            print("\nNo active orders found.")
            return

        summary = [[i+1, o.order_id, o.customer_name, f"Rs {o.grand_total:,.2f}"] for i, o in enumerate(orders)]
        print(f"\n{'SELECT ORDER TO ' + mode.upper():^60}\n" + "═"*60)
        print(tabulate(summary, headers=['SN', 'Order ID', 'Customer', 'Total'], tablefmt='fancy_grid'))

        try:
            choice = int(input(f"\nEnter S.No (1-{len(orders)}) or 0 to Back: ").strip())
            if choice == 0: 
                return
            idx = choice - 1
            if 0 <= idx < len(orders):
                if mode == "Modify": 
                    self.perform_modify(orders, idx)
                elif mode == "Cancel": 
                    self.perform_cancel(orders, idx)
            else:
                print(f"Invalid Selection. Please enter a number between 1 and {len(orders)}.")
        except ValueError:
            print("Input Error: Please enter a valid integer (number) only.")

    def perform_modify(self, orders, o_idx):
        sel = orders[o_idx]
        while True:
            print(f"\n[ MODIFYING ORDER: {sel.order_id} ]")
            item_table = [[i+1, it.name, it.qty, f"Rs {it.price:,.2f}", f"Rs {it.subtotal:,.2f}"] for i, it in enumerate(sel.items)]
            print(tabulate(item_table, headers=['#', 'Item', 'Qty', 'Unit Price', 'Subtotal'], tablefmt='fancy_grid'))
            
            try:
                choice = int(input("\nSelect Item # (0 to Back): ").strip())
                if choice == 0: 
                    break 
                i_idx = choice - 1
                if 0 <= i_idx < len(sel.items):
                    new_qty = int(input(f"Enter New Quantity for {sel.items[i_idx].name}: ").strip())
                    
                    if new_qty > 0:
                        it = sel.items[i_idx]
                        it.qty = new_qty
                        it.subtotal = float(it.price) * float(new_qty) 
                        self.refresh_bill(sel)
                        self._save_models(orders)
                        print(f"Updated: {it.name} total is now Rs {it.subtotal:,.2f}")
                    else:
                        print("Error: Quantity must be 1 or more.")
                else:
                    print("Invalid Item Number.")
            except ValueError:
                print("Input Error: Numbers only please.")

    def perform_cancel(self, orders, o_idx):
        try:
            print("\n" + "─"*30 + "\n DELETE OPTIONS ".center(30, "━") + "\n 1. Delete Entire Order\n 2. Delete Specific Item\n 3. Back\n" + "─"*30)
            
            choice = int(input("Select Action (1, 2,3): ").strip())
            
            if choice == 1:
                confirm = input(f"Delete Order {orders[o_idx].order_id}? (y/n): ").lower()
                if confirm == 'y':
                    removed = orders.pop(o_idx)
                    self._save_models(orders)
                    print(f"Success: Order {removed.order_id} deleted.")

            elif choice == 2:
                sel = orders[o_idx]
                item_list = [[i+1, it.name, it.qty] for i, it in enumerate(sel.items)]
                print(tabulate(item_list, headers=['#', 'Item', 'Qty'], tablefmt='fancy_grid'))
                
                item_choice = int(input("\nEnter Item # to remove (0 to Cancel): ").strip())
                if item_choice == 0: 
                    return
                
                i_idx = item_choice - 1
                if 0 <= i_idx < len(sel.items):
                    sel.items.pop(i_idx)
                    if not sel.items: orders.pop(o_idx)
                    else: self.refresh_bill(sel)
                    self._save_models(orders)
                    print("Item removed.")
            elif choice == 3: 
                return
        except ValueError:
            print(" Input Error: Please enter a number.")

    def run_admin_menu(self):

        while True:
            All_Menu.Order_management()
            
            try:
                choice = int(input("Enter Action (1-4): ").strip())
                if choice == 1:
                    orders = self._map_to_models()
                    summary = [[o.order_id, o.customer_name, f"Rs {o.grand_total:,.2f}"] for o in orders]
                    print(tabulate(summary, headers=['Order ID', 'Customer', 'Grand Total'], tablefmt='fancy_grid'))
                elif choice == 2: 
                    self.manage_orders_flow("Modify")
                elif choice == 3: 
                    self.manage_orders_flow("Cancel")
                elif choice == 4:
                    break
                else: print("Error: Please choose a number between 1 and 4.")
            except ValueError:
                print("Input Error: Text is not allowed. Please enter a number.")