import os
import sys
from datetime import datetime, timedelta
from tabulate import tabulate
from App.File_Handler.File_manager import JSONHandler
from App.model.database_model import DBFiles
class ReportManager:
    """
    Manages and displays food sales reports using the central JSONHandler.
    """
    FILENAME = DBFiles.ORDERS
    def show_report(self):

        self.display_sales_report()
    @staticmethod
    def filter_orders(period_days):
        """Filters orders based on the number of days from today."""
        orders = JSONHandler.load_data(ReportManager.FILENAME) 
        now = datetime.now()
        threshold = now - timedelta(days=period_days)
        filtered = []
        for order in orders:
            ts_str = order.get("timestamp") or order.get("date")
            if not ts_str:
                continue
            
            try:
                order_time = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                if order_time >= threshold:
                    filtered.append(order)
            except ValueError:
                try:
                    order_time = datetime.strptime(ts_str, "%Y-%m-%d")
                    if order_time >= threshold:
                        filtered.append(order)
                except:
                    continue
        return filtered

    @staticmethod
    def calculate_summary(orders):
      
        total_rev = sum(float(o.get("grand_total_after_discount", 0)) for o in orders)
        return len(orders), total_rev

    @staticmethod
    def display_sales_report():
        """Main UI loop for the Sales Report with improved table structure."""
        while True:
            print("\n" + "═"*70)
            print("\t FOOD SALES ANALYTICS")
            print("═"*70)
            print("  1. Daily Sales (Last 24 Hours)")
            print("  2. Weekly Sales (Last 7 Days)")
            print("  3. Monthly Sales (Last 30 Days)")
            print("  4. Back to Reports Menu")
            print("─"*70)
            
            choice = input("\nSelect Option (1-4): ").strip()
            if choice == '4':
                break
            if choice not in ['1', '2', '3']:
                print("Invalid selection.")
                continue

            days = {'1': 1, '2': 7, '3': 30}[choice]
            period_label = {'1': 'DAILY', '2': 'WEEKLY', '3': 'MONTHLY'}[choice]
            
            orders = ReportManager.filter_orders(days)

            if not orders:
                print(f"\n[!] No records found for {period_label} period.")
                input("\nPress Enter to continue...")
                continue

            table_data = []
            for o in orders:
                oid = o.get("order_id", "N/A")
                ts = o.get("timestamp") or o.get("date", "N/A")
                if len(ts) > 16: ts = ts[:16] 
                
                rev = float(o.get("grand_total_after_discount", 0))
                items_list = o.get("items", [])
                items_str = "\n".join([f"• {i['name']} (x{i['qty']})" for i in items_list])
                
                table_data.append([oid, ts, items_str, f"₹ {rev:,.2f}"])

            print(f"\n[ {period_label} SALES SUMMARY ]")
            print(tabulate(
                table_data, 
                headers=["ID", "Date/Time", "Items Purchased", "Amount"], 
                tablefmt="fancy_grid", 
                maxcolwidths=[None, None, 35, None], 
                colalign=("center", "left", "left", "right") 
            ))
            
            count, revenue = ReportManager.calculate_summary(orders)
            
            print("\n" + "━"*70)
            summary_text = f" TOTAL ORDERS: {count} | TOTAL REVENUE: ₹ {revenue:,.2f} "
            print(summary_text.center(70, "▒"))
            print("━"*70)
            input("\nPress Enter to return to menu...")