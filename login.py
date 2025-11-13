import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from modules.auth_operations import verify_user
import subprocess

# 🧭 Base directory (works for normal + .app build)
def get_base_dir():
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
        base_dir = os.path.abspath(os.path.join(app_path, "../../.."))
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    return base_dir

BASE_DIR = get_base_dir()

# ------------------------------------------------------------
# 🧩 LOGIN WINDOW
# ------------------------------------------------------------
root = ttk.Window(themename="cosmo")
root.title("🔐 DSOFT | Smart Sugarcane Factory Login")
root.geometry("400x350")

ttk.Label(
    root, 
    text="🌾 Smart Sugarcane Factory System", 
    font=("Helvetica", 16, "bold"), 
    bootstyle="primary"
).pack(pady=20)

# ------------------------------------------------------------
# 🧩 Username and Password Fields
# ------------------------------------------------------------
ttk.Label(root, text="Username:", font=("Helvetica", 12)).pack(pady=(10, 5))
username_entry = ttk.Entry(root, width=25)
username_entry.pack()

ttk.Label(root, text="Password:", font=("Helvetica", 12)).pack(pady=(15, 5))
password_entry = ttk.Entry(root, show="*", width=25)
password_entry.pack()

# ------------------------------------------------------------
# 🧩 Login Function
# ------------------------------------------------------------
def login_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    valid, result = verify_user(username, password)

    if valid:
        messagebox.showinfo("Welcome", f"✅ Login successful! Role: {result}")
        root.destroy()  # Close login window
        
        # Launch main app
        main_app_path = os.path.join(BASE_DIR, "app.py")
        subprocess.Popen(["python3", main_app_path])
    else:
        messagebox.showerror("Login Failed", result)

# ------------------------------------------------------------
# 🧩 Buttons
# ------------------------------------------------------------
ttk.Button(root, text="Login", width=20, bootstyle="success", command=login_user).pack(pady=20)
ttk.Button(root, text="Exit", width=20, bootstyle="danger", command=root.destroy).pack()

# ------------------------------------------------------------
# 🧩 Footer
# ------------------------------------------------------------
ttk.Label(
    root,
    text="© 2025 DSOFT TECHNO SYSTEMS",
    font=("Helvetica", 10, "italic"),
    bootstyle="secondary"
).pack(side="bottom", pady=10)

root.mainloop()
