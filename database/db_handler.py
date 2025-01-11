from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import base

class mainsession:
    def __init__(self):
        self.engine = create_engine('sqlite:///cafe.db')
        base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()
    
    def close(self):
        self.session.close()