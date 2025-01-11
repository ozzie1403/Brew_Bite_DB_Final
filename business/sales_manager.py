from datetime import datetime
from database.models import sale, sale_item, inventory

class salesmanager:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_sale(self, user_id: int, items, sale):
        total_amount = 0
        sale = sale(
            user_id=user_id,
            date=datetime.now().date(),
            total_amount=0
            )
        self.db.session.add(sale)
        self.db.session.flush()
        
        for item_id, quantity in items:
            item = self.db.session.query(inventory).filter_by(item_id=item_id).first()
            if item and item.quantity >= quantity:
                total_amount += item.cost * quantity
                sale_item = sale_item(
                    sale_id=sale.sale_id,
                    item_id=item_id,
                    quantity=quantity
                    )
                item.quantity -= quantity
                self.db.session.add(sale_item)
        
        sale.total_amount = total_amount
        self.db.session.commit()
        return sale