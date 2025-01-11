import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class SalesWindow:
    def __init__(self, parent, sales_manager, inventory_manager, current_user):
        """
        Initializes the sales window where the user can manage and process sales.

        Parameters:
        - parent: The parent Tkinter window.
        - sales_manager: The manager responsible for handling sales logic.
        - inventory_manager: The manager responsible for managing inventory.
        - current_user: The user currently logged in.
        """
        # Create a new window for managing sales
        self.window = tk.Toplevel(parent)
        self.window.title("Sales Management")
        self.window.geometry("1000x600")

        # Store the managers and current user
        self.sales_manager = sales_manager
        self.inventory_manager = inventory_manager
        self.current_user = current_user

        # Initialize an empty cart
        self.cart = []

        # Set up the user interface components
        self.setup_ui()

        # Load inventory items into the inventory list
        self.load_inventory()

    def setup_ui(self):
        """
        Set up the user interface components, including:
        - Inventory list
        - Shopping cart list
        - Total section (total amount of the cart)
        """
        # Left panel for displaying available items
        self.inventory_frame = ttk.LabelFrame(self.window, text="Available Items", padding="10")
        self.inventory_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Right panel for displaying items added to the shopping cart
        self.cart_frame = ttk.LabelFrame(self.window, text="Shopping Cart", padding="10")
        self.cart_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Set up the inventory list (treeview) and cart list (treeview)
        self.setup_inventory_list()
        self.setup_cart_list()

        # Set up the total section (display total amount of the cart)
        self.setup_total_section()

    def setup_inventory_list(self):
        """
        Set up the inventory list where available items are shown.
        Users can select items to add to the cart.
        """
        columns = ('ID', 'Name', 'Available', 'Cost')
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=columns, show='headings')

        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100)

        self.inventory_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Quantity entry field and Add to Cart button
        ttk.Label(self.inventory_frame, text="Quantity:").grid(row=1, column=0, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(self.inventory_frame, textvariable=self.quantity_var).grid(row=1, column=1, pady=5)
        ttk.Button(self.inventory_frame, text="Add to Cart", command=self.add_to_cart).grid(row=2, column=0,
                                                                                            columnspan=2, pady=5)

    def setup_cart_list(self):
        """
        Set up the cart list where items added to the cart are shown.
        Users can remove items or clear the cart entirely.
        """
        columns = ('ID', 'Name', 'Quantity', 'Cost', 'Total')
        self.cart_tree = ttk.Treeview(self.cart_frame, columns=columns, show='headings')

        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)

        self.cart_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Buttons for removing selected items or clearing the cart
        ttk.Button(self.cart_frame, text="Remove Selected", command=self.remove_from_cart).grid(row=1, column=0, pady=5)
        ttk.Button(self.cart_frame, text="Clear Cart", command=self.clear_cart).grid(row=1, column=1, pady=5)

    def setup_total_section(self):
        """
        Set up the section showing the total amount of the cart and the "Complete Sale" button.
        """
        self.total_frame = ttk.Frame(self.cart_frame, padding="10")
        self.total_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Total amount label
        self.total_var = tk.StringVar(value="Total: GBP 0.00")
        ttk.Label(self.total_frame, textvariable=self.total_var, font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)

        # Button to complete the sale
        ttk.Button(self.total_frame, text="Complete Sale", command=self.complete_sale).pack(side=tk.RIGHT, padx=5)

    def load_inventory(self):
        """
        Load the inventory items from the inventory manager and display them in the inventory list.
        """
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        for item in self.inventory_manager.get_all_items():
            self.inventory_tree.insert('', 'end',
                                       values=(item.item_id, item.item_name, item.quantity, f"GBP {item.cost:.2f}"))

    def add_to_cart(self):
        """
        Add the selected item from the inventory to the shopping cart.
        The user must specify a quantity and ensure that enough stock is available.
        """
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to add")
            return

        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            item = self.inventory_tree.item(selected[0])['values']
            available_quantity = item[2]
            if quantity > available_quantity:  # Check if enough stock is available
                raise ValueError("Not enough items in stock")

            total = quantity * float(item[3].replace('GBP ', '').replace('gbp', ''))
            self.cart.append((item[0], item[1], quantity, float(item[3].replace('GBP ', '').replace('gbp', '')), total))
            self.update_cart_display()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_from_cart(self):
        """
        Remove the selected item from the shopping cart.
        """
        selected = self.cart_tree.selection()
        if not selected:
            return  # Do nothing if no item is selected

        item_index = self.cart_tree.index(selected[0])
        self.cart.pop(item_index)
        self.update_cart_display()

    def clear_cart(self):
        """
        Clear all items from the shopping cart.
        """
        self.cart = []
        self.update_cart_display()

    def update_cart_display(self):
        """
        Update the cart display after adding/removing items. It also updates the total amount.
        """
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total = 0
        for item in self.cart:
            self.cart_tree.insert('', 'end', values=item)
            total += item[4]

        self.total_var.set(f"Total: GBP {total:.2f}")

    def complete_sale(self):
        """
        Complete the sale by processing the items in the cart. This will record the sale and
        update the inventory.
        """
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty")
            return

        try:
            # Create the sale with item_id and quantity
            items = [(item[0], item[2]) for item in self.cart]  # (item_id, quantity)
            self.sales_manager.create_sale(self.current_user.user_id, items)
            messagebox.showinfo("Success", "Sale completed successfully!")

            # Clear the cart and reload the inventory
            self.clear_cart()
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete sale: {str(e)}")
