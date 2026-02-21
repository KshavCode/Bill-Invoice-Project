## 📲 Download
[![Latest Release](https://img.shields.io/github/v/release/KshavCode/quickbill-py?include_prereleases&label=Latest%20APK&color=blue)](https://github.com/KshavCode/quickbill-py/releases/latest)

# QuickBill-Py
A lightweight, GUI-based desktop application designed to streamline the billing process for small businesses and wholesale shopkeepers. Many local vendors struggle with manual bookkeeping; this app automates invoice generation by utilizing a local SQLite database for robust inventory management and secure transaction history, allowing for quick, error-free, and trackable sales.

## Features
- **Database-Driven Inventory:** Reads items and pricing directly from a lightweight, serverless SQLite database, making price updates and inventory management instantaneous and reliable.
- **Secure Transaction History:** All generated invoices are permanently logged in the database, preventing accidental data loss and making future sales queries easy.
- **Sequential Invoice Tracking**: Automatically increments invoice numbers to ensure record consistency.
- **Smart Quantity Handling:** Supports custom quantities for each item, calculating total amounts on the fly for rapid entry.
- **Sequential Invoice Tracking:** Automatically increments invoice numbers using database relations to ensure strict bookkeeping consistency.
- **Dynamic File Organization:** Alongside database logging, it generates and saves text-based invoice receipts into auto-generated folders organized by Date, Month, and Year.
- **Zero-Config Timestamping:** Uses system time to timestamp every bill automatically, reducing manual data entry.

## Required Packages 💻
- **Tkinter**: For the graphical user interface.
- **SQLite3**: Python's built-in library for secure, serverless database management (ACID compliant).
- **OS & Datetime:** For automated file system management and time-stamping.
- **Pathlib:** For modern, cross-platform file path handling.
  
🚀 Future Roadmap
With data now securely structured in a database, the foundation is set for advanced features:
- **Export to PDF:** Upgrading the text-based receipts into professional, branded PDF formats (using ReportLab or FPDF).
- **Analytics Dashboard:** Leveraging SQL queries to create a visual dashboard tracking daily/monthly sales totals and identifying best-selling items.
- **Customer Database:** Storing frequent customer details to auto-fill information on future visits.

