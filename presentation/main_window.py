import tkinter as tk
from tkinter import ttk, messagebox
from database.db_handler import mainsession
from business.user_manager import usermanager
from business.inventory_manager import inventorymanager
from business.sales_manager import salesmanager
from presentation.inventory_window import InventoryWindow
from presentation.sales_window import saleswindow
from presentation.reports_window import ReportsWindow
from presentation.users_window import userswindow

class mainwindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Brew & Bite cafe management system")
        self.root.geometry("800x600")

        self.db = mainsession()
        self.user_manager = usermanager(self.db)
        self.inventory_manager = inventorymanager(self.db)
        self.sales_manager = salesmanager(self.db)
        
        self.current_user = None
        self.setup_login_frame()
    
    def setup_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1, pady=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)
        
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.login_frame, text="Register", command=self.show_register).grid(row=3, column=0, columnspan=2)
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        user = self.user_manager.verify_user(username, password)
        if user:
            self.current_user = user
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register New User")
        register_window.geometry("300x200")
        
        ttk.Label(register_window, text="Username:").pack(pady=5)
        username_var = tk.StringVar()
        ttk.Entry(register_window, textvariable=username_var).pack(pady=5)
        
        ttk.Label(register_window, text="Password:").pack(pady=5)
        password_var = tk.StringVar()
        ttk.Entry(register_window, textvariable=password_var, show="*").pack(pady=5)
        
        ttk.Label(register_window, text="Email:").pack(pady=5)
        email_var = tk.StringVar()
        ttk.Entry(register_window, textvariable=email_var).pack(pady=5)
        
        def register():
            try:
                self.user_manager.create_user(
                    username_var.get(),
                    password_var.get(),
                    email_var.get()
                )
                messagebox.showinfo("Success", "User registered successfully!")
                register_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(register_window, text="Register", command=register).pack(pady=10)
    
    def show_main_menu(self):
        self.login_frame.destroy()
        
        self.menu_frame = ttk.Frame(self.root, padding="20")
        self.menu_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(self.menu_frame, text=f"Welcome, {self.current_user.username}!").grid(row=0, column=0, columnspan=2, pady=10)
        
        buttons = [
            ("Manage Users", self.show_users),
            ("Manage Inventory", self.show_inventory),
            ("Record Sale", self.show_sales),
            ("View Reports", self.show_reports),
            ("Logout", self.logout)
        ]
        
        for i, (text, command) in enumerate(buttons, start=1):
            ttk.Button(self.menu_frame, text=text, command=command).grid(row=i, column=0, columnspan=2, pady=5)
    
    def show_users(self):
        userswindow(self.root, self.user_manager, self.current_user)
    
    def show_inventory(self):
        InventoryWindow(self.root, self.inventory_manager)
    
    def show_sales(self):
        saleswindow(self.root, self.sales_manager, self.inventory_manager, self.current_user)
    
    def show_reports(self):
        ReportsWindow(self.root, self.db, self.current_user)
    
    def logout(self):
        self.current_user = None
        self.menu_frame.destroy()
        self.setup_login_frame()
    
    def run(self):
        self.root.mainloop()