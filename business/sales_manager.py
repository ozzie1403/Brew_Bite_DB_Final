from datetime import datetime
from database.models import Sale, SaleItem, Inventory


class SalesManager:
    def __init__(self, db_handler):
        # Initialize the SalesManager with the database handler (session).
        self.db = db_handler
        print("Sales Manager is ready to process sales!")

    def create_sale(self, user_id, items):
        """
        Create a new sale transaction for a user.
        The items parameter should be a list of tuples where each tuple contains:
        (item_id, quantity).

        It calculates the total amount of the sale, updates inventory, and stores
        the transaction in the database.
        """
        if not items:
            print("No items provided for the sale.")
            return None

        total_amount = 0
        sale = Sale(
            user_id=user_id,
            date=datetime.now().date(),  # Record the current date of the sale
            total_amount=0  # Initially set the total amount to 0
        )

        # Add the sale to the session and flush to get the sale ID
        try:
            self.db.session.add(sale)
            self.db.session.flush()  # Ensure we get the sale ID before proceeding
        except Exception as e:
            print(f"Error while creating the sale: {e}")
            self.db.session.rollback()
            return None

        # Process each item in the sale
        for item_id, quantity in items:
            item = self.db.session.query(Inventory).filter_by(item_id=item_id).first()

            # Ensure the item exists and there is enough stock to complete the sale
            if item:
                if item.quantity >= quantity:
                    total_amount += item.cost * quantity  # Add to the total sale amount
                    sale_item = SaleItem(
                        sale_id=sale.sale_id,
                        item_id=item_id,
                        quantity=quantity
                    )
                    item.quantity -= quantity  # Update the inventory quantity

                    # Add the sale item to the session
                    self.db.session.add(sale_item)
                    print(f"Added {quantity} of {item.item_name} to the sale.")
                else:
                    print(f"Not enough stock for {item.item_name}. Only {item.quantity} available.")
            else:
                print(f"Item with ID {item_id} not found in inventory.")

        # Update the total amount of the sale after processing all items
        sale.total_amount = total_amount

        try:
            # Commit all changes to the database
            self.db.session.commit()
            print(f"Sale completed successfully! Total amount: ${total_amount:.2f}")
            return sale
        except Exception as e:
            # If something goes wrong, roll back the session and print an error message
            print(f"Error while completing the sale: {e}")
            self.db.session.rollback()
            return None
