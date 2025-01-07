from database.models import User
import hashlib
import os

class UserManager:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def _hash_password(self, password):
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def _verify_password(self, password, stored_hash):
        salt, hash_value = stored_hash.split('$')
        computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return computed_hash == hash_value
    
    def create_user(self, username, password, email):
        hashed = self._hash_password(password)
        new_user = User(
            username=username,
            password=hashed,
            email=email
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user
    
    def verify_user(self, username, password):
        user = self.db.session.query(User).filter_by(username=username).first()
        if user and self._verify_password(password, user.password):
            return user
        return None
    
    def get_user(self, user_id):
        return self.db.session.query(User).filter_by(user_id=user_id).first()
    
    def get_all_users(self):
        return self.db.session.query(User).all()
    
    def update_user_password(self, user_id, new_password):
        user = self.get_user(user_id)
        if user:
            user.password = self._hash_password(new_password)
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