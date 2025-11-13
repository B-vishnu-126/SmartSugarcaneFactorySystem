import os
import sys
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from modules import farmer_operations as f
from modules import delivery_operations as d
from modules.payment_calculation import calculate_payments
from modules.export_payments import export_payments_to_excel
from modules.export_pdf import export_payments_to_pdf

# ============================================================
# 🧩 PATH DETECTION (works for both .py and macOS .app)
# ============================================================

def get_base_dir():
    """Detect correct base directory for both .py and .app modes."""
    if getattr(sys, 'frozen', False):  # running inside .app
        app_path = os.path.dirname(sys.executable)
        base_dir = os.path.abspath(os.path.join(app_path, "../../.."))
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    return base_dir

BASE_DIR = get_base_dir()
DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")

# Auto-create required folders
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

print("📂 BASE_DIR:", BASE_DIR)
print("📁 Database:", DB_PATH)
print("📁 Exports:", EXPORTS_DIR)

# ============================================================
# 🧩 MAIN WINDOW
# ============================================================

root = ttk.Window(themename="cosmo")
root.title("🌾 Smart Sugarcane Factory Management System | DSOFT TECHNO SYSTEMS")
root.geometry("1000x750")

title_label = ttk.Label(
    root,
    text="🌾 Smart Sugarcane Factory Management System",
    font=("Helvetica", 22, "bold"),
    bootstyle="primary"
)
title_label.pack(fill=X, pady=15)

# ============================================================
# 🧩 DASHBOARD
# ============================================================

dashboard_frame = ttk.Frame(root, padding=10)
dashboard_frame.pack(fill=X, padx=10, pady=5)

farmer_card = ttk.Label(dashboard_frame, text="👨‍🌾 Total Farmers: 0", font=("Helvetica", 14, "bold"), bootstyle="success")
delivery_card = ttk.Label(dashboard_frame, text="🚚 Total Deliveries: 0", font=("Helvetica", 14, "bold"), bootstyle="info")
payment_card = ttk.Label(dashboard_frame, text="💰 Total Payment ₹: 0", font=("Helvetica", 14, "bold"), bootstyle="warning")

farmer_card.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")
delivery_card.grid(row=0, column=1, padx=15, pady=5, sticky="nsew")
payment_card.grid(row=0, column=2, padx=15, pady=5, sticky="nsew")
dashboard_frame.columnconfigure((0, 1, 2), weight=1)

# ============================================================
# 🧩 FARMER SECTION
# ============================================================

frame1 = ttk.Labelframe(root, text="👨‍🌾 Farmer Registration", padding=15, bootstyle="info")
frame1.pack(fill=X, padx=15, pady=10)

ttk.Label(frame1, text="Name:", font=("Helvetica", 11)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
ttk.Label(frame1, text="Phone:", font=("Helvetica", 11)).grid(row=0, column=2, padx=5, pady=5, sticky=W)
ttk.Label(frame1, text="Village:", font=("Helvetica", 11)).grid(row=0, column=4, padx=5, pady=5, sticky=W)

name_entry = ttk.Entry(frame1, width=20)
phone_entry = ttk.Entry(frame1, width=20)
village_entry = ttk.Entry(frame1, width=20)

name_entry.grid(row=0, column=1, padx=5, pady=5)
phone_entry.grid(row=0, column=3, padx=5, pady=5)
village_entry.grid(row=0, column=5, padx=5, pady=5)

def add_farmer():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    village = village_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Farmer name cannot be empty.")
        return

    f.add_farmer(name, phone, village)
    messagebox.showinfo("Success", f"✅ Farmer '{name}' added successfully!")
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    village_entry.delete(0, END)
    update_dashboard()

ttk.Button(frame1, text="Add Farmer", bootstyle="success-outline", width=18, command=add_farmer).grid(row=0, column=6, padx=15)

# ============================================================
# 🧩 DELIVERY SECTION
# ============================================================

frame2 = ttk.Labelframe(root, text="🚚 Delivery Entry", padding=15, bootstyle="success")
frame2.pack(fill=X, padx=15, pady=10)

ttk.Label(frame2, text="Farmer ID:", font=("Helvetica", 11)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
ttk.Label(frame2, text="Weight (tons):", font=("Helvetica", 11)).grid(row=0, column=2, padx=5, pady=5, sticky=W)
ttk.Label(frame2, text="Rate per ton (₹):", font=("Helvetica", 11)).grid(row=0, column=4, padx=5, pady=5, sticky=W)

farmer_id_entry = ttk.Entry(frame2, width=10)
weight_entry = ttk.Entry(frame2, width=10)
rate_entry = ttk.Entry(frame2, width=10)

farmer_id_entry.grid(row=0, column=1, padx=5, pady=5)
weight_entry.grid(row=0, column=3, padx=5, pady=5)
rate_entry.grid(row=0, column=5, padx=5, pady=5)

def add_delivery():
    try:
        fid = int(farmer_id_entry.get())
        weight = float(weight_entry.get())
        rate = float(rate_entry.get())
        d.add_delivery(fid, weight, rate)
        messagebox.showinfo("Success", "✅ Delivery recorded successfully!")
        load_deliveries()
        update_dashboard()
        farmer_id_entry.delete(0, END)
        weight_entry.delete(0, END)
        rate_entry.delete(0, END)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for ID, Weight, and Rate.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

ttk.Button(frame2, text="Add Delivery", bootstyle="primary-outline", width=18, command=add_delivery).grid(row=0, column=6, padx=15)

# ============================================================
# 🧩 DELIVERY TABLE
# ============================================================

frame3 = ttk.Labelframe(root, text="📋 All Deliveries", padding=15, bootstyle="secondary")
frame3.pack(fill=BOTH, expand=True, padx=15, pady=15)

cols = ("ID", "Farmer Name", "Village", "Weight (tons)", "Rate", "Payment", "Date")
tree = ttk.Treeview(frame3, columns=cols, show="headings", height=15, bootstyle="info")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.pack(fill=BOTH, expand=True)

# ============================================================
# 🧩 DASHBOARD LOGIC
# ============================================================

def get_summary_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM farmers;")
        total_farmers = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM deliveries;")
        total_deliveries = cursor.fetchone()[0]
        cursor.execute("SELECT IFNULL(SUM(payment), 0) FROM deliveries;")
        total_payment = cursor.fetchone()[0]
        conn.close()
        return total_farmers, total_deliveries, total_payment
    except Exception as e:
        print("❌ Dashboard Error:", e)
        return 0, 0, 0

def update_dashboard():
    total_farmers, total_deliveries, total_payment = get_summary_data()
    farmer_card.config(text=f"👨‍🌾 Total Farmers: {total_farmers}")
    delivery_card.config(text=f"🚚 Total Deliveries: {total_deliveries}")
    payment_card.config(text=f"💰 Total Payment ₹: {total_payment:.2f}")

def load_deliveries():
    for row in tree.get_children():
        tree.delete(row)
    deliveries = d.view_deliveries()
    for index, row in enumerate(deliveries):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=row, tags=(tag,))
    update_dashboard()

# ============================================================
# 🧩 SEARCH / VIEW FARMERS / DELETE FUNCTIONS
# ============================================================

def open_search_popup():
    popup = ttk.Toplevel(root)
    popup.title("🔍 Search Farmer")
    popup.geometry("400x300")
    popup.resizable(False, False)

    ttk.Label(popup, text="Search Farmer by Name or ID", font=("Helvetica", 13, "bold"), bootstyle="primary").pack(pady=10)
    search_entry = ttk.Entry(popup, width=30)
    search_entry.pack(pady=10)

    result_box = ttk.Treeview(popup, columns=("ID", "Name", "Phone", "Village"), show="headings", height=5, bootstyle="info")
    for col in ("ID", "Name", "Phone", "Village"):
        result_box.heading(col, text=col)
        result_box.column(col, anchor="center", width=80)
    result_box.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def search_farmer():
        keyword = search_entry.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Please enter a name or ID to search.")
            return
        farmers = f.view_farmers()
        results = [farmer for farmer in farmers if keyword.lower() in farmer[1].lower() or str(farmer[0]) == keyword]

        for row in result_box.get_children():
            result_box.delete(row)
        for row in results:
            result_box.insert("", "end", values=row)
        if not results:
            messagebox.showinfo("Not Found", "No farmer found with that name or ID.")

    ttk.Button(popup, text="Search", bootstyle="primary-outline", command=search_farmer).pack(pady=5)

def view_all_farmers_popup():
    popup = ttk.Toplevel(root)
    popup.title("👨‍🌾 All Farmers | DSOFT TECHNO SYSTEMS")
    popup.geometry("550x400")
    popup.resizable(False, False)

    ttk.Label(popup, text="👨‍🌾 Registered Farmers List", font=("Helvetica", 14, "bold"), bootstyle="primary").pack(pady=10)

    cols = ("ID", "Name", "Phone", "Village")
    farmer_table = ttk.Treeview(popup, columns=cols, show="headings", height=10, bootstyle="info")
    for col in cols:
        farmer_table.heading(col, text=col)
        farmer_table.column(col, anchor="center", width=120)
    farmer_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(popup, orient="vertical", command=farmer_table.yview)
    farmer_table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    farmers = f.view_farmers()
    if not farmers:
        messagebox.showinfo("Info", "No farmers found in the database.")
        popup.destroy()
        return
    for farmer in farmers:
        farmer_table.insert("", "end", values=farmer)

    ttk.Button(popup, text="Close", bootstyle="secondary-outline", command=popup.destroy).pack(pady=10)

def delete_selected_delivery():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a delivery to delete.")
        return
    selected_row = tree.item(selected_item)["values"]
    delivery_id = selected_row[0]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Delivery ID {delivery_id}?")
    if confirm:
        d.delete_delivery(delivery_id)
        messagebox.showinfo("Deleted", f"🗑️ Delivery ID {delivery_id} deleted successfully!")
        load_deliveries()

# ============================================================
# 🧩 ACTION BUTTONS
# ============================================================

action_frame = ttk.Frame(root, padding=10)
action_frame.pack(pady=10)

def calculate_payments_gui():
    popup = ttk.Toplevel(root)
    popup.title("💰 Enter Rate per Ton")
    popup.geometry("300x180")
    popup.resizable(False, False)

    ttk.Label(popup, text="Enter Rate per Ton (₹):", font=("Helvetica", 12)).pack(pady=15)
    rate_input = ttk.Entry(popup, width=15)
    rate_input.insert(0, "3200")
    rate_input.pack(pady=5)

    def confirm_rate():
        try:
            rate = float(rate_input.get())
            popup.destroy()
            calculate_payments(rate)
            messagebox.showinfo("Success", f"✅ Payments calculated successfully at ₹{rate}/ton.")
            update_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid rate.")

    ttk.Button(popup, text="Calculate", bootstyle="warning", command=confirm_rate).pack(pady=10)

def export_payments_gui():
    try:
        export_payments_to_excel()
        messagebox.showinfo("Export", "✅ Payment report exported successfully to Excel!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_pdf_gui():
    try:
        path = export_payments_to_pdf()
        if path:
            messagebox.showinfo("PDF Export", f"✅ PDF exported successfully!\n\nSaved at:\n{path}")
        else:
            messagebox.showwarning("No Data", "No payment data found to export.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Buttons Layout
ttk.Button(action_frame, text="💰 Calculate Payments", bootstyle="warning-outline", width=20, command=calculate_payments_gui).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(action_frame, text="📤 Export to Excel", bootstyle="success-outline", width=20, command=export_payments_gui).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(action_frame, text="🧾 Export PDF Report", bootstyle="danger-outline", width=20, command=export_pdf_gui).grid(row=0, column=2, padx=10, pady=5)
ttk.Button(action_frame, text="🔍 Search Farmer", bootstyle="primary-outline", width=20, command=open_search_popup).grid(row=1, column=0, padx=10, pady=5)
ttk.Button(action_frame, text="🗑️ Delete Delivery", bootstyle="danger-outline", width=20, command=delete_selected_delivery).grid(row=1, column=1, padx=10, pady=5)
ttk.Button(action_frame, text="🔄 Refresh Data", bootstyle="info-outline", width=20, command=load_deliveries).grid(row=1, column=2, padx=10, pady=5)
ttk.Button(action_frame, text="👨‍🌾 View Farmers", bootstyle="success-outline", width=20, command=view_all_farmers_popup).grid(row=2, column=1, padx=10, pady=5)

# ============================================================
# 🏢 FOOTER BRANDING
# ============================================================

footer = ttk.Label(
    root,
    text="© 2025 DSOFT TECHNO SYSTEMS | All Rights Reserved",
    font=("Helvetica", 10, "italic"),
    bootstyle="secondary"
)
footer.pack(side=BOTTOM, pady=5)

# ============================================================
# 🧩 STARTUP
# ============================================================

load_deliveries()
update_dashboard()
root.mainloop()
