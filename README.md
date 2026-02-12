# QuickBill-Py
A lightweight, GUI-based desktop application designed to streamline the billing process for small businesses and wholesale shopkeepers. Many local vendors struggle with manual bookkeeping; this app automates invoice generation by pulling inventory data from a structured JSON file, allowing for quick, error-free transactions.

## Features
- **Automated Inventory Loading**: Reads items and pricing directly from a JSON configuration file for easy updates.
- **Smart Quantity Handling**: Supports custom quantities for each item, defaulting to 1 for rapid entry.
- **Sequential Invoice Tracking**: Automatically increments invoice numbers to ensure record consistency.
- **Dynamic File Organization**: Generates and saves text-based invoices into auto-generated folders organized by Date, Month, and Year.
- **Zero-Config Timestamping**: Uses system time to timestamp every bill automatically, reducing manual data entry.

## Required Packages 💻
- **Tkinter**: For the graphical user interface.
- **JSON**: For persistent data storage of items and prices.
- **OS & Datetime**: For automated file system management and time-stamping.
  
🚀 Future Roadmap
While the current version meets all immediate requirements for local shop management, potential future enhancements could include:
- Export to PDF: Converting .txt invoices into professional PDF formats.
- Analytics Dashboard: A simple view to track daily or monthly sales totals.
- SQLite Integration: For handling larger inventories more efficiently.

