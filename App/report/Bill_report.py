
from datetime import datetime, timedelta
from tabulate import tabulate
from App.File_Handler.File_manager import JSONHandler
from App.model.database_model import DBFiles

class BillReportManager:
    FILENAME = DBFiles.BILLING

    @staticmethod
    def filter_bills(days):
        """Flexible filter to handle different date formats."""
        all_bills = JSONHandler.load_data(BillReportManager.FILENAME)
        
        if not all_bills:
            print(f"[!] Warning: No data found in {BillReportManager.FILENAME}")
            return []

        threshold = datetime.now() - timedelta(days=days)
        filtered = []
        
        for b in all_bills:
            date_str = b.get("date") or b.get("timestamp")
            if not date_str:
                continue
                
            try:
                clean_date = date_str.split(" ")[0]
                bill_date = None
                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
                    try:
                        bill_date = datetime.strptime(clean_date, fmt)
                        break
                    except ValueError:
                        continue
                
                if bill_date and bill_date >= threshold:
                    filtered.append(b)
            except Exception as e:
                continue
                
        return filtered

    @staticmethod
    def display_report():
        while True:
            try:
                print("\n" + "═"*65)
                print(f"║ {'BILLING SALES REPORT':^61} ║")
                print("═"*65)
                print(" 1. Daily Report (Last 24 Hours)")
                print(" 2. Weekly Report (Last 7 Days)")
                print(" 3. Monthly Report (Last 30 Days)")
                print(" 4. Back")
                print("─"*65)

                user_input = input(" Select Option (1-4): ").strip()

                if not user_input:
                    print("[!] Error: Please enter a choice.")
                    continue

                try:
                    choice = int(user_input)
                except ValueError:
                    print(f"[!] Error: '{user_input}' is not a number.")
                    continue

                if choice == 4:
                    print("[*] Returning...")
                    break

                if choice not in [1, 2, 3]:
                    print("[!] Invalid Range! Select 1-4.")
                    continue

                days_map = {1: 1, 2: 7, 3: 30}
                period_name = {1: 'DAILY', 2: 'WEEKLY', 3: 'MONTHLY'}[choice]
                
                bills = BillReportManager.filter_bills(days_map[choice])

                if not bills:
                    print(f"\n[!] No records found for the {period_name} period.")
                    print(f"    Check if data exists in your database folder.")
                    input("\nPress Enter to continue...")
                    continue

                table_data = []
                total_revenue = 0
                method_summary = {}

                for b in bills:
            
                    amount = float(b.get("final_amount") or b.get("total_amount") or 0)
                    method = b.get("payment_method") or b.get("method") or "Cash"
                    
                    total_revenue += amount
                    method_summary[method] = method_summary.get(method, 0) + amount
                    
                    table_data.append([
                        b.get("bill_id", "N/A"),
                        b.get("customer") or b.get("customer_name", "Guest"),
                        b.get("date", "N/A"),
                        method,
                        f"Rs. {amount:,.2f}"
                    ])

                headers = ["Bill ID", "Customer", "Date", "Payment", "Amount"]
                
                print(f"\n{period_name} SALES SUMMARY".center(75, "─"))
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
                summary_table = [[m, f"Rs. {amt:,.2f}"] for m, amt in method_summary.items()]
                print("\n" + " PAYMENT METHODS ".center(30, "-"))
                print(tabulate(summary_table, headers=["Method", "Total"], tablefmt="simple"))
                
                print("═"*75)
                print(f" TOTAL BILLS: {len(bills)} | GRAND TOTAL: Rs. {total_revenue:,.2f} ".center(75, "█"))
                print("═"*75)
                
                input("\nPress Enter to return to menu...")

            except Exception as e:
                print(f"[!] System Error: {e}")
                break

