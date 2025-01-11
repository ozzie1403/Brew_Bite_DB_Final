from database.models import inventory #importing inventory class

class inventorymanager:
    def __init__(self, db_session):
        self.db = db_session
    
    def add_item(self, item_name: str, quantity: int, cost: float):
        new_item = inventory(
            item_name=item_name,
            quantity=quantity,
            cost=cost
            )
        self.db.session.add(new_item)
        self.db.session.commit()
        return new_item
    
    def quantity_update(self, item_id: int, new_quantity: float):
        item = self.db.session.query(inventory).filter_by(item_id=item_id).first()
        if item:
            item.quantity = new_quantity
            self.db.session.commit()
            return True
        return False
    
    def get_all_items(self):
        return self.db.session.query(inventory).all()