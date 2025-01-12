from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

class DatabaseHandler:

    def __init__(self):
        try:
            # Creates engine
            self.engine = create_engine('sqlite:///cafe.db')
            # Creates all tables
            Base.metadata.create_all(self.engine)

            # session binder with engine
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print("Database connection established successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def commit(self):
        try:
            self.session.commit()
            print("Changes committed to the database successfully!")
        except Exception as e:
            print(f"Error committing to the database: {e}")
            self.rollback()

    def rollback(self):
        try:
            self.session.rollback()
            print("Transaction rolled back due to an error.")
        except Exception as e:
            print(f"Error rolling back the transaction: {e}")

    def close(self):
        try:
            self.session.close()
            print("Database session closed.")
        except Exception as e:
            print(f"Error closing the database session: {e}")
