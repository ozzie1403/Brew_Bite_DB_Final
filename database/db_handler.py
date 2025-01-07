from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine('sqlite:///cafe.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()
    
    def close(self):
        self.session.close()