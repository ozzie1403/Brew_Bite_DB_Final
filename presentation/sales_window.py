import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class saleswindow:
    def __init__(self, parent, sales_manager, inventory_manager, current_user):
        self.window = tk.Toplevel(parent)
        self.window.title("Sales Management")
        self.window.geometry("1000x600")
        
        self.sales_manager = sales_manager
        self.inventory_manager = inventory_manager
        self.current_user = current_user
        self.cart = []
        
        self.setup_ui()
        self.load_inventory()
    
    def setup_ui(self):
        self.inventory_frame = ttk.LabelFrame(self.window, text="Items available", padding="10")
        self.inventory_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.cart_frame = ttk.LabelFrame(self.window, text="Shopping cart", padding="10")
        self.cart_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.setup_inventory_list()
        self.setup_cart_list()
        self.setup_total_section()
    
    def setup_inventory_list(self):
        columns = ('ID', 'Name', 'Available', 'Cost')
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=columns, show='headings')
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100)
        
        self.inventory_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        ttk.Label(self.inventory_frame, text="Quantity:").grid(row=1, column=0, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(self.inventory_frame, textvariable=self.quantity_var).grid(row=1, column=1, pady=5)
        ttk.Button(self.inventory_frame, text="Add to Cart", command=self.add_to_cart).grid(row=2, column=0, columnspan=2, pady=5)
    
    def setup_cart_list(self):
        columns = ('ID', 'Name', 'Quantity', 'Cost', 'Total')
        self.cart_tree = ttk.Treeview(self.cart_frame, columns=columns, show='headings')
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)
        
        self.cart_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        ttk.Button(self.cart_frame, text="Remove Selected", command=self.remove_from_cart).grid(row=1, column=0, pady=5)
        ttk.Button(self.cart_frame, text="Clear Cart", command=self.clear_cart).grid(row=1, column=1, pady=5)
    
    def setup_total_section(self):
        self.total_frame = ttk.Frame(self.cart_frame, padding="10")
        self.total_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        self.total_var = tk.StringVar(value="Total: £0.00")
        ttk.Label(self.total_frame, textvariable=self.total_var, font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.total_frame, text="Complete Sale", command=self.complete_sale).pack(side=tk.RIGHT, padx=5)
    
    def load_inventory(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        for item in self.inventory_manager.get_all_items():
            self.inventory_tree.insert('', 'end', values=(item.item_id, item.item_name, item.quantity, f"£{item.cost:.2f}"))
    
    def add_to_cart(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to add")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            item = self.inventory_tree.item(selected[0])['values']
            if quantity > item[2]:  # Available quantity
                raise ValueError("Not enough items in stock")
            
            total = quantity * float(item[3].replace('£', ''))
            self.cart.append((item[0], item[1], quantity, float(item[3].replace('£', '')), total))
            self.update_cart_display()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            return
        
        item_index = self.cart_tree.index(selected[0])
        self.cart.pop(item_index)
        self.update_cart_display()
    
    def clear_cart(self):
        self.cart = []
        self.update_cart_display()
    
    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        total = 0
        for item in self.cart:
            self.cart_tree.insert('', 'end', values=item)
            total += item[4]
        
        self.total_var.set(f"Total: £{total:.2f}")
    
    def complete_sale(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        try:
            items = [(item[0], item[2]) for item in self.cart]  # (item_id, quantity)
            self.sales_manager.create_sale(self.current_user.user_id, items)
            messagebox.showinfo("Success", "Sale completed successfully!")
            self.clear_cart()
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Sorry! process failed!", str(e))