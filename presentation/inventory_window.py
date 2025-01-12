import tkinter as tk
from tkinter import ttk, messagebox

class InventoryWindow:

    def __init__(self, parent, inventory_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Inventory Management")
        self.window.geometry("800x600")

        # inventory manager stored
        self.inventory_manager = inventory_manager

        # frames created
        self.list_frame = ttk.Frame(self.window, padding="10")
        self.list_frame.grid(row=0, column=0, sticky="nsew")

        self.form_frame = ttk.Frame(self.window, padding="10")
        self.form_frame.grid(row=0, column=1, sticky="nsew")

        # setup components
        self.setup_inventory_list()
        self.setup_item_form()
        self.load_inventory()

    def setup_inventory_list(self):
        columns = ('ID', 'Name', 'Quantity', 'Cost')

        # treeview widget integrated
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')

        # defined column headers and their widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def setup_item_form(self):

        # item name field
        ttk.Label(self.form_frame, text="Item Name:").grid(row=0, column=0, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, pady=5)

        # quantity
        ttk.Label(self.form_frame, text="Quantity:").grid(row=1, column=0, pady=5)
        self.quantity_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.quantity_var).grid(row=1, column=1, pady=5)

        # Cost field
        ttk.Label(self.form_frame, text="Cost:").grid(row=2, column=0, pady=5)
        self.cost_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.cost_var).grid(row=2, column=1, pady=5)

        # Buttons to handle item actions
        ttk.Button(self.form_frame, text="Add New", command=self.add_item).grid(row=3, column=0, pady=10)
        ttk.Button(self.form_frame, text="Update", command=self.update_item).grid(row=3, column=1, pady=10)
        ttk.Button(self.form_frame, text="Delete", command=self.delete_item).grid(row=3, column=2, pady=10)

    def load_inventory(self):

        # Clear the existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add all items from the inventory to the treeview
        for item in self.inventory_manager.get_all_items():
            self.tree.insert('', 'end', values=(item.item_id, item.item_name, item.quantity, item.cost))

    def add_item(self):

        try:
            name = self.name_var.get()
            quantity = int(self.quantity_var.get())
            cost = float(self.cost_var.get())

            # Add the new item through the inventory manager
            self.inventory_manager.add_item(name, quantity, cost)
            self.load_inventory()  # Reload the list of inventory items
            self.clear_form()  # Clear the input fields
            messagebox.showinfo("Success", "Item added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")

    def update_item(self):

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to update")
            return

        try:
            item_id = self.tree.item(selected[0])['values'][0]
            quantity = int(self.quantity_var.get())

            # Update the selected item's quantity through the inventory manager
            self.inventory_manager.update_quantity(item_id, quantity)
            self.load_inventory()
            messagebox.showinfo("Success", "Item updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            try:
                item_id = self.tree.item(selected[0])['values'][0]
                self.inventory_manager.delete_item(item_id)
                self.load_inventory()
                self.clear_form()
                messagebox.showinfo("Success", "Item deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete item: {e}")

    def on_select(self, event):

        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.name_var.set(item[1])
            self.quantity_var.set(item[2])
            self.cost_var.set(item[3])

    def clear_form(self):

        self.name_var.set('')
        self.quantity_var.set('')
        self.cost_var.set('')
