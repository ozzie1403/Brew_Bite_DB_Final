from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

class DatabaseHandler:
    def __init__(self):
        """
        Initialize the database connection and session.
        Creates the engine, binds it to the session, and ensures all tables are created.
        """
        try:
            # Create the engine that connects to the SQLite database
            self.engine = create_engine('sqlite:///cafe.db')
            # Create all tables based on the models defined in Base (if they don't exist)
            Base.metadata.create_all(self.engine)

            # Bind the session to the engine
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print("Database connection established successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def commit(self):
        """
        Commit the current transaction to the database.
        This ensures any changes made in the session are saved.
        """
        try:
            self.session.commit()
            print("Changes committed to the database successfully!")
        except Exception as e:
            print(f"Error committing to the database: {e}")
            self.rollback()

    def rollback(self):
        """
        Rollback the current transaction.
        If an error occurs, this method will undo any changes made during the transaction.
        """
        try:
            self.session.rollback()
            print("Transaction rolled back due to an error.")
        except Exception as e:
            print(f"Error rolling back the transaction: {e}")

    def close(self):
        """
        Close the database session.
        This method should be called when the session is no longer needed to free up resources.
        """
        try:
            self.session.close()
            print("Database session closed.")
        except Exception as e:
            print(f"Error closing the database session: {e}")
