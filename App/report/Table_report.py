import os
import sys
from datetime import datetime, timedelta
from tabulate import tabulate
from collections import defaultdict
from App.File_Handler.File_manager import JSONHandler
from App.model.database_model import DBFiles
class BookingReportManager:
    """
    Manages and displays table booking reports using the central JSONHandler.
    """
    FILENAME = DBFiles.BOOKINGS

    @staticmethod
    def filter_bookings(days):
        """Filter bookings based on the number of days from today."""
        bookings = JSONHandler.load_data(BookingReportManager.FILENAME)
        threshold = datetime.now() - timedelta(days=days)
        filtered = []
        for b in bookings:
            try:
                b_time = datetime.strptime(b.get("timestamp"), "%Y-%m-%d %H:%M:%S")
                if b_time >= threshold:
                    filtered.append(b)
            except:
                continue
        return filtered

    @staticmethod
    def merge_bookings(bookings):
        """Merge multiple tables into one entry based on customer and time slot."""
        merged = defaultdict(lambda: {
            "booking_id": "", "tables": [], "booked_seats": 0, "total_fee": 0,
            "customer_name": "", "customer_phone": "", "slot": "", "date": "", "booked_at": ""
        })

        for b in bookings:
            key = (b.get("customer_name"), b.get("slot"), b.get("date"))
            b_id = b.get("booking_id", "N/A")
            b_seats = b.get("booked_seats", 0)
            b_fee = b.get("booking_fee", 0)
            
            if not merged[key]["booking_id"]:
                merged[key]["booking_id"] = b_id
            
            merged[key]["tables"].append(b.get("table_number"))
            merged[key]["booked_seats"] += int(b_seats)
            merged[key]["total_fee"] += float(b_fee)
            merged[key]["customer_name"] = b.get("customer_name")
            merged[key]["customer_phone"] = b.get("customer_phone")
            merged[key]["slot"] = b.get("slot")
            merged[key]["date"] = b.get("date")
            merged[key]["booked_at"] = b.get("timestamp") 

        return list(merged.values())

    @staticmethod
    def display_report():
        while True:
            print("\n" + "═"*70)
            print(f"**********************BOOKING REPORT MENU***********************")
            print("═"*70)
            print("  1. Daily Bookings (Last 24h)")
            print("  2. Weekly Bookings (Last 7 Days)")
            print("  3. Monthly Bookings (Last 30 Days)")
            print("  4. Back")
            print("═"*70)

            user_input = input("Select Option (1-4): ").strip()
            if not user_input:
                print("Input cannot be empty.")
                continue

            try:
                choice = int(user_input)
                if choice == 4:
                    break 
                
                if choice not in [1, 2, 3]:
                    print(f"[!] {choice} is not valid. Select 1-4.")
                    continue

                days_map = {1: 1, 2: 7, 3: 30}
                period_name = {1: 'Daily', 2: 'Weekly', 3: 'Monthly'}[choice]
                
                bookings = BookingReportManager.filter_bookings(days_map[choice])
                merged = BookingReportManager.merge_bookings(bookings)

                if not merged:
                    print(f"\n[!] No bookings found for {period_name} period.")
                    continue

                table_data = []
                total_seats = 0
                total_cash = 0

                for b in merged:
                    total_seats += b["booked_seats"]
                    total_cash += b["total_fee"]
                    booked_at = b.get("booked_at", "N/A")[:16] 
                    table_list = ", ".join(map(str, b["tables"]))
                    
                    table_data.append([
                        b["booking_id"], 
                        b["customer_name"], 
                        b["customer_phone"],
                        f"{b['date']}\n({b['slot']})", 
                        table_list,                   
                        b["booked_seats"], 
                        f"₹ {b['total_fee']:,.2f}", 
                        booked_at
                    ])

                headers = ["ID", "Customer", "Phone", "Slot Details", "Tables", "Seats", "Fee", "Booked On"]
                
                print(f"\n{period_name.upper()} BOOKINGS REPORT".center(100))
                
                print(tabulate(
                    table_data, 
                    headers=headers, 
                    tablefmt="fancy_grid",
                    maxcolwidths=[None, 15, None, None, 15, None, None, None],
                    colalign=("center", "left", "center", "center", "center", "center", "right", "left")
                ))

                print("━" * 100)
                summary = f" GRAND TOTAL | Total Seats: {total_seats} | Revenue: ₹ {total_cash:,.2f} "
                print(summary.center(100, "="))
                print("━" * 100)
                
                input("\nPress Enter to return to Menu...")

            except ValueError:
                print(f"Error: '{user_input}' is not a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")