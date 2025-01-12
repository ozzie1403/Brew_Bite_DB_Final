import tkinter as tk
from tkinter import ttk, messagebox

class UsersWindow:
    def __init__(self, parent, user_manager, current_user):
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("800x600")

        self.user_manager = user_manager
        self.current_user = current_user


        self.list_frame = ttk.Frame(self.window, padding="10")
        self.list_frame.grid(row=0, column=0, sticky="nsew")

        self.form_frame = ttk.Frame(self.window, padding="10")
        self.form_frame.grid(row=0, column=1, sticky="nsew")

        # user list setup
        self.setup_users_list()
        self.setup_user_form()

        # Loads existing users
        self.load_users()

    def setup_users_list(self):
        columns = ('ID', 'Username', 'Email')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')

        # Configure column headers and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Bind the selection event to populate the user form when a user is selected
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Add vertical scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def setup_user_form(self):
        """
        Set up the user form for adding or updating user details.
        """
        # Username field
        ttk.Label(self.form_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.username_var).grid(row=0, column=1, pady=5)

        # Password field
        ttk.Label(self.form_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)

        # Email field
        ttk.Label(self.form_frame, text="Email:").grid(row=2, column=0, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.email_var).grid(row=2, column=1, pady=5)

        # Buttons for Add, Update, Delete actions
        ttk.Button(self.form_frame, text="Add User", command=self.add_user).grid(row=3, column=0, pady=10)
        ttk.Button(self.form_frame, text="Update User", command=self.update_user).grid(row=3, column=1, pady=10)
        ttk.Button(self.form_frame, text="Delete User", command=self.delete_user).grid(row=3, column=2, pady=10)

    def load_users(self):
        """
        Loads the list of users into the treeview from the user manager.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in self.user_manager.get_all_users():
            # Insert each user's information into the treeview
            self.tree.insert('', 'end', values=(user.user_id, user.username, user.email))

    def add_user(self):
        """
        Adds a new user to the system by getting details from the form and passing them to the user manager.
        """
        try:
            username = self.username_var.get()
            password = self.password_var.get()
            email = self.email_var.get()

            # Validate that all fields are filled in
            if not all([username, password, email]):
                raise ValueError("All fields are required")

            # Call the user manager to create the user
            self.user_manager.create_user(username, password, email)

            # Reload the user list and clear the form
            self.load_users()
            self.clear_form()

            messagebox.showinfo("Success", "User added successfully!")

        except Exception as e:
            # Show an error message if something goes wrong
            messagebox.showerror("Error", str(e))

    def update_user(self):
        """
        Updates an existing user's details. A user must be selected from the list to update.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to update")
            return

        try:
            user_id = self.tree.item(selected[0])['values'][0]
            email = self.email_var.get()
            password = self.password_var.get()

            # Only update the fields that are provided
            if password:
                self.user_manager.update_user_password(user_id, password)
            if email:
                self.user_manager.update_user_email(user_id, email)

            # Reload the user list to reflect the changes
            self.load_users()

            messagebox.showinfo("Success", "User updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_user(self):
        """
        Deletes a selected user from the system. The currently logged-in user cannot be deleted.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        user_id = self.tree.item(selected[0])['values'][0]

        # Ensure the current user can't delete themselves
        if user_id == self.current_user.user_id:
            messagebox.showerror("Error", "Cannot delete your own account")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            try:
                # Call the user manager to delete the selected user
                self.user_manager.delete_user(user_id)

                # Reload the user list and clear the form
                self.load_users()
                self.clear_form()

                messagebox.showinfo("Success", "User deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_select(self, event):
        """
        Fills the user form with the details of the selected user from the list.
        """
        selected = self.tree.selection()
        if selected:
            user = self.tree.item(selected[0])['values']
            # Populate the form with the user's information
            self.username_var.set(user[1])
            self.email_var.set(user[2])
            self.password_var.set('')  # Don't show the password for security

    def clear_form(self):
        """
        Clears all fields in the user form after an action is performed.
        """
        self.username_var.set('')
        self.password_var.set('')
        self.email_var.set('')
