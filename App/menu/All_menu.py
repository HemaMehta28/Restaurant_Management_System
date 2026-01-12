class All_Menu:
    def __init__(self):
        pass

    @staticmethod
    def display_dashboard():
        print("========================================================================")
        print("| *************** Staff Dashboard **************** |")
        print("========================================================================")
        print("| \t\t1. Take Order |")
        print("| \t\t2. Book Table |")
        print("| \t\t3. Exit |")
        print("========================================================================")

    @staticmethod
    def display_menu():
        print("\n" + "="*60)
        print("| *********** RESTAURANT MANAGEMENT SYSTEM ************ |")
        print("="*60)
        print("| \t\t1. Login |")
        print("| \t\t2. SignUp |")
        print("| \t\t3. Exit |")
        print("="*60)

    @staticmethod
    def Order_menu():
        print("========================================================================")
        print("| *************** Order Menu **************** |")
        print("========================================================================")
        print("| \t\t1. Show food menu |")
        print("| \t\t2. Add Order |")
        print("| \t\t3. Show all orders |")
        print("| \t\t4. Generate bill |")
        print("| \t\t5. Back to main menu |")
        print("========================================================================")
 
    @staticmethod
    def Add_menu():
        print("========================================================================")
        print("| *************** Add Order **************** |")
        print("========================================================================")
        print("| \t\t1. Add food to order |")
        print("| \t\t2. View order |")
        print("| \t\t3. Confirm Order|")
        print("| \t\t4. Exit to menu |")
        print("========================================================================")

    def Table_book_menu():
        print("========================================================================")
        print("| *************** RESTAURANT TABLE MANAGEMENT SYSTEM **************** |")
        print("========================================================================")
        print("| \t\t1. New Seat Booking |")
        print("| \t\t2. View Table Status |")
        print("| \t\t3. View All Bookings |")
        print("| \t\t4. Back to main menu |")
        print("========================================================================")

    @staticmethod
    def MenuManagement_menu():
        print("========================================================================")
        print("| *************** MENU MANAGEMENT **************** |")
        print("========================================================================")
        print("| \t\t1. View Menu |")
        print("| \t\t2. Add New Item |")
        print("| \t\t3. Update  |")
        print("| \t\t4. Delete Item |")
        print("| \t\t5. Back |")
        print("========================================================================")

    @staticmethod
    def Admindashboard_menu():
        print("========================================================================")
        print("| *************** ADMIN DASHBOARD **************** |")
        print("========================================================================")
        print("| \t\t1. Menu Management |")
        print("| \t\t2. Order Management |")
        print("| \t\t3. Staff Management |")
        print("| \t\t4. Inventory Management |")
        print("| \t\t5. Report Analysis |")
        print("| \t\t6. Back to Main Menu |")
        print("========================================================================")

    @staticmethod
    def Order_management():
        print("========================================================================")
        print("| *************** ORDER MANAGEMENT SYSTEM **************** |")
        print("========================================================================")
        print(" 1. View All Orders\n 2. Modify Order(Update Qty)\n 3. Cancel Order / Delete Item\n 4. Logout\n" )
        print("========================================================================")
    
    @staticmethod
    def Report_menu():
            print("\n" + "═"*50)
            print("\tREPORTS MANAGEMENT")
            print("═"*50)
            print("1. Food Sales Report")
            print("2. Table Booking Report")
            print("3. Bill Report")
            print("4. Back")
            print("═"*50)
    @staticmethod
    def ManageStaff():
            print("\n" + "═"*50)
            print("\t STAFF MANAGEMENT ")
            print( "═"*50)
            print(" 1. View All Staff Members")
            print(" 2. Remove Staff Member")
            print(" 3. Return to Main Menu")
            print("\n" + "═"*50)
    @staticmethod
    def ManageInventry():
            print("\n" + "═"*60)
            print("\tINVENTORY MANAGEMENT SYSTEM".center(40))
            print("═"*60)
            print(" 1. View Report")
            print(" 2. Restock Item")
            print(" 3. Exit")
            print("─"*60)