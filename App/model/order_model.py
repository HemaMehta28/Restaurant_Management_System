class FoodMenuModel:
    id = None
    name = None
    category = None
    sub_type = None
    half_price = None
    full_price = None
    price = None
    stock = None


class OrderItemModel:
    def __init__(self):
        self.name = None
        self.qty = 0
        self.price = 0.0
        self.subtotal = 0.0

class OrderModel:
    def __init__(self):
        self.order_id = None
        self.customer_name = None
        self.booking_fee = 0.0
        self.food_total = 0.0
        self.grand_total = 0.0
        self.items = [] 

class DraftItemModel:
    food_id = None
    item_name = None
    size_label = None
    item_type = None
    quantity = None
    unit_rate = None
    subtotal = None
    stock_reduced = None


class RestaurantConfigModel:
    def __init__(self):
        self.base_dir = ""
        self.db_folder = ""
        self.menu_file = ""
        self.order_file = ""
        self.history_file = ""  





class OrderConfig:
    DEFAULT_GUEST = "Walk-in Guest"
    DEFAULT_TABLE = "N/A"
    TYPE_HALF = "HALF"
    TYPE_FULL = "FULL"
    KEY_VEG = "veg"
    KEY_NONVEG = "nonveg"
    KEY_STOCK = "stock"
    KEY_NAME = "name"
    KEY_ID = "id"
    KEY_HALF = "half"
    KEY_FULL = "full"
    STATUS_COMPLETED = "Completed"

class InventoryModel:
    def __init__(self, item_id, name, stock):
        self.id = str(item_id)
        self.name = name
        self.current_stock = float(stock) 
        self.status_tag = self._generate_status() 

    def _generate_status(self):
        """Status tag logic"""
        if self.current_stock > 10: 
            return "[Full]"
        if self.current_stock > 5: 
            return "<OK>"
        if self.current_stock > 0: 
            return "|LOW|"
        return " OUT"

    def to_dict_update(self):
        return {"id": self.id, "name": self.name, "stock": self.current_stock}