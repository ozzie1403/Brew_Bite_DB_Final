from database.models import user
import hashlib
import os

class usermanager:
    def __init__(self, db_session):
        self.db = db_session
    
    def hash_password(self, password):
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def verify_password(self, password, stored_hash):
        salt, hash_value = stored_hash.split('$')
        calculated_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return calculated_hash == hash_value
    
    def create_user(self, username, password, email):
        hashed = self.hash_password(password)
        new_user = user(
            username=username,
            password=hashed,
            email=email
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user
    
    def verify_user(self, username, password, user):
        user = self.db.session.query(user).filter_by(username=username).first()
        if user and self.verify_password(password, user.password):
            return user
        return None
    
    def get_user(self, user_id):
        return self.db.session.query(user).filter_by(user_id=user_id).first()
    
    def get_all_users(self):
        return self.db.session.query(user).all()
    
    def update_user_password(self, user_id, new_password):
        user = self.get_user(user_id)
        if user:
            user.password = self.hash_password(new_password)
            self.db.session.commit()
            return True
        return False
    
    def update_user_email(self, user_id, new_email):
        user = self.get_user(user_id)
        if user:
            user.email = new_email
            self.db.session.commit()
            return True
        return False
    
    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
            return True
        return False