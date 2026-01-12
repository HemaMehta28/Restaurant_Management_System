class InputValidator:
    @staticmethod
    def validate_integer(u_input, min_val=None, max_val=None, length=None, no_leading_zero=False):
        if not u_input.isdigit():
            return False, " Invalid input. Please enter numbers only."
        if no_leading_zero and u_input[0] == '0':
            return False, "Invalid. Number cannot start with 0."
   
        if length and len(u_input) != length:
            return False, f"Invalid. Must be exactly {length} digits."

        val = int(u_input)
        
     
        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            return False, f"Out of range. Enter a value between {min_val} and {max_val}."
        
        return True, val

    @staticmethod
    def validate_string(u_input):
        if u_input and u_input.replace(" ", "").isalpha():
            return True, u_input
        return False, "Invalid Name. Use letters only (no symbols or numbers)."
  
    @staticmethod
    def get_choice(prompt):
        """Sirf integer input lega, agar string daali toh error dega."""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input! Please enter a number (1, 2, 3, etc.).")