import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import json
from pathlib import Path

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.title("Modern Bill Invoice")
        
        # --- App Data Setup ---
        self.setup_directories_and_files()
        self.load_data()
        self.setup_invoice_number()

        # --- Variables ---
        self.cname_var = tk.StringVar()
        self.invoice_var = tk.StringVar(value=self.format_invoice_num(self.current_inv_num))
        self.total_var = tk.DoubleVar(value=0.0)
        
        # Lists to hold row variables (DRY principle)
        self.max_items = 6
        self.item_vars = [tk.StringVar(value="None") for _ in range(self.max_items)]
        self.price_vars = [tk.DoubleVar(value=0.0) for _ in range(self.max_items)]
        self.qty_vars = [tk.IntVar(value=0) for _ in range(self.max_items)]
        self.amount_vars = [tk.DoubleVar(value=0.0) for _ in range(self.max_items)]

        self.build_ui()

    def setup_directories_and_files(self):
        """Creates necessary folders and default files if they don't exist to prevent crashes."""
        self.docs_dir = Path("Docs")
        self.docs_dir.mkdir(exist_ok=True)
    
        self.items_prices_file = self.docs_dir / "prices.json"
        
        # Create dummy data if missing          
        if not self.items_prices_file.exists():
            default_prices = {"price": {"Apple": 20.0, "Banana": 10.0, "Orange": 15.0, "Milk": 50.0, "Bread": 40.0}}
            with open(self.items_prices_file, "w") as f:
                json.dump(default_prices, f, indent=4)
                
        # Setup today's invoice folder
        datenow = datetime.datetime.now().strftime("%d-%b-%Y")
        self.invoice_dir = Path(f"Invoice_{datenow}")
        self.invoice_dir.mkdir(exist_ok=True)
        self.invoice_tracker = self.invoice_dir / "invoice_tracker.txt"

    def load_data(self):
        """Loads items and prices into memory once at startup."""
        try:
            with open(self.items_prices_file, "r") as f:
                self.prices_dict = json.load(f).get("price")
                self.prices_dict["None"] = 0
                self.item_list = list(self.prices_dict.keys())
        except Exception as e:
            messagebox.showerror("Data Error", f"Could not load items/prices: {e}")
            self.prices_dict = {"None": 0}
            self.item_list = ["None"]

    def setup_invoice_number(self):
        """Initializes or reads the current invoice number."""
        if not self.invoice_tracker.exists():
            with open(self.invoice_tracker, "w") as f:
                f.write("1")
            self.current_inv_num = 1
        else:
            with open(self.invoice_tracker, "r") as f:
                try:
                    self.current_inv_num = int(f.read().strip())
                except ValueError:
                    self.current_inv_num = 1

    def format_invoice_num(self, num):
        return f"{num:04d}"

    def build_ui(self):
        """Constructs the UI using the grid layout manager."""
        # Top Frame (Header)
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill="x", padx=20)

        tk.Label(top_frame, text="Invoice No:", font=("Garamond", 14, "bold")).grid(row=0, column=0, sticky="w")
        tk.Entry(top_frame, textvariable=self.invoice_var, state="readonly", font=("Georgia", 14), width=8).grid(row=0, column=1, padx=10)

        tk.Label(top_frame, text="Customer Name:", font=("Garamond", 14)).grid(row=1, column=0, sticky="w", pady=15)
        tk.Entry(top_frame, textvariable=self.cname_var, font=("Georgia", 14), width=30).grid(row=1, column=1, padx=10)

        # Main Grid Frame (Items)
        mid_frame = tk.Frame(self.root)
        mid_frame.pack(fill="both", expand=True, padx=20)

        # Column Headers
        headers = ["Item Name", "Price (₹)", "Quantity", "Amount (₹)"]
        for col, text in enumerate(headers):
            tk.Label(mid_frame, text=text, font=("Corbel", 14, "bold")).grid(row=0, column=col+1, padx=10, pady=10)

        # Generate 6 Rows Dynamically
        for i in range(self.max_items):
            tk.Label(mid_frame, text=f"Item {i+1}:", font=("Garamond", 13)).grid(row=i+1, column=0, sticky="e", pady=5)
            
            # Combobox instead of OptionMenu
            cb = ttk.Combobox(mid_frame, textvariable=self.item_vars[i], values=self.item_list, font=("Helvetica", 12), width=20, state="readonly")
            cb.grid(row=i+1, column=1, padx=10, pady=5)
            
            tk.Entry(mid_frame, textvariable=self.price_vars[i], font=("Georgia", 13), width=10, justify="center", state="readonly").grid(row=i+1, column=2, padx=10)
            tk.Entry(mid_frame, textvariable=self.qty_vars[i], font=("Georgia", 13), width=10, justify="center", bg="#D9FFF2").grid(row=i+1, column=3, padx=10)
            tk.Entry(mid_frame, textvariable=self.amount_vars[i], font=("Arial", 13, "bold"), width=12, justify="center", state="readonly").grid(row=i+1, column=4, padx=10)

        # Bottom Frame (Buttons & Total)
        bot_frame = tk.Frame(self.root, pady=20)
        bot_frame.pack(fill="x", padx=20)

        tk.Button(bot_frame, text="Calculate", command=self.calculate, bg="#BEEDA7", font=("Corbel", 14, "bold"), width=12).pack(side="left", padx=10)
        tk.Button(bot_frame, text="Reset", command=self.reset, bg="#FFCDC7", font=("Corbel", 14, "bold"), width=12).pack(side="left", padx=10)
        tk.Button(bot_frame, text="Save Invoice", command=self.save_invoice, bg="#FEFFF3", font=("Corbel", 14, "bold"), width=15).pack(side="left", padx=10)

        tk.Label(bot_frame, text="Total (₹):", font=("Corbel", 14, "bold")).pack(side="left", padx=(40, 5))
        tk.Entry(bot_frame, textvariable=self.total_var, font=("Arial", 16, "bold"), width=12, justify="center", state="readonly").pack(side="left")

    def calculate(self):
        """Calculates prices and amounts based on selections."""
        total = 0.0
        has_items = False

        for i in range(self.max_items):
            item = self.item_vars[i].get()
            
            if item and item != "None":
                has_items = True
                # Fetch price from dictionary
                price = self.prices_dict.get(item, 0.0)
                self.price_vars[i].set(price)
                
                try:
                    qty = self.qty_vars[i].get()
                except tk.TclError:
                    qty = 0 # Handle empty/invalid quantity input
                    self.qty_vars[i].set(0)

                amount = price * qty
                self.amount_vars[i].set(amount)
                total += amount
            else:
                self.price_vars[i].set(0.0)
                self.amount_vars[i].set(0.0)

        self.total_var.set(total)

        if not has_items:
            messagebox.showwarning("No Items", "Please select at least one item to calculate.")

    def reset(self):
        """Clears all fields."""
        self.cname_var.set("")
        self.total_var.set(0.0)
        for i in range(self.max_items):
            self.item_vars[i].set("None")
            self.price_vars[i].set(0.0)
            self.qty_vars[i].set(0)
            self.amount_vars[i].set(0.0)

    def save_invoice(self):
        """Saves the invoice to a text file."""
        self.calculate() # Ensure values are up to date
        
        if self.total_var.get() == 0:
            messagebox.showerror("Error", "Cannot save an empty invoice.")
            return
        if not self.cname_var.get().strip():
            messagebox.showerror("Error", "Customer name is required.")
            return

        if messagebox.askyesno("Confirm", "Do you really want to save this bill?"):
            customer = self.cname_var.get().strip()
            inv_num_str = self.format_invoice_num(self.current_inv_num)
            
            invoice_text = f"Invoice No. - {inv_num_str}, Customer Name - {customer}\n"
            invoice_text += "-" * 50 + "\nItems:\n"
            
            for i in range(self.max_items):
                item = self.item_vars[i].get()
                if item and item != "None":
                    price = self.price_vars[i].get()
                    qty = self.qty_vars[i].get()
                    amt = self.amount_vars[i].get()
                    invoice_text += f"{item:15} (₹{price} x {qty}) = ₹{amt}\n"
            
            invoice_text += "-" * 50 + f"\nTotal Amount = ₹{self.total_var.get()}\n"

            # Save file
            file_path = self.invoice_dir / f"{inv_num_str}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(invoice_text)

            # Increment Tracker
            self.current_inv_num += 1
            with open(self.invoice_tracker, "w") as f:
                f.write(str(self.current_inv_num))
            
            # Update UI for next bill
            self.invoice_var.set(self.format_invoice_num(self.current_inv_num))
            self.reset()
            messagebox.showinfo("Success", f"Invoice {inv_num_str} saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()