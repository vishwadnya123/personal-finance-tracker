import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.transactions = []

        # Set up the main frame
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Transaction date
        self.date_label = ttk.Label(self.frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(self.frame)
        self.date_entry.grid(row=0, column=1, sticky=tk.W)

        # Category
        self.category_label = ttk.Label(self.frame, text="Category:")
        self.category_label.grid(row=1, column=0, sticky=tk.W)
        self.category_entry = ttk.Entry(self.frame)
        self.category_entry.grid(row=1, column=1, sticky=tk.W)

        # Description
        self.description_label = ttk.Label(self.frame, text="Description:")
        self.description_label.grid(row=2, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(self.frame)
        self.description_entry.grid(row=2, column=1, sticky=tk.W)

        # Amount
        self.amount_label = ttk.Label(self.frame, text="Amount:")
        self.amount_label.grid(row=3, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(self.frame)
        self.amount_entry.grid(row=3, column=1, sticky=tk.W)

        # Add transaction button
        self.add_button = ttk.Button(self.frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Show report button
        self.report_button = ttk.Button(self.frame, text="Show Report", command=self.show_report)
        self.report_button.grid(row=5, column=0, columnspan=2, pady=10)

    def add_transaction(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        if not date or not category or not description or not amount:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number.")
            return

        self.transactions.append({
            'Date': datetime.strptime(date, "%Y-%m-%d"),
            'Category': category,
            'Description': description,
            'Amount': amount
        })

        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        
        messagebox.showinfo("Transaction Added", "Your transaction has been added successfully.")

    def show_report(self):
        if not self.transactions:
            messagebox.showwarning("No Data", "No transactions to show.")
            return

        df = pd.DataFrame(self.transactions)

        # Monthly summary
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_summary = df.groupby('Month')['Amount'].sum().reset_index()
        monthly_summary['Month'] = monthly_summary['Month'].dt.strftime('%Y-%m')

        # Plot spending patterns
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Month', y='Amount', data=monthly_summary, palette='viridis')
        plt.title('Monthly Spending Overview')
        plt.xlabel('Month')
        plt.ylabel('Total Amount')
        plt.xticks(rotation=45)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
