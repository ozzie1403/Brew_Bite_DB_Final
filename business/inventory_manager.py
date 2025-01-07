from database.models import Inventory

class InventoryManager:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def add_item(self, item_name, quantity, cost):
        new_item = Inventory(
            item_name=item_name,
            quantity=quantity,
            cost=cost
        )
        self.db.session.add(new_item)
        self.db.session.commit()
        return new_item
    
    def update_quantity(self, item_id, new_quantity):
        item = self.db.session.query(Inventory).filter_by(item_id=item_id).first()
        if item:
            item.quantity = new_quantity
            self.db.session.commit()
            return True
        return False
    
    def get_all_items(self):
        return self.db.session.query(Inventory).all()