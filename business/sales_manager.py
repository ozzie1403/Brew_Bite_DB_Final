from datetime import datetime
from database.models import Sale, SaleItem, Inventory


class SalesManager:

    def __init__(self, db_handler):
        self.db = db_handler
        print("Sales Manager is ready")

    def create_sale(self, user_id, items):
        if not items:
            print("No items provided for the sale.")
            return None

        total_amount = 0
        sale = Sale(
            user_id=user_id,
            date=datetime.now().date(),
            total_amount=0
        )

        try:
            self.db.session.add(sale)
            self.db.session.flush()
        except Exception as e:
            print(f"Error while creating the sale: {e}")
            self.db.session.rollback()
            return None

        for item_id, quantity in items:
            item = self.db.session.query(Inventory).filter_by(item_id=item_id).first()

            if item:
                if item.quantity >= quantity:
                    total_amount += item.cost * quantity
                    sale_item = SaleItem(
                        sale_id=sale.sale_id,
                        item_id=item_id,
                        quantity=quantity
                    )
                    item.quantity -= quantity

                    self.db.session.add(sale_item)
                    print(f"Added {quantity} of {item.item_name} to the sale.")
                else:
                    print(f"Not enough stock for {item.item_name}. Only {item.quantity} available.")
            else:
                print(f"Item with ID {item_id} not found in inventory.")

        sale.total_amount = total_amount

        try:
            self.db.session.commit()
            print(f"Sale completed successfully! Total amount: GBP{total_amount:.2f}")
            return sale
        except Exception as e:
            print(f"Error while completing the sale: {e}")
            self.db.session.rollback()
            return None
