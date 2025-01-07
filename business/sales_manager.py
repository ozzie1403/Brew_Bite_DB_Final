from datetime import datetime
from database.models import Sale, SaleItem, Inventory


class SalesManager:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def create_sale(self, user_id, items):
        # items should be a list of tuples: [(item_id, quantity), ...]
        total_amount = 0
        sale = Sale(
            user_id=user_id,
            date=datetime.now().date(),
            total_amount=0
        )
        self.db.session.add(sale)
        self.db.session.flush()
        
        for item_id, quantity in items:
            item = self.db.session.query(Inventory).filter_by(item_id=item_id).first()
            if item and item.quantity >= quantity:
                total_amount += item.cost * quantity
                sale_item = SaleItem(
                    sale_id=sale.sale_id,
                    item_id=item_id,
                    quantity=quantity
                )
                item.quantity -= quantity
                self.db.session.add(sale_item)
        
        sale.total_amount = total_amount
        self.db.session.commit()
        return sale