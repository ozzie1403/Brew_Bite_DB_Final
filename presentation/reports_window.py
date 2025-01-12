import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json

from database.models import Sale, Inventory

class ReportsWindow:

    def __init__(self, parent, db_handler, current_user):
        self.window = tk.Toplevel(parent)
        self.window.title("Financial Reports")
        self.window.geometry("800x600")

        self.db = db_handler
        self.current_user = current_user

        self.setup_ui()

    def setup_ui(self):
        self.report_frame = ttk.LabelFrame(self.window, text="Generate Report", padding="10")
        self.report_frame.pack(fill=tk.X, padx=5, pady=5)

        report_types = [
            "Daily Sales",
            "Monthly Sales",
            "Inventory Status",
            "Low Stock Alert",
            "Revenue Analysis"
        ]

        self.report_type = tk.StringVar(value=report_types[0])

        for report in report_types:
            ttk.Radiobutton(self.report_frame, text=report, value=report, variable=self.report_type).pack(anchor=tk.W)

        ttk.Button(self.report_frame, text="Generate Report", command=self.generate_report).pack(pady=10)

        self.display_frame = ttk.LabelFrame(self.window, text="Report Results", padding="10")
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.report_text = tk.Text(self.display_frame, wrap=tk.WORD, width=80, height=20)
        self.report_text.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self.window, text="Export Report", command=self.export_report).pack(pady=5)

    def generate_report(self):
        report_type = self.report_type.get()
        self.report_text.delete(1.0, tk.END)  # Clear the previous report content

        try:
            if report_type == "Daily Sales":
                self.generate_daily_sales_report()
            elif report_type == "Monthly Sales":
                self.generate_monthly_sales_report()
            elif report_type == "Inventory Status":
                self.generate_inventory_report()
            elif report_type == "Low Stock Alert":
                self.generate_low_stock_report()
            elif report_type == "Revenue Analysis":
                self.generate_revenue_analysis()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def generate_daily_sales_report(self):

        today = datetime.now().date()
        sales = self.db.session.query(Sale).filter(Sale.date == today).all()

        report = f"Daily Sales Report - {today}\n\n"
        total_revenue = 0

        for sale in sales:
            report += f"Sale ID: {sale.sale_id}\n"
            report += f"Time: {sale.date}\n"
            report += f"Amount: GBP{sale.total_amount:.2f}\n"
            report += "-" * 40 + "\n"
            total_revenue += sale.total_amount

        report += f"\nTotal Daily Revenue: GBP {total_revenue:.2f}"
        self.report_text.insert(tk.END, report)

    def generate_monthly_sales_report(self):

        today = datetime.now().date()
        first_day = today.replace(day=1)
        sales = self.db.session.query(Sale).filter(Sale.date >= first_day).all()

        report = f"Monthly Sales Report - {today.strftime('%B %Y')}\n\n"
        total_revenue = 0
        daily_totals = {}

        for sale in sales:
            date_str = sale.date.strftime('%Y-%m-%d')
            daily_totals[date_str] = daily_totals.get(date_str, 0) + sale.total_amount
            total_revenue += sale.total_amount

        for date, amount in sorted(daily_totals.items()):
            report += f"{date}: GBP {amount:.2f}\n"

        report += f"\nTotal Monthly Revenue: GBP {total_revenue:.2f}"
        self.report_text.insert(tk.END, report)

    def generate_inventory_report(self):

        inventory = self.db.session.query(Inventory).all()

        report = "Current Inventory Status\n\n"
        total_value = 0

        for item in inventory:
            value = item.quantity * item.cost
            total_value += value
            report += f"Item: {item.item_name}\n"
            report += f"Quantity: {item.quantity}\n"
            report += f"Unit Cost: GBP {item.cost:.2f}\n"
            report += f"Total Value: GBP {value:.2f}\n"
            report += "-" * 40 + "\n"

        report += f"\nTotal Inventory Value: GBP {total_value:.2f}"
        self.report_text.insert(tk.END, report)

    def generate_low_stock_report(self):

        LOW_STOCK_THRESHOLD = 10
        low_stock = self.db.session.query(Inventory).filter(Inventory.quantity < LOW_STOCK_THRESHOLD).all()

        report = "Low Stock Alert Report\n\n"

        if not low_stock:
            report += "No items are running low on stock."
        else:
            for item in low_stock:
                report += f"Item: {item.item_name}\n"
                report += f"Current Quantity: {item.quantity}\n"
                report += f"Reorder Suggested: {LOW_STOCK_THRESHOLD - item.quantity} units\n"
                report += "-" * 40 + "\n"

        self.report_text.insert(tk.END, report)

    def generate_revenue_analysis(self):

        today = datetime.now().date()
        last_month = today - timedelta(days=30)
        sales = self.db.session.query(Sale).filter(Sale.date >= last_month).all()

        report = "Revenue Analysis (Last 30 Days)\n\n"

        # Daily revenue breakdown
        daily_revenue = {}
        for sale in sales:
            date_str = sale.date.strftime('%Y-%m-%d')
            daily_revenue[date_str] = daily_revenue.get(date_str, 0) + sale.total_amount

        # Calculate statistics
        total_revenue = sum(daily_revenue.values())
        avg_daily_revenue = total_revenue / len(daily_revenue) if daily_revenue else 0

        report += f"Total Revenue: GBP {total_revenue:.2f}\n"
        report += f"Average Daily Revenue: GBP {avg_daily_revenue:.2f}\n\n"
        report += "Daily Breakdown:\n"

        for date, amount in sorted(daily_revenue.items()):
            report += f"{date}: GBP {amount:.2f}\n"

        self.report_text.insert(tk.END, report)

    def export_report(self):

        report_content = self.report_text.get(1.0, tk.END)
        if not report_content.strip():
            messagebox.showwarning("Warning", "No report to export")
            return

        try:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report_content)
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
