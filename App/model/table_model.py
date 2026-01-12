import os
from datetime import datetime
from App.domain.Staff.file_handler import FileHandler

class TableManager:
    def __init__(self):
        self.handler = FileHandler()
        self.config = self.handler.get_config()
        self.table_data_file = os.path.join(self.config.db_folder, 'table_data.json')
        self.booking_file = os.path.join(self.config.db_folder, 'table_book.json')
        self.tables = self.handler.read_json(self.table_data_file)
        self.booking_data = self.handler.read_json(self.booking_file)

    def get_all_json_slots(self):
        slots = set()
        for t in self.tables:
            for s in t.get('slots', []):
                slots.add(s)
        return sorted(list(slots))

    def get_remaining_seats(self, table_no, date, slot):
        table = next((t for t in self.tables if int(t['table_number']) == int(table_no)), None)
        if not table: return 0
        
        total_capacity = int(table['capacity'])
        occupied = 0
        for b in self.booking_data:
            if (int(b.get('table_number', 0)) == int(table_no) and 
                b.get('date') == date and 
                b.get('slot') == slot):
                occupied += int(b.get('booked_seats', b.get('seats', 0)))
        
        return total_capacity - occupied

    def add_booking(self, table_no, date, slot, name, phone, seats, booking_id):
        fee = int(seats) * 50
        
        new_booking = {
            "booking_id": booking_id,
            "table_number": table_no,
            "date": date,
            "slot": slot,
            "customer_name": name,
            "customer_phone": phone,
            "booked_seats": seats,
            "booking_fee": fee,  
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.booking_data.append(new_booking)
        self.save_bookings()

    def save_bookings(self):
        self.handler.write_json(self.booking_file, self.booking_data)