import re
class AdminValidator:
    @staticmethod
    def get_validated_input(prompt, options=None):
        while True:
            value = input(prompt).strip()
            if not value:
                print("[!] Input cannot be empty.")
                continue
            if not value.isdigit():
                print("[!] Please enter a valid number.")
                continue
            
            choice = int(value)
            if options and choice not in options:
                print(f"[!] Invalid choice. Please select from {options}.")
                continue
                
            return choice

    @staticmethod
    def get_input(prompt, options=None, is_id=False):
       
        while True:
            val = input(prompt).strip()
            if not val:
                print("[!] Input cannot be empty.")
                continue
            
            if not val.isdigit():
                print("[!] Please enter a valid number.")
                continue
            
            choice = int(val)
            
            if options and choice not in options:
                print(f"[!] Invalid selection. Choose from {options}.")
                continue
            
            if is_id and choice <= 0:
                print("[!] ID must be greater than 0.")
                continue
                
            return choice
        
    @staticmethod
    def validate_input(prompt, input_type='str', options=None, min_value=None):
        """
        Standardized validation logic for Admin tasks.
        """
        while True:
            value = input(prompt).strip()
            if not value:
                print("[!] Input cannot be empty.")
                continue
            if input_type == 'choice' and options:
                value_lower = value.lower()
                if value_lower not in options:
                    print(f"[!] Invalid choice. Please choose from {options}")
                    continue
                return value_lower

            if input_type == 'int':
                try:
                    num = int(value)
                    if min_value is not None and num < min_value:
                        print(f"Value should be at least {min_value}.")
                        continue
                    return num
                except ValueError:
                    print("Invalid input. Please enter a whole number.")
                    continue

            return value
        
    @staticmethod
    def validate_staff_input(prompt, input_type='str', options=None):
        while True:
            value = input(prompt).strip()
            if not value:
                print("[!] Field cannot be empty.")
                continue

            if input_type == 'choice' and options:
                if value not in options:
                    print(f"[!] Choose from {options}")
                    continue
                return value

            if input_type == 'phone':
                if not re.fullmatch(r'\d{10}', value):
                    print("[!] Phone must be exactly 10 digits.")
                    continue
                return value
                
            return value