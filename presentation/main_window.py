import tkinter as tk
from tkinter import ttk, messagebox
from database.db_handler import DatabaseHandler
from business.user_manager import UserManager
from business.inventory_manager import InventoryManager
from business.sales_manager import SalesManager
from presentation.inventory_window import InventoryWindow
from presentation.sales_window import SalesWindow
from presentation.reports_window import ReportsWindow
from presentation.users_window import UsersWindow

class MainWindow:
    def __init__(self):
        """
        Initializes the main window of the Brew and Bite Café Management System.
        Sets up the necessary database connections, user managers, and initial login screen.
        """
        # Initialize the main application window
        self.root = tk.Tk()
        self.root.title("Brew and Bite Café Management System")
        self.root.geometry("800x600")

        # Set up database and business logic handlers
        self.db = DatabaseHandler()
        self.user_manager = UserManager(self.db)
        self.inventory_manager = InventoryManager(self.db)
        self.sales_manager = SalesManager(self.db)

        # Store the currently logged-in user
        self.current_user = None

        # Start with the login screen
        self.setup_login_frame()

    def setup_login_frame(self):
        """
        Creates the login screen where users can enter their credentials to log in.
        """
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Username input
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1, pady=5)

        # Password input
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)

        # Login button
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

        # Register button for new users
        ttk.Button(self.login_frame, text="Register", command=self.show_register).grid(row=3, column=0, columnspan=2)

    def login(self):
        """
        Handles the login process by verifying the user's credentials.
        If valid, it proceeds to the main menu; otherwise, shows an error.
        """
        username = self.username_var.get()
        password = self.password_var.get()
        user = self.user_manager.verify_user(username, password)

        if user:
            # Store the logged-in user
            self.current_user = user
            # Show the main menu after successful login
            self.show_main_menu()
        else:
            # Show an error message if login fails
            messagebox.showerror("Error", "Invalid username or password")

    def show_register(self):
        """
        Opens the registration window where new users can create an account.
        """
        register_window = tk.Toplevel(self.root)
        register_window.title("Register New User")
        register_window.geometry("300x200")

        # Fields for username, password, and email
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
            """
            Handles the registration process, adding a new user to the system.
            """
            try:
                self.user_manager.create_user(
                    username_var.get(),
                    password_var.get(),
                    email_var.get()
                )
                messagebox.showinfo("Success", "User registered successfully!")
                register_window.destroy()  # Close the register window
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Register button
        ttk.Button(register_window, text="Register", command=register).pack(pady=10)

    def show_main_menu(self):
        """
        After successful login, displays the main menu with options to manage the system.
        """
        self.login_frame.destroy()

        # Create the main menu frame
        self.menu_frame = ttk.Frame(self.root, padding="20")
        self.menu_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Welcome message
        ttk.Label(self.menu_frame, text=f"Welcome, {self.current_user.username}!").grid(row=0, column=0, columnspan=2,
                                                                                        pady=10)

        # Buttons for different system functionalities
        buttons = [
            ("Manage Users", self.show_users),
            ("Manage Inventory", self.show_inventory),
            ("Record Sale", self.show_sales),
            ("View Reports", self.show_reports),
            ("Logout", self.logout)
        ]

        # Create a button for each functionality
        for i, (text, command) in enumerate(buttons, start=1):
            ttk.Button(self.menu_frame, text=text, command=command).grid(row=i, column=0, columnspan=2, pady=5)

    def show_users(self):
        """
        Opens the user management window where users can be added, updated, or deleted.
        """
        UsersWindow(self.root, self.user_manager, self.current_user)

    def show_inventory(self):
        """
        Opens the inventory management window where items can be added, updated, or deleted.
        """
        InventoryWindow(self.root, self.inventory_manager)

    def show_sales(self):
        """
        Opens the sales window where sales transactions can be recorded.
        """
        SalesWindow(self.root, self.sales_manager, self.inventory_manager, self.current_user)

    def show_reports(self):
        """
        Opens the reports window where financial and other system reports can be viewed.
        """
        ReportsWindow(self.root, self.db, self.current_user)

    def logout(self):
        """
        Logs the user out, returns to the login screen.
        """
        self.current_user = None
        self.menu_frame.destroy()
        self.setup_login_frame()

    def run(self):
        """
        Starts the main application loop for the window.
        """
        self.root.mainloop()
