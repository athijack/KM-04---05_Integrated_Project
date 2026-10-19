"""
main.py
--------
Entry point for Thabo's Corner Store — Sales Insights System.

Run with:
    python main.py

This file ties together all five modules in the correct order:
    data_cleaning -> database -> analysis -> visualize -> security
"""

import os

import data_cleaning
import database
import analysis
import visualize
import security

DATA_DIR = os.path.join("..", "data")   # one level up from starter_code/
PRODUCTS_CSV = os.path.join(DATA_DIR, "products.csv")
SALES_CSV = os.path.join(DATA_DIR, "sales.csv")
DB_PATH = "store.db"


def main():
    print("=" * 60)
    print("  Thabo's Corner Store — Sales Insights System")
    print("=" * 60)

    # ---- Task 6: security gate -------------------------------------
    # Uncomment the block below to require a password before reports load.
    # Password: spaza2026
    #
    # if not security.login_gate(security.STORED_PASSWORD_HASH):
    #     return

    # ---- Task 2: load & clean data ----------------------------------
    print("\n[1/5] Loading raw data...")
    raw_products, raw_sales = data_cleaning.load_raw_data(PRODUCTS_CSV, SALES_CSV)
    print(f"  Loaded {len(raw_products)} raw product rows and "
          f"{len(raw_sales)} raw sales rows.")

    print("\n[2/5] Cleaning data...")
    clean_products = data_cleaning.clean_products(raw_products)
    valid_ids = clean_products["product_id"].tolist()
    clean_sales = data_cleaning.clean_sales(raw_sales, valid_product_ids=valid_ids)
    print(" ", data_cleaning.cleaning_summary(raw_products, clean_products, "products"))
    print(" ", data_cleaning.cleaning_summary(raw_sales, clean_sales, "sales"))

    # ---- Task 3: build the database ---------------------------------
    print("\n[3/5] Building database...")
    conn = database.get_connection(DB_PATH)
    database.create_tables(conn)
    database.insert_products(conn, clean_products)
    database.insert_sales(conn, clean_sales)
    print(f"  Database saved to: {DB_PATH}")

    print("\n  --- SQL Query Results ---")

    print("\n  Query 1: Total revenue per product:")
    for row in database.query_total_revenue_per_product(conn):
        print(f"    {row[0]:<35} R{row[1]:>8,.2f}")

    print("\n  Query 2: Best-selling product (units):")
    for row in database.query_best_selling_product(conn):
        print(f"    {row[0]} — {row[1]} units")

    print("\n  Query 3: Sales by payment method:")
    for row in database.query_sales_by_payment_method(conn):
        print(f"    {row[0]:<15} {row[1]} transactions")

    print("\n  Query 4 (custom): Revenue per category:")
    for row in database.query_custom_one(conn):
        print(f"    {row[0]:<25} R{row[1]:>8,.2f}")

    print("\n  Query 5 (custom): Monthly revenue trend:")
    for row in database.query_custom_two(conn):
        print(f"    {row[0]}  R{row[1]:>8,.2f}")

    # ---- Task 4: programming logic / analysis -----------------------
    print("\n[4/5] Running analysis...")
    sales_records = clean_sales.to_dict("records")
    products_records = clean_products.to_dict("records")

    print(f"  Total sales records  : {analysis.total_sales_records(sales_records)}")

    alerts = analysis.low_stock_alert(products_records)
    if alerts:
        print(f"  Low stock alerts ({len(alerts)}): {', '.join(alerts)}")
    else:
        print("  Low stock alerts: none")

    trend = analysis.monthly_sales_trend(sales_records)
    print(f"  Monthly trend        : {trend}")
    print(f"  Average basket size  : {analysis.average_basket_size(sales_records)} units")

    # Demonstrate classify_transaction_size
    print("\n  Transaction size classification examples:")
    for qty in [1, 2, 5, 10]:
        label = analysis.classify_transaction_size(qty)
        print(f"    quantity={qty} -> {label}")

    # ---- Task 5: visualisation ---------------------------------------
    print("\n[5/5] Generating charts...")
    revenue_rows = database.query_total_revenue_per_product(conn)
    names = [r[0] for r in revenue_rows]
    revenues = [r[1] for r in revenue_rows]
    visualize.bar_chart_revenue_per_product(names, revenues)
    visualize.line_chart_monthly_trend(trend)

    conn.close()

    print("\n" + "=" * 60)
    print("  Done! All tasks completed successfully.")
    print("  Charts saved in starter_code/")
    print("  Database saved as starter_code/store.db")
    print("  Don't forget to commit and push to GitHub!")
    print("=" * 60)


if __name__ == "__main__":
    main()
