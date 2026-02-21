import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
from pathlib import Path
import sqlite3 as sql

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.title("QuickBill-Py: Modern Invoice")
        
        # --- App Data Setup ---
        self.setup_directories()
        self.setup_database()
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
        self.comboboxes = [] # To keep track of dropdowns for real-time updates

        self.build_ui()

    def setup_directories(self):
        """Creates the daily folder for text file receipts."""
        datenow = datetime.datetime.now().strftime("%d-%b-%Y")
        self.invoice_dir = Path(f"Invoice_{datenow}")
        self.invoice_dir.mkdir(exist_ok=True)

    def setup_database(self):
        """Connects to SQLite and creates necessary tables."""
        self.db_name = "quickbill.db"
        self.db = sql.connect(self.db_name) 
        cursor = self.db.cursor()
        
        try:
            # Create Items Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items(
                    name TEXT PRIMARY KEY,
                    price REAL NOT NULL
                );
            ''')
            
            # Create Invoices Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER NOT NULL,
                    customer_name TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL
                );
            ''')
            
            # Check if items table is empty; if so, add default items
            cursor.execute("SELECT COUNT(*) FROM items")
            if cursor.fetchone()[0] == 0:
                default_items = [("Apple", 20.0), ("Banana", 10.0), ("Milk", 50.0), ("Bread", 40.0)]
                cursor.executemany("INSERT INTO items (name, price) VALUES (?, ?)", default_items)
            
            self.db.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to setup database: {e}")

    def load_data(self):
        """Loads items and prices from SQLite into memory."""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT name, price FROM items ORDER BY name ASC")
            
            self.prices_dict = {"None": 0.0}
            self.item_list = ["None"]
            
            for name, price in cursor.fetchall():
                self.prices_dict[name] = price
                self.item_list.append(name)
                
            # If the UI is already built, update the combobox dropdowns in real-time
            if hasattr(self, 'comboboxes'):
                for cb in self.comboboxes:
                    cb['values'] = self.item_list
                    
        except Exception as e:
            messagebox.showerror("Data Error", f"Could not load items from database: {e}")
            self.prices_dict = {"None": 0.0}
            self.item_list = ["None"]

    def setup_invoice_number(self):
        """Fetches the highest invoice number from the database to determine the next one."""
        cursor = self.db.cursor()
        cursor.execute("SELECT MAX(invoice_id) FROM invoices")
        result = cursor.fetchone()[0]
        
        if result is None:
            self.current_inv_num = 1
        else:
            self.current_inv_num = result + 1

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

        headers = ["Item Name", "Price (₹)", "Quantity", "Amount (₹)"]
        for col, text in enumerate(headers):
            tk.Label(mid_frame, text=text, font=("Corbel", 14, "bold")).grid(row=0, column=col+1, padx=10, pady=10)

        for i in range(self.max_items):
            tk.Label(mid_frame, text=f"Item {i+1}:", font=("Garamond", 13)).grid(row=i+1, column=0, sticky="e", pady=5)
            
            cb = ttk.Combobox(mid_frame, textvariable=self.item_vars[i], values=self.item_list, font=("Helvetica", 12), width=20, state="readonly")
            cb.grid(row=i+1, column=1, padx=10, pady=5)
            self.comboboxes.append(cb)
            
            tk.Entry(mid_frame, textvariable=self.price_vars[i], font=("Georgia", 13), width=10, justify="center", state="readonly").grid(row=i+1, column=2, padx=10)
            tk.Entry(mid_frame, textvariable=self.qty_vars[i], font=("Georgia", 13), width=10, justify="center", bg="#D9FFF2").grid(row=i+1, column=3, padx=10)
            tk.Entry(mid_frame, textvariable=self.amount_vars[i], font=("Arial", 13, "bold"), width=12, justify="center", state="readonly").grid(row=i+1, column=4, padx=10)

        # Bottom Frame (Buttons & Total)
        bot_frame = tk.Frame(self.root, pady=20)
        bot_frame.pack(fill="x", padx=20)

        tk.Button(bot_frame, text="Manage Inventory", command=self.open_inventory_window, bg="#D9FEFF", font=("Corbel", 13, "bold"), width=15).pack(side="left", padx=5)
        tk.Button(bot_frame, text="Calculate", command=self.calculate, bg="#BEEDA7", font=("Corbel", 13, "bold"), width=10).pack(side="left", padx=5)
        tk.Button(bot_frame, text="Reset", command=self.reset, bg="#FFCDC7", font=("Corbel", 13, "bold"), width=10).pack(side="left", padx=5)
        tk.Button(bot_frame, text="Save Invoice", command=self.save_invoice, bg="#FEFFF3", font=("Corbel", 13, "bold"), width=12).pack(side="left", padx=5)

        tk.Label(bot_frame, text="Total (₹):", font=("Corbel", 14, "bold")).pack(side="left", padx=(30, 5))
        tk.Entry(bot_frame, textvariable=self.total_var, font=("Arial", 16, "bold"), width=12, justify="center", state="readonly").pack(side="left")

    def calculate(self):
        """Calculates prices and amounts based on selections."""
        total = 0.0
        has_items = False

        for i in range(self.max_items):
            item = self.item_vars[i].get()
            
            if item and item != "None":
                has_items = True
                price = self.prices_dict.get(item, 0.0)
                self.price_vars[i].set(price)
                
                try:
                    qty = self.qty_vars[i].get()
                except tk.TclError:
                    qty = 0
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
        """Saves the invoice to the SQLite database and a text file."""
        self.calculate()
        
        if self.total_var.get() == 0:
            messagebox.showerror("Error", "Cannot save an empty invoice.")
            return
        if not self.cname_var.get().strip():
            messagebox.showerror("Error", "Customer name is required.")
            return

        if messagebox.askyesno("Confirm", "Do you really want to save this bill?"):
            customer = self.cname_var.get().strip()
            inv_num_str = self.format_invoice_num(self.current_inv_num)
            date_str = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
            
            invoice_text = f"Invoice No. - {inv_num_str}, Customer Name - {customer}\n"
            invoice_text += "-" * 50 + "\nItems:\n"
            
            cursor = self.db.cursor()
            
            for i in range(self.max_items):
                item = self.item_vars[i].get()
                if item and item != "None":
                    price = self.price_vars[i].get()
                    qty = self.qty_vars[i].get()
                    amt = self.amount_vars[i].get()
                    
                    invoice_text += f"{item:15} (₹{price} x {qty}) = ₹{amt}\n"
                    
                    cursor.execute('''
                        INSERT INTO invoices (invoice_id, customer_name, item_name, quantity, amount, date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (self.current_inv_num, customer, item, qty, amt, date_str))
            
            invoice_text += "-" * 50 + f"\nTotal Amount = ₹{self.total_var.get()}\n"

            self.db.commit()

            file_path = self.invoice_dir / f"{inv_num_str}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(invoice_text)

            self.current_inv_num += 1
            self.invoice_var.set(self.format_invoice_num(self.current_inv_num))
            
            self.reset()
            messagebox.showinfo("Success", f"Invoice {inv_num_str} saved successfully!")

    def open_inventory_window(self):
        """Opens a separate window to manage items and prices."""
        inv_win = tk.Toplevel(self.root)
        inv_win.title("Manage Inventory")
        inv_win.geometry("500x500")
        inv_win.grab_set() 

        input_frame = tk.LabelFrame(inv_win, text="Add / Update Item", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Item Name:").grid(row=0, column=0, sticky="w")
        name_entry = tk.Entry(input_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Price (₹):").grid(row=1, column=0, sticky="w")
        price_entry = tk.Entry(input_frame)
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        tree_frame = tk.Frame(inv_win)
        tree_frame.pack(fill="both", expand=True, padx=10)

        columns = ("name", "price")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        tree.heading("name", text="Item Name")
        tree.heading("price", text="Price (₹)")
        tree.column("price", width=100, anchor="center")
        tree.pack(side="left", fill="both", expand=True)

        scroller = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scroller.set)
        scroller.pack(side="right", fill="y")

        def refresh_table():
            for item in tree.get_children():
                tree.delete(item)
            cursor = self.db.cursor()
            cursor.execute("SELECT name, price FROM items ORDER BY name ASC")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        def save_item():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            if not name or not price:
                messagebox.showwarning("Input Error", "Both fields are required!", parent=inv_win)
                return
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO items (name, price) VALUES (?, ?)
                    ON CONFLICT(name) DO UPDATE SET price=excluded.price
                """, (name, float(price)))
                self.db.commit()
                name_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                refresh_table()
                self.load_data() 
            except ValueError:
                messagebox.showerror("Error", "Price must be a number!", parent=inv_win)

        def delete_item():
            selected = tree.selection()
            if not selected:
                return
            item_name = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Confirm", f"Delete {item_name} from inventory?", parent=inv_win):
                cursor = self.db.cursor()
                cursor.execute("DELETE FROM items WHERE name = ?", (item_name,))
                self.db.commit()
                refresh_table()
                self.load_data()

        btn_frame = tk.Frame(inv_win)
        btn_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="Save / Update", command=save_item, bg="#BEEDA7").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=delete_item, bg="#FFCDC7").pack(side="left", padx=5)

        refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()