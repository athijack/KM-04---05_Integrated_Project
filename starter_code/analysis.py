"""
analysis.py
------------
Task 4: Programming logic — functions, loops, conditionals and arrays.

This module covers KM-05 topics: Programming Basics (data types,
conditionals, loops, arrays/lists, functions) and Introduction to
Algorithms.

IMPORTANT: Plain Python is used throughout (for-loops, if/else,
lists and dictionaries) rather than pandas shortcuts, to demonstrate
the KM-05 programming fundamentals.
"""


def total_sales_records(sales_rows: list) -> int:
    """
    Count how many sales records there are using an explicit loop.

    Args:
        sales_rows: a list of dictionaries, one per sale.

    Returns:
        the total number of records as an integer.
    """
    count = 0
    for row in sales_rows:   # loop over every record
        count += 1            # increment for each one
    return count


def low_stock_alert(products_rows: list, threshold: int = 5) -> list:
    """
    Return a list of product names that are currently out of stock.

    A product is flagged when its in_stock value is False (boolean)
    or the string "False" (as it may come from a CSV read).

    Args:
        products_rows: list of dictionaries, one per product.
        threshold: unused in this dataset (no stock-count column),
                   kept for forward compatibility.

    Returns:
        a list of product_name strings that need re-ordering.
    """
    alerts = []
    for product in products_rows:
        # in_stock may be a boolean or the string "False" from CSV reading
        in_stock_val = product.get("in_stock", True)
        if in_stock_val is False or str(in_stock_val).strip().lower() == "false":
            alerts.append(product["product_name"])
    return alerts


def monthly_sales_trend(sales_rows: list) -> dict:
    """
    Build a dictionary mapping each month (YYYY-MM) to total units sold,
    using a loop to accumulate quantities.

    Args:
        sales_rows: list of dicts; each has "sale_date" (YYYY-MM-DD)
                    and "quantity" (int).

    Returns:
        a dict like {"2026-01": 143, "2026-02": 97}
    """
    trend = {}
    for row in sales_rows:
        # Extract the first 7 characters: "YYYY-MM"
        month = row["sale_date"][:7]
        quantity = row["quantity"]
        if month in trend:
            trend[month] += quantity     # add to existing month
        else:
            trend[month] = quantity      # first sale for this month
    return trend


def classify_transaction_size(quantity: int) -> str:
    """
    Classify a single transaction by the number of units purchased.

    Rules:
        quantity >= 5  -> "Bulk"
        quantity >= 2  -> "Multiple"
        quantity == 1  -> "Single"
        anything else  -> "Invalid"

    Demonstrates a multi-branch if / elif / else chain (KM-05).
    """
    if quantity >= 5:
        return "Bulk"
    elif quantity >= 2:
        return "Multiple"
    elif quantity == 1:
        return "Single"
    else:
        return "Invalid"


def average_basket_size(sales_rows: list) -> float:
    """
    Calculate the average quantity per sale across all sales.

    Uses a loop to sum all quantities, then divides by the number
    of records. Returns 0.0 if there are no records (avoids
    division-by-zero).

    Returns:
        a float rounded to 2 decimal places.
    """
    total = 0
    for row in sales_rows:
        total += row["quantity"]    # accumulate total units

    record_count = len(sales_rows)
    if record_count == 0:
        return 0.0

    return round(total / record_count, 2)

# Task 4 complete — analysis using loops, conditionals, lists and dictionaries.
