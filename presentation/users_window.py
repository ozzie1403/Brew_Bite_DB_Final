import tkinter as tk
from tkinter import ttk, messagebox

class UsersWindow
    def __init__(self, parent, user_manager, current_user):
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("800x600")
        
        self.user_manager = user_manager
        self.current_user = current_user
        
        # Create frames
        self.list_frame = ttk.Frame(self.window, padding="10")
        self.list_frame.grid(row=0, column=0, sticky="nsew")
        
        self.form_frame = ttk.Frame(self.window, padding="10")
        self.form_frame.grid(row=0, column=1, sticky="nsew")
        
        self.setup_users_list()
        self.setup_user_form()
        self.load_users()
    
    def setup_users_list(self):
        columns = ('ID', 'Username', 'Email')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def setup_user_form(self):
        # Username
        ttk.Label(self.form_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.username_var).grid(row=0, column=1, pady=5)
        
        # Password
        ttk.Label(self.form_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)
        
        # Email
        ttk.Label(self.form_frame, text="Email:").grid(row=2, column=0, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.email_var).grid(row=2, column=1, pady=5)
        
        # Buttons
        ttk.Button(self.form_frame, text="Add User", command=self.add_user).grid(row=3, column=0, pady=10)
        ttk.Button(self.form_frame, text="Update User", command=self.update_user).grid(row=3, column=1, pady=10)
        ttk.Button(self.form_frame, text="Delete User", command=self.delete_user).grid(row=3, column=2, pady=10)
    
    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for user in self.user_manager.get_all_users():
            self.tree.insert('', 'end', values=(user.user_id, user.username, user.email))
    
    def add_user(self):
        try:
            username = self.username_var.get()
            password = self.password_var.get()
            email = self.email_var.get()
            
            if not all([username, password, email]):
                raise ValueError("All fields are required")
            
            self.user_manager.create_user(username, password, email)
            self.load_users()
            self.clear_form()
            messagebox.showinfo("Success", "User added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to update")
            return
        
        try:
            user_id = self.tree.item(selected[0])['values'][0]
            email = self.email_var.get()
            password = self.password_var.get()
            
            if password:  # Only update password if provided
                self.user_manager.update_user_password(user_id, password)
            if email:  # Only update email if provided
                self.user_manager.update_user_email(user_id, email)
            
            self.load_users()
            messagebox.showinfo("Success", "User updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        user_id = self.tree.item(selected[0])['values'][0]
        if user_id == self.current_user.user_id:
            messagebox.showerror("Error", "Cannot delete your own account")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            try:
                self.user_manager.delete_user(user_id)
                self.load_users()
                self.clear_form()
                messagebox.showinfo("Success", "User deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            user = self.tree.item(selected[0])['values']
            self.username_var.set(user[1])
            self.email_var.set(user[2])
            self.password_var.set('')  # Clear password field for security
    
    def clear_form(self):
        self.username_var.set('')
        self.password_var.set('')
        self.email_var.set('')