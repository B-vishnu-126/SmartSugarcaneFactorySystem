import os
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_payments_to_pdf():
    """
    Exports a professional PDF report of all farmer payments
    with DSOFT TECHNO SYSTEMS branding.
    """
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = os.path.join(BASE_DIR, "database", "farmers.db")
    EXPORT_DIR = os.path.join(BASE_DIR, "exports")
    os.makedirs(EXPORT_DIR, exist_ok=True)

    pdf_path = os.path.join(EXPORT_DIR, "payments_report.pdf")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT f.name, f.village, ROUND(p.total_weight,2), 
           p.rate_per_ton, p.deductions, ROUND(p.total_amount,2), p.payment_date
    FROM payments p
    JOIN farmers f ON f.farmer_id = p.farmer_id
    ORDER BY f.name;
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("⚠️ No payment data found for PDF export.")
        return None

    # Start PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkgreen)
    c.drawCentredString(width / 2, height - 60, "🌾 SMART SUGARCANE FACTORY SYSTEM")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 80, "Powered by DSOFT TECHNO SYSTEMS")

    c.line(40, height - 90, width - 40, height - 90)

    # Date
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 105, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    # Table Header
    table_data = [
        ["Farmer Name", "Village", "Total (Ton)", "Rate/Ton", "Deductions", "Total ₹", "Date"]
    ]

    # Add rows
    total_sum = 0
    for row in data:
        name, village, weight, rate, ded, total, date = row
        total_sum += total
        table_data.append([
            name, village, str(weight), f"{rate:.2f}", f"{ded:.2f}", f"{total:.2f}", date
        ])

    # Add Grand Total Row
    table_data.append(["", "", "", "", "Grand Total:", f"{total_sum:.2f}", ""])

    # Table Styling
    table = Table(table_data, colWidths=[90, 80, 70, 60, 70, 70, 70])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.limegreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey]),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (4, -1), (5, -1), colors.lightgreen)
    ]))

    # Place table
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, height - 500)

    # Signature section
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(60, 100, "_________________________")
    c.drawString(80, 85, "Factory Manager Signature")

    # Footer
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, 60, "© 2025 DSOFT TECHNO SYSTEMS | All Rights Reserved")

    c.save()
    print(f"✅ PDF report exported successfully: {pdf_path}")
    return pdf_path
