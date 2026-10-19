"""
data_cleaning.py
-----------------
Task 2: Load the raw CSV files and clean them.

This module covers KM-04 topics: Introduction to Data (data types,
errors of omission) and Data in Spreadsheets.

The raw files in data/products.csv and data/sales.csv contain REAL
data-quality problems on purpose, so you get practice fixing them:

  products.csv issues to find and fix:
    - Some products are missing a unit_price
    - One product is missing its product_name
    - Category text is inconsistently capitalised (e.g. "beverages" vs "Beverages")
    - One exact duplicate row

  sales.csv issues to find and fix:
    - sale_date is written in at least FOUR different formats
    - Some rows have a missing sale_date (an error of omission)
    - Some rows have a missing quantity
    - Some rows have a missing payment_method
    - A few rows reference a product_id that does not exist in products.csv
    - One exact duplicate row

You must handle every one of these before the data moves on to the
database in database.py. Document the decisions you make (e.g. "rows
with a missing sale_date were dropped because we cannot analyse sales
trends without a date") in your README findings section.
"""

import pandas as pd


def load_raw_data(products_path: str, sales_path: str):
    """
    Load the two raw CSV files into pandas DataFrames.

    Args:
        products_path: file path to products.csv
        sales_path: file path to sales.csv

    Returns:
        (products_df, sales_df) tuple of pandas DataFrames, UNCLEANED.
    """
    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)
    return (products_df, sales_df)


def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":
    """
    Clean the products DataFrame.

    Cleaning decisions:
        - Rows with a missing product_name are dropped: a product with
          no name is not usable and cannot be displayed or sold.
        - Rows with a missing unit_price are dropped: without a price we
          cannot calculate revenue, which is the core of the analysis.
        - category is standardised to Title Case so "beverages" becomes
          "Beverages" — this removes grouping errors in SQL GROUP BY.
        - Exact duplicate rows (same product_id AND all other columns)
          are dropped, keeping only the first occurrence.

    Returns:
        A cleaned copy of the DataFrame. Does not modify products_df in place.
    """
    # Work on a copy so we never mutate the original
    df = products_df.copy()

    # Drop rows with a missing product_name
    df = df.dropna(subset=["product_name"])

    # Drop rows with a missing unit_price
    df = df.dropna(subset=["unit_price"])

    # Standardise category capitalisation to Title Case
    df["category"] = df["category"].str.strip().str.title()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Reset the index so it is clean and sequential
    df = df.reset_index(drop=True)

    return df


def clean_sales(sales_df: "pd.DataFrame", valid_product_ids) -> "pd.DataFrame":
    """
    Clean the sales DataFrame.

    Cleaning decisions:
        - sale_date is standardised to YYYY-MM-DD.
          All day-first formats (DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD)
          are parsed with dayfirst=True, which is correct for the South
          African locale used in this dataset.
          Ambiguous dates like 05-01-2026 are treated as 5 January 2026
          (day=05, month=01) following the dayfirst convention.
        - Rows where sale_date cannot be parsed (or is missing) are
          dropped: we cannot place them on a sales timeline without a date.
        - Rows with a missing quantity are dropped: they cannot contribute
          to revenue or trend calculations.
        - Missing payment_method is filled with "Unknown": this is honest
          and does not distort the payment-method breakdown.
        - Missing customer_type is filled with "Unknown": it is an
          optional context field and not critical to the analysis.
        - Rows whose product_id is not in valid_product_ids are dropped:
          these are data-entry errors (e.g. P099 which does not exist)
          and linking them to products would cause foreign-key violations.
        - Exact duplicate rows are dropped.

    Args:
        sales_df: the raw sales DataFrame
        valid_product_ids: collection of product_id values from the
            cleaned products table

    Returns:
        A cleaned copy of the DataFrame with sale_date as YYYY-MM-DD string.
    """
    df = sales_df.copy()

    # --- Parse dates ---
    # pandas.to_datetime with dayfirst=True handles multiple formats:
    #   YYYY-MM-DD, DD/MM/YYYY, YYYY/MM/DD, DD-MM-YYYY
    # errors="coerce" turns unparseable values into NaT (Not a Time)
    df["sale_date"] = pd.to_datetime(
        df["sale_date"],
        dayfirst=True,
        errors="coerce"
    )

    # Drop rows where date could not be parsed or was originally missing
    df = df.dropna(subset=["sale_date"])

    # Convert datetime to the standard string format YYYY-MM-DD
    df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")

    # --- Drop rows with missing quantity ---
    df = df.dropna(subset=["quantity"])

    # Ensure quantity is stored as integer
    df["quantity"] = df["quantity"].astype(int)

    # --- Fill missing payment_method with "Unknown" ---
    df["payment_method"] = df["payment_method"].fillna("Unknown")

    # --- Fill missing customer_type with "Unknown" ---
    df["customer_type"] = df["customer_type"].fillna("Unknown")

    # --- Drop rows with invalid product_id references ---
    df = df[df["product_id"].isin(valid_product_ids)]

    # --- Remove exact duplicate rows ---
    df = df.drop_duplicates()

    # Reset index
    df = df.reset_index(drop=True)

    return df


def cleaning_summary(raw_df: "pd.DataFrame", clean_df: "pd.DataFrame", name: str) -> str:
    """
    Build a short, human-readable string summarising how many rows were
    removed or changed during cleaning.

    Example output:
        "products: 16 raw rows -> 14 clean rows (2 removed)"
    """
    raw_count = len(raw_df)
    clean_count = len(clean_df)
    removed = raw_count - clean_count
    return f"{name}: {raw_count} raw rows -> {clean_count} clean rows ({removed} removed)"

# Task 2 complete — data cleaning handles all products and sales CSV issues.
