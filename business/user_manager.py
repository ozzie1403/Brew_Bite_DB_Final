from database.models import User
import hashlib
import os

class UserManager:
    def __init__(self, db_handler):
        # Initialize the UserManager with the database session.
        self.db = db_handler
        print("User Manager is ready to handle user-related tasks!")

    def _hash_password(self, password):
        """
        Hash the password with a salt for added security.
        We generate a random salt and combine it with the password, then hash the combination.
        """
        salt = os.urandom(16).hex()  # Generate a random salt for each password.
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()  # Hash the password + salt combination.
        return f"{salt}${hashed}"  # Return the salt and hashed password as a single string.

    def _verify_password(self, password, stored_hash):
        """
        Verify if the provided password matches the stored password hash.
        This method extracts the salt from the stored hash and recomputes the hash to check.
        """
        salt, hash_value = stored_hash.split('$')
        computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return computed_hash == hash_value

    def create_user(self, username, password, email):
        """
        Create a new user account with the provided username, password, and email.
        The password is hashed before saving it to the database for security.
        """
        if not username or not password or not email:
            print("Error: All fields (username, password, email) must be provided.")
            return None

        hashed = self._hash_password(password)
        new_user = User(
            username=username,
            password=hashed,
            email=email
        )
        try:
            self.db.session.add(new_user)
            self.db.session.commit()
            print(f"User '{username}' created successfully!")
            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            self.db.session.rollback()
            return None

    def verify_user(self, username, password):
        """
        Verify the user's credentials by checking if the username exists and the password matches.
        """
        user = self.db.session.query(User).filter_by(username=username).first()
        if user and self._verify_password(password, user.password):
            print(f"User '{username}' verified successfully!")
            return user
        print(f"Verification failed for user '{username}'.")
        return None

    def get_user(self, user_id):
        """
        Retrieve a user by their user_id.
        """
        user = self.db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            print(f"User found: {user.username}")
        else:
            print(f"No user found with ID {user_id}.")
        return user

    def get_all_users(self):
        """
        Get a list of all users in the database.
        """
        users = self.db.session.query(User).all()
        print(f"Retrieved {len(users)} user(s) from the database.")
        return users

    def update_user_password(self, user_id, new_password):
        """
        Update the user's password by user ID.
        The new password is hashed before saving.
        """
        user = self.get_user(user_id)
        if user:
            user.password = self._hash_password(new_password)
            try:
                self.db.session.commit()
                print(f"Password for user '{user.username}' updated successfully!")
                return True
            except Exception as e:
                print(f"Error updating password: {e}")
                self.db.session.rollback()
                return False
        print(f"User with ID {user_id} not found.")
        return False

    def update_user_email(self, user_id, new_email):
        """
        Update the user's email by user ID.
        """
        user = self.get_user(user_id)
        if user:
            user.email = new_email
            try:
                self.db.session.commit()
                print(f"Email for user '{user.username}' updated to {new_email}.")
                return True
            except Exception as e:
                print(f"Error updating email: {e}")
                self.db.session.rollback()
                return False
        print(f"User with ID {user_id} not found.")
        return False

    def delete_user(self, user_id):
        """
        Delete a user from the database by user ID.
        """
        user = self.get_user(user_id)
        if user:
            try:
                self.db.session.delete(user)
                self.db.session.commit()
                print(f"User '{user.username}' deleted successfully!")
                return True
            except Exception as e:
                print(f"Error deleting user: {e}")
                self.db.session.rollback()
                return False
        print(f"User with ID {user_id} not found.")
        return False
