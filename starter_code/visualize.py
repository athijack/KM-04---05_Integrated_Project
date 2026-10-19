"""
visualize.py
-------------
Task 5: Turn your analysis into charts.

This module covers KM-04 KT07: Visualising Data with AI-assisted tools.
We use matplotlib to produce two required charts:
  1. A bar chart of total revenue per product
  2. A line chart of monthly sales trend (units sold per month)

Both charts are saved as .png files for submission evidence.
"""

import matplotlib.pyplot as plt


def bar_chart_revenue_per_product(
    product_names: list,
    revenues: list,
    save_path: str = "revenue_per_product.png"
):
    """
    Create and save a bar chart of total revenue per product.

    Args:
        product_names: list of product name strings (x-axis labels)
        revenues: list of revenue totals (Rand), same order as product_names
        save_path: file path to save the .png chart
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Use a colour gradient so bars are visually distinct
    bars = ax.bar(product_names, revenues, color="steelblue", edgecolor="white")

    # Add value labels on top of each bar
    for bar, revenue in zip(bars, revenues):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            f"R{revenue:,.0f}",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=45
        )

    ax.set_xlabel("Product", fontsize=11)
    ax.set_ylabel("Total Revenue (Rand)", fontsize=11)
    ax.set_title("Total Revenue per Product — Thabo's Corner Store", fontsize=13, fontweight="bold")

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Bar chart saved to: {save_path}")


def line_chart_monthly_trend(
    monthly_trend: dict,
    save_path: str = "monthly_trend.png"
):
    """
    Create and save a line chart of total units sold per month.

    Args:
        monthly_trend: dict mapping "YYYY-MM" -> total units sold
                       (the output of analysis.monthly_sales_trend())
        save_path: file path to save the .png chart
    """
    # Sort months chronologically so the line reads left-to-right in time
    sorted_months = sorted(monthly_trend.keys())
    totals = [monthly_trend[m] for m in sorted_months]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(sorted_months, totals, marker="o", linewidth=2,
            color="darkorange", markersize=8, markerfacecolor="white",
            markeredgecolor="darkorange", markeredgewidth=2)

    # Annotate each data point with its value
    for month, total in zip(sorted_months, totals):
        ax.annotate(
            str(total),
            xy=(month, total),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=10
        )

    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Total Units Sold", fontsize=11)
    ax.set_title("Monthly Sales Trend — Thabo's Corner Store", fontsize=13, fontweight="bold")

    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Line chart saved to: {save_path}")
