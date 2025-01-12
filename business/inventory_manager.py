from database.models import Inventory

class InventoryManager:

    def __init__(self, db_session):
        self.db = db_session
        print("Inventory Manager initialized successfully!")

    def add_item(self, item_name, quantity, cost):
        if quantity < 0 or cost < 0:
            raise ValueError("Quantity and cost must be non-negative values.")

        new_item = Inventory(
            item_name=item_name,
            quantity=quantity,
            cost=cost
        )
        try:
            self.db.session.add(new_item)
            self.db.session.commit()
            print(f"Item '{item_name}' added successfully!")
            return new_item
        except Exception as e:
            self.db.session.rollback()
            print(f"Error while adding item: {e}")
            return None

    def update_quantity(self, item_id, new_quantity):
        if new_quantity < 0:
            raise ValueError("Quantity must be a non-negative value.")

        item = self.db.session.query(Inventory).filter_by(item_id=item_id).first()

        if item:
            item.quantity = new_quantity
            try:
                self.db.session.commit()
                print(f"Quantity of item '{item.item_name}' updated to {new_quantity}.")
                return True
            except Exception as e:
                self.db.session.rollback()
                print(f"Error while updating quantity: {e}")
                return False
        else:
            print(f"Item with ID {item_id} not found.")
            return False

    def delete_item(self, item_id):
        item = self.db.session.query(Inventory).filter_by(item_id=item_id).first()

        if item:
            try:
                self.db.session.delete(item)  # Delete the item from the database
                self.db.session.commit()  # Commit the transaction
                print(f"Item with ID {item_id} deleted successfully.")
                return True
            except Exception as e:
                self.db.session.rollback()  # Rollback in case of an error
                print(f"Error while deleting item: {e}")
                return False
        else:
            print(f"Item with ID {item_id} not found.")
            return False

    def get_all_items(self):
        items = self.db.session.query(Inventory).all()
        if items:
            print(f"Retrieved {len(items)} item(s) from inventory.")
            return items
        else:
            print("No items found in inventory.")
            return []

    def get_item_by_name(self, item_name):
        item = self.db.session.query(Inventory).filter_by(item_name=item_name).first()
        if item:
            print(f"Item found: {item_name}")
            return item
        else:
            print(f"Item '{item_name}' not found.")
            return None
