import os, sys

# Works for both normal run and packaged (.exe/.app)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")
EXPORTS_PATH = os.path.join(BASE_DIR, "exports")

# Auto-create folders
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(EXPORTS_PATH, exist_ok=True)
