# 🌾 Smart Sugarcane Factory Management System
### Developed by **DSOFT TECHNO SYSTEMS**

A complete end-to-end desktop solution to manage sugarcane factory operations — built with **Python, ttkbootstrap, and SQLite3**.  
This system helps factories streamline **farmer management, delivery tracking, and automated payment calculations** with modern UI and reporting.

---

## 🚀 Features

✅ **Secure Login System** (bcrypt-based password protection)  
✅ **Farmer Management** – Add, search, and view registered farmers  
✅ **Delivery Tracking** – Record sugarcane deliveries by farmer ID and weight  
✅ **Automatic Payment Calculation** – Compute total amounts and export reports  
✅ **Excel Report Export** – Generate formatted Excel reports for all payments  
✅ **PDF Report Export** – Professionally styled PDF with DSOFT branding  
✅ **Interactive Dashboard** – Live totals for farmers, deliveries, and payments  
✅ **Beautiful GUI** using `ttkbootstrap`

---

## 🧰 Technologies Used

| Component | Technology |
|------------|-------------|
| Language | Python 3.13 |
| Database | SQLite3 |
| GUI Framework | ttkbootstrap |
| Reporting | pandas, openpyxl, reportlab |
| Security | bcrypt |
| Packaging | PyInstaller |
| Platform | macOS / Windows Compatible |

---

## 🧩 Folder Structure

FarmerDeliverySystem/
├── app.py                  # Main GUI dashboard
├── login.py                # Login screen
├── modules/                # All helper modules
├── database/farmers.db     # SQLite database
├── exports/                # O/Pfolder(Excel/PDF)
├── README.md               # Project description
└── venv/                   # Virtual environment



---

## 🧱 How to Run the Project

### 1️⃣ Clone this repository
```bash
git clone https://github.com/yourusername/FarmerDeliverySystem.git
cd FarmerDeliverySystem

2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3️⃣ Install required dependencies
pip install -r requirements.txt

4️⃣ Run the login app
python3 login.py


#Default credentials:
Username: admin
Password: 12345

📊 Sample Reports
📘 Excel Report: exports/payments_report.xlsx
📗 PDF Report: exports/payments_report.pdf

🏢 About DSOFT TECHNO SYSTEMS

DSOFT TECHNO SYSTEMS is a software development group focused on building practical and intelligent desktop applications for the agriculture and factory automation industries.

🔖 Copyright

© 2025 DSOFT TECHNO SYSTEMS | All Rights Reserved.
Built with ❤️ by Vishnudas Bhande.


---

Do the same for the “How to Run” section so it stays formatted correctly.

---

### ✅ **2️⃣ Add a Screenshot Preview (optional but powerful)**
You can show your GUI right on the GitHub page:  

```markdown
## 🖥️ Application Preview
![Login Screenshot](exports/Login_preview.png)
![Dashboard Screenshot](exports/dashboard_preview.png)