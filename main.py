from modules.payment_calculation import calculate_payments
from modules.export_payments import export_payments_to_excel

if __name__ == "__main__":
    print("=== Sugarcane Factory Payment System ===")

    # Ask the factory owner to input rate per ton
    rate = float(input("Enter rate per ton (₹): "))

    # Step 1: Calculate and store payments in database
    calculate_payments(rate)

    # Step 2: Export all payments to Excel file
    print("\nNow exporting payment report to Excel...")
    export_payments_to_excel()

    print("\n Payment calculation and Excel export complete!")
