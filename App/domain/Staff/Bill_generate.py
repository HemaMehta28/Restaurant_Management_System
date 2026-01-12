import os
import json
from tabulate import tabulate
from datetime import datetime
from App.domain.Staff.file_handler import FileHandler

class BillGenerator:
    def __init__(self):
        self.handler = FileHandler()
        self.config = self.handler.get_config()
        self.order_db = self.config.order_file
        self.history_db = self.config.history_file
        self.order_record_db = self.config.order_record_file
    

    def get_int_input(self, prompt):
        """Safely get integer input from user."""
        while True:
            val = input(prompt).strip()
            if val.isdigit():
                return int(val)
            print("[!] INVALID INPUT")

    def generate_bill(self):
        try:
            orders = self.handler.read_json(self.order_db) or []
            if not orders:
                print("\n[!] No active orders found.")
                return
            print("\n" + "═"*55)
            print("PENDING BILLS".center(55))
            print("═"*55)
            summary = []
            for i, o in enumerate(orders, 1):
                summary.append([
                    i,
                    o.get("order_id"),
                    o.get("customer_name", "Guest"),
                    f"Rs {o.get('grand_total', 0)}"
                ])
            print(tabulate(summary, headers=["No", "Order ID", "Customer", "Amount"], tablefmt="grid"))

            choice = self.get_int_input("\nSelect Order (0 to Back): ")
            if choice == 0:
                return

            idx = choice - 1
            if idx < 0 or idx >= len(orders):
                print("[!] Invalid selection")
                return

            order = orders[idx]
            food_total = order.get("food_total", 0)
            booking_fee = order.get("booking_fee", 0)
            cust_name = order.get("customer_name", "Guest")
            discount_per = self.get_int_input("Enter Discount %: ")
            discount_amt = (food_total * discount_per) / 100
            taxable = food_total - discount_amt
            gst = taxable * 0.05
            grand_total = taxable + gst + booking_fee
            print("\n" + "="*50)
            print("RESTAURANT TAX INVOICE".center(50))
            print("="*50)
            print(f"Order ID : {order.get('order_id')}")
            print(f"Customer : {cust_name}")
            print(f"Date     : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            print("-"*50)

            items = []
            for i in order.get("items", []):
                items.append([i.get("name"), i.get("qty"), i.get("price"), i.get("subtotal")])
            print(tabulate(items, headers=["Item", "Qty", "Rate", "Total"], tablefmt="plain"))

            print("-"*50)
            print(f"Food Total     : Rs {food_total:.2f}")
            print(f"Discount       : -Rs {discount_amt:.2f}")
            print(f"GST (5%)       : Rs {gst:.2f}")
            print(f"Booking Fee    : Rs {booking_fee:.2f}")
            print("─"*50)
            print(f"GRAND TOTAL    : Rs {grand_total:.2f}")
            print("="*50)

            method = None
            while True:
                print("\nPayment Method:")
                print("1. Cash | 2. Card | 3. UPI")
                pay = self.get_int_input("Choice (1-3): ")
                
                if pay == 1:
                    method = "CASH"
                    break
                elif pay == 2:
                    method = "CARD"
                    break
                elif pay == 3:
                    method = "UPI"
                    break
                else:
                    print("[!] Invalid Choice! Please select 1, 2, or 3.")

            confirm = self.get_int_input(f"\nConfirm Payment via {method}? (1.Yes / 2.No): ")
            if confirm != 1:
                print("Billing Cancelled")
                return



            history = self.handler.read_json(self.history_db) or []
            history.append({
                "bill_id": f"BILL-{datetime.now().strftime('%H%M%S')}",
                "order_id": order.get("order_id"),
                "customer": cust_name,
                "payment_method": method,
                "final_amount": grand_total,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "PAID"
            })
            self.handler.write_json(self.history_db, history)

            order_record = self.handler.read_json(self.order_record_db) or []
            full_order_record = order.copy() 
            full_order_record["payment_method"] = method
            full_order_record["grand_total_after_discount"] = grand_total
            full_order_record["discount_percent"] = discount_per
            full_order_record["discount_amount"] = discount_amt
            full_order_record["gst"] = gst
            full_order_record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_record.append(full_order_record)
            self.handler.write_json(self.order_record_db, order_record)

            orders.pop(idx)
            self.handler.write_json(self.order_db, orders)

            print(f"\n[✔] Payment Successful via {method}")
            print(f"[✔] Order {order.get('order_id')} recorded in order record.\n")

        except Exception as e:
          
            print(f"[!] Exception during billing: {type(e).__name__} - {e}")
