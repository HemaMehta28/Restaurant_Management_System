import pwinput
from .Auth_Filehandler import FileHandler, AuthLogger
from App.model.Auth_model import UserRoles
from ..domain.Admin.Admin_Dashboard import AdminDashboard
from ..domain.Staff.Staff_Dashboard import StaffDashboard

class Staff_login:
    def __init__(self, config_instance):
        self.config = config_instance
        self.db = FileHandler(config=config_instance)

    def login(self):
        users = self.db.read_all()
        print(f"\n{'='*20} Login Screen {'='*20}")
        
        user_data = None
        while True:
            email = input("Enter Email: ").strip().lower()
            user_data = next((u for u in users if u['email'].lower() == email), None)
            
            if user_data:
                break
            else:
                AuthLogger.write_log( "N/A", email,"AuthError", "login","Email not found",self.config  )

                print("[✘] Email not found! Please try again.")

        while True:
            pw = pwinput.pwinput("Enter Password: ")
            if user_data['password'] == pw:
                print(f"\n[✔] Login Successful!")
                print(f"Welcome {user_data['role']}: {user_data['name']}")
                
                u_id = user_data.get('id') or user_data.get('staff_id') or "N/A"

                AuthLogger.write_log(u_id,user_data['email'],  "SUCCESS", "login",f"{user_data['role']} Login",self.config )

                self.redirect_to_dashboard(user_data)
                return user_data
            else:
                u_id = user_data.get('id') or user_data.get('staff_id') or "N/A"

                AuthLogger.write_log( u_id,user_data['email'],"AuthError", "login", "Incorrect password",self.config )
                print("[✘] Incorrect Password. Please try again.")

    def redirect_to_dashboard(self, user_data):
        role = user_data.get('role')
        u_id = user_data.get('id') or user_data.get('staff_id')
        email = user_data.get('email')

        if role == UserRoles.ADMIN:
            dashboard = AdminDashboard(
                admin_id=u_id,
                email=email
            )
            dashboard = AdminDashboard()
            dashboard.run()

            
        elif role == UserRoles.STAFF:
            dashboard = StaffDashboard(
                staff_id=u_id,
                email=email
            )
            dashboard.run()
