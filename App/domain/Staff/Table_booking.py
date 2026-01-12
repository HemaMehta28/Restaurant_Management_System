import os
import uuid
from datetime import datetime, timedelta
from App.model.table_model import TableManager
from App.validation.Staff_validation import InputValidator
from App.menu.All_menu import All_Menu
class TableBookingUI:
    def __init__(self):
        self.manager = TableManager()
        self.validator = InputValidator()
        self.FEE_PER_SEAT = 50 
    def generate_booking_id(self):
        return f"{str(uuid.uuid4())[:3].upper()}"
    def get_input(self, prompt, is_digit=True, min_val=None, max_val=None, length=None, no_leading_zero=False):
        while True:
            u_input = input(prompt).strip()
            if u_input == '0': return 0
            if not u_input:
                print("Input cannot be empty.")
                continue
            if is_digit: 
                is_valid, result = self.validator.validate_integer(
                    u_input, min_val=min_val, max_val=max_val, 
                    length=length, no_leading_zero=no_leading_zero
                )
            else:
                is_valid, result = self.validator.validate_string(u_input)
            
            if is_valid: return result
            else: print(f"[!] {result}") 

    def select_date_and_slot(self, title):
        """Prompts user to select an available date and time slot."""
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        
        print("\n" + "═"*45 + f"\n   {title}: SELECT DATE\n" + "═"*45)
        date_list = [now + timedelta(days=i) for i in range(7)]
        for i, d in enumerate(date_list, 1):
            print(f"{i}. {d.strftime('%A')} ({d.strftime('%Y-%m-%d')})")
        
        d_idx = self.get_input("\nSelect Date Index (or 0 to back): ", min_val=1, max_val=len(date_list))
        if d_idx == 0: return None, None
        sel_date = date_list[d_idx - 1].strftime("%Y-%m-%d")

      
        all_db_slots = self.manager.get_all_json_slots()
        filtered_slots = []
        for slot in all_db_slots:
            if sel_date == today_str:
                start_time_str = slot.split(" - ")[0]
                slot_time = datetime.strptime(start_time_str, "%I:%M %p").time()
                if slot_time > now.time():
                    filtered_slots.append(slot)
            else:
                filtered_slots.append(slot)

        if not filtered_slots:
            print(f"\n No upcoming slots available for {sel_date}."); return None, None

        print("\n" + "═"*45 + f"\n   {title}: SELECT TIME SLOT\n" + "═"*45)
        for i, s in enumerate(filtered_slots, 1): print(f"{i}. {s}")
        
        s_idx = self.get_input("\nSelect Slot Index (or 0 to back): ", min_val=1, max_val=len(filtered_slots))
        if s_idx == 0: return None, None
        sel_slot = filtered_slots[s_idx - 1]
        
        return sel_date, sel_slot

    def run(self):
        while True:
            All_Menu.Table_book_menu()
            choice = self.get_input("\nSelect Option (1-4): ", min_val=1, max_val=4)
            if choice == 1: 
                self.booking_flow()
            elif choice == 2: 
                self.show_status()
            elif choice == 3: 
                self.view_history()
            elif choice == 4 or choice == 0: 
                print("[*] Returning to Staff Dashboard...")
                break

    def booking_flow(self):
        """Executes the step-by-step table booking process."""
        sel_date, sel_slot = self.select_date_and_slot("NEW BOOKING")
        if not sel_date: return

        booking_id = self.generate_booking_id()
        current_session_bookings = []

        print("\n" + "─"*45 + "\nCUSTOMER DETAILS\n" + "─"*45)
        name = self.get_input("Customer Name: ", is_digit=False)
        if name == 0: return
        phone = self.get_input("Phone Number: ", length=10, no_leading_zero=True)
        if phone == 0: return

        while True:
            print(f"\n" + "═"*55 + f"\n DATE: {sel_date} | SLOT: {sel_slot}\n" + "═"*55)
            available_tables = []
            for t in self.manager.tables:
                if sel_slot in t.get('slots', []):
                    rem = self.manager.get_remaining_seats(t['table_number'], sel_date, sel_slot)
                    print(f"T-{t['table_number']:<10} Cap: {t['capacity']:<10} Available: {rem:<10}")
                    if rem > 0: available_tables.append(int(t['table_number']))
            
            if not available_tables:
                print("\n[!] All tables are full for this slot."); break

            t_no = self.get_input("\nSelect Table No (or 0 to Finish): ")
            if t_no == 0: break
            
            if t_no in available_tables:
                rem_seats = self.manager.get_remaining_seats(t_no, sel_date, sel_slot)
                seats = self.get_input(f"Seats on T-{t_no} (Max {rem_seats}): ", min_val=1, max_val=rem_seats)
                if seats == 0: break

                self.manager.add_booking(t_no, sel_date, sel_slot, name, str(phone), seats, booking_id)
                current_session_bookings.append({'table': t_no, 'seats': seats, 'fee': seats * self.FEE_PER_SEAT})
                print(f" T-{t_no} added to booking list.")

                print("\n1. Add another table | 2. Confirm & Finish")
                if self.get_input("Choice: ", min_val=1, max_val=2) != 1: break
            else: print("[!] This table is not available.")

        if current_session_bookings:
            self.print_receipt(booking_id, sel_date, sel_slot, name, phone, current_session_bookings)

    def show_status(self):
        """Displays real-time table occupancy for a selected slot."""
        sel_date, sel_slot = self.select_date_and_slot("LIVE STATUS MAP")
        if not sel_date: return

        print(f"\n" + "*"*65 + f"\n LIVE TABLE MAP: {sel_date} | {sel_slot}\n" + "*"*65)
        print(f"{'Table No':<12} {'Total Cap':<12} {'Occupied':<12} {'Available':<12}")
        print("─"*65)
        
        for t in self.manager.tables:
            if sel_slot in t.get('slots', []):
                t_no = t['table_number']
                total = int(t['capacity'])
                free = self.manager.get_remaining_seats(t_no, sel_date, sel_slot)
                occ = total - free
                
                status_text = "[FULL]" if free == 0 else "[FREE]"
                print(f"T-{t_no:<10} {total:<12} {occ:<12} {free:<12} {status_text}")
        
        print("─"*65)
        input("\nPress Enter to return to Dashboard...")

    def print_receipt(self, bid, date, slot, name, phone, bookings):
        print("\n" + "═"*42 + "\n\tBOOKING SUCCESSFUL\n" + "─"*42)
        print(f"| Booking ID: {bid}\n| Customer  : {name}\n| Date      : {date}\n| Slot      : {slot}")
        print("─"*42)
        total_amt = sum(b['fee'] for b in bookings)
        for b in bookings:
            print(f"| Table T-{b['table']:<5} : {b['seats']} Seats | Rs.{b['fee']}")
        print("─"*42 + f"\n| TOTAL PAYABLE: Rs.{total_amt}\n" + "═"*42)
        input("\nPress Enter to continue...")

    def view_history(self):
        """Retrieves and displays all past booking records."""
        self.manager.booking_data = self.manager.handler.read_json(self.manager.booking_file)
        if not self.manager.booking_data:
            print("\n[!] No booking history found."); return

        grouped = {}
        for b in self.manager.booking_data:
            bid = b.get('booking_id', 'N/A')
            if bid not in grouped: grouped[bid] = []
            grouped[bid].append(b)

        print("\n" + "═"*65 + f"\n{'RESTAURANT BOOKING HISTORY':^65}\n" + "═"*65)
        for bid, items in grouped.items():
            f = items[0]
            print(f"\nID: {bid} | Customer: {f.get('customer_name')}\nDate: {f.get('date')} | Slot: {f.get('slot')}")
            print("┌──────────┬──────────┬──────────┐\n│ Table    │ Seats    │ Fee      │\n├──────────┼──────────┼──────────┤")
            order_total = 0
            for i in items:
                fee = i.get('booking_fee', 0)
                print(f"│ T-{i.get('table_number'):<6} │ {i.get('booked_seats'):<8} │ Rs.{fee:<5} │")
                order_total += fee
            print("└──────────┴──────────┴──────────┘\n" + f"Total: Rs.{order_total}")
        input("\nPress Enter to back...")