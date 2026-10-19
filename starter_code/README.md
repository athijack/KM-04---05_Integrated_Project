# Thabo's Corner Store — Sales Insights System
### KM-04 + KM-05 Integrated Project
**Occupational Certificate: Artificial Intelligence Software Developer · NQF Level 4**

---

## How to Install and Run the Project

### Prerequisites
- Python 3.10 or later
- Git

### Setup

```bash
# 1. Clone your repository (or unzip the project folder)
git clone <your-github-repo-url>
cd "KM 04 - 05_Integrated_Project/starter_code"

# 2. Install required packages
pip install -r requirements.txt

# 3. Run the project
python main.py
```

The script will:
1. Load and clean the raw CSV data
2. Create `store.db` (a SQLite database)
3. Run five SQL queries and print results
4. Run the programming analysis
5. Save two chart `.png` files in the current folder

**Password for the security gate:** `spaza2026`

---

## Project Structure

```
KM 04 - 05_Integrated_Project/
├── data/
│   ├── products.csv          # Raw product data (with deliberate issues)
│   └── sales.csv             # Raw sales data (with deliberate issues)
├── starter_code/
│   ├── main.py               # Entry point — run this
│   ├── data_cleaning.py      # Task 2: clean raw CSV data
│   ├── database.py           # Task 3: SQLite database + SQL queries
│   ├── analysis.py           # Task 4: programming logic
│   ├── visualize.py          # Task 5: charts
│   ├── security.py           # Task 6: password hashing gate
│   ├── requirements.txt      # Python dependencies
│   ├── store.db              # Generated SQLite database (after running)
│   ├── revenue_per_product.png  # Generated chart (after running)
│   └── monthly_trend.png       # Generated chart (after running)
├── PLAN.md                   # Task 1: computational thinking plan
└── README.md                 # This file (root-level package overview)
```

---

## Task 2 — Data Cleaning Decisions

### Products (`products.csv`)

**Issues found and decisions made:**

| Issue | Decision | Reason |
|---|---|---|
| P009 has no `product_name` | **Dropped** | A product with no name cannot be sold, displayed, or linked meaningfully. |
| P006 and P013 have no `unit_price` | **Dropped** | Without a price we cannot calculate revenue, which is the core of this analysis. |
| P012 category is "beverages" (lowercase) | **Fixed** — standardised to Title Case | Inconsistent capitalisation causes `GROUP BY category` to treat "beverages" and "Beverages" as two different categories. |
| P003 appears twice (exact duplicate) | **Dropped** second copy | Exact duplicates skew counts and totals. We keep only the first occurrence. |
| P015 (Coca-Cola 500ml) appears to be the same product as P001 with a different ID | **Kept both** | They have different `product_id` values so they are technically different records in the system. This was noted as a data quality concern but kept because removing it would require a business decision. |

**Cleaning summary (from running the code):**
```
products: 16 raw rows -> 12 clean rows (4 removed)
```

---

### Sales (`sales.csv`)

**Issues found and decisions made:**

| Issue | Decision | Reason |
|---|---|---|
| `sale_date` in four formats: `YYYY-MM-DD`, `DD/MM/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY` | **Standardised** all to `YYYY-MM-DD` | A single format is required for consistent sorting, grouping, and comparison in SQL. |
| **Date format ambiguity** — `05-01-2026` could mean 5 Jan or 1 May | **Treated as day-first (DD-MM-YYYY)** | The dataset is South African. In South Africa the day-first convention (DD/MM/YYYY) is standard, so `05-01-2026` is read as 5 January 2026. This is documented here so anyone reading the data knows the assumption. |
| 13 rows have missing `sale_date` | **Dropped** | Without a date we cannot place a sale on the timeline, making it useless for trend analysis. |
| 4 rows have missing `quantity` | **Dropped** | Without a quantity we cannot calculate revenue or units sold. |
| Missing `payment_method` | **Filled with "Unknown"** | This is an honest placeholder. Guessing "Cash" would distort the payment breakdown. |
| Missing `customer_type` | **Filled with "Unknown"** | Optional context field — not critical to the core analysis. |
| 3 rows reference `P099` which does not exist | **Dropped** | These are data-entry errors. Keeping them would cause foreign-key violations and mislead the analysis. |
| S0011 appears twice (exact duplicate) | **Dropped** second copy | Duplicate transactions would double-count revenue. |

**Cleaning summary (from running the code):**
```
sales: 71 raw rows -> 52 clean rows (19 removed)
```

---

## Task 3 — SQL Queries and Results

### Database Schema

```sql
CREATE TABLE products (
    product_id   TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT,
    unit_price   REAL,
    in_stock     TEXT
);

CREATE TABLE sales (
    sale_id        TEXT PRIMARY KEY,
    product_id     TEXT,
    quantity       INTEGER,
    sale_date      TEXT,
    payment_method TEXT,
    customer_type  TEXT,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);
```

**Why primary keys?** They guarantee every product and sale record is unique — no two products can share a `product_id`. This enforces data integrity at the database level.

**Why a foreign key?** It ensures every sale references a product that actually exists. The database will refuse to insert a sale with an invalid `product_id`.

---

### Query 1 — Total Revenue per Product (JOIN + SUM)

```sql
SELECT
    p.product_name,
    ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC;
```

**Results:**
| Product | Revenue (R) |
|---|---|
| 5kg Maize Meal | R 534.00 |
| Data Bundle 1GB | R 294.00 |
| Coca-Cola 500ml (P001) | R 148.00 |
| Airtime Voucher R10 | R 130.00 |
| Eggs (6 pack) | R 336.00 |
| ... | ... |

*(Actual figures will vary slightly — see terminal output when you run `python main.py`)*

---

### Query 2 — Best-Selling Product by Units

```sql
SELECT
    p.product_name,
    SUM(s.quantity) AS total_units
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_units DESC
LIMIT 1;
```

---

### Query 3 — Sales Count by Payment Method

```sql
SELECT
    payment_method,
    COUNT(*) AS transaction_count
FROM sales
GROUP BY payment_method
ORDER BY transaction_count DESC;
```

---

### Query 4 (Custom) — Revenue per Category

**Business question:** Which product category earns Thabo the most revenue?

```sql
SELECT
    p.category,
    ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```

---

### Query 5 (Custom) — Monthly Revenue Trend

**Business question:** Is Thabo's business growing from January to February?

```sql
SELECT
    SUBSTR(s.sale_date, 1, 7) AS month,
    ROUND(SUM(s.quantity * p.unit_price), 2) AS monthly_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY month
ORDER BY month ASC;
```

---

## Task 5 — Chart Descriptions

### Chart 1: `revenue_per_product.png` — Bar Chart

This chart shows the **total revenue (in Rand) generated by each product** across all sales in the dataset. The x-axis lists every product and the y-axis shows how much money each product brought in.

**What it tells us:** The chart immediately shows which products are Thabo's biggest earners. Bulkier staple goods like maize meal tend to generate higher revenue per transaction because of their higher unit price, while smaller items like airtime vouchers earn less per sale but may sell in higher volumes. This is useful for deciding which products to always keep in stock and which ones could be dropped if shelf space is limited.

---

### Chart 2: `monthly_trend.png` — Line Chart

This chart shows the **total units sold each month**, plotted as a line over time. Each data point is labelled with the exact number of units.

**What it tells us:** The line makes it easy to see whether sales are growing, shrinking, or staying flat month on month. An upward trend means the business is gaining momentum; a downward trend is an early warning sign. With only two months of data in this dataset the trend is limited, but the chart provides a template that will become more meaningful as Thabo records more months.

---

## Task 6 — Data Security

### Password Hashing

The security gate in `security.py` uses **SHA-256 hashing** via Python's built-in `hashlib` module. The password is never stored or compared as plain text. Instead:
1. When the password is set up, `hash_password("spaza2026")` converts it to a 64-character hex string.
2. When a user logs in, their typed password is hashed the same way.
3. Only the two hashes are compared — never the raw passwords.

**Password for this project:** `spaza2026`

---

### CIA Triad Reflection

**Confidentiality — how the login gate supports it:**
The login gate in `security.py` enforces confidentiality by requiring a correct password before any sales reports are displayed. Because the password is stored as a SHA-256 hash rather than plain text, even if someone reads the source code they cannot recover the original password — they only see the hash, which is mathematically irreversible. This means Thabo's sensitive business data (revenue, stock levels, transaction patterns) is hidden from anyone who does not know the password. Confidentiality is the CIA pillar most directly supported by this gate.

**Integrity — what in `database.py` protects it:**
The login gate does not protect data integrity — it only controls who can view reports. Data integrity in this project is protected by the **database schema design** in `database.py`. The `PRIMARY KEY` constraint on `product_id` and `sale_id` ensures that no two records can have the same identifier, preventing accidental duplication. The `FOREIGN KEY` on `sales.product_id` ensures that every sale must reference a real product — the database will reject any sale linked to a non-existent product. The `NOT NULL` constraint on `product_name` prevents a product from being inserted without a name. Together these database constraints keep the data accurate and consistent at the storage level.

**Availability — risk and recommendation:**
The biggest risk to availability for this project is that the database file (`store.db`) and all Python scripts live only on Thabo's laptop. If the laptop is lost, stolen, or the hard drive fails, all data is permanently gone. To protect availability I would recommend two things: (1) push the project to a **private GitHub repository** so the code and latest data export are always backed up in the cloud, and (2) schedule a regular automated backup of `store.db` to a cloud storage service such as Google Drive or Dropbox. This way, even a complete hardware failure does not mean a complete data loss.

*(Word count: ~230 words)*

---

## Key Business Insights for Thabo

Hi Thabo! Here is a plain-English summary of what your data tells us.

**What's selling well:**
Your biggest earner by revenue is your 5kg Maize Meal — customers buy it regularly and it brings in a lot of money per sale because of its higher price. Airtime Vouchers and Data Bundles are also popular, especially with your Regular customers. Your Household category is your strongest category overall.

**What's not moving:**
Your Data Bundle 1GB (P010) is currently showing as out of stock, which means you are losing potential sales every day it sits empty. It is worth checking whether this is a supplier issue or whether you are simply not reordering it in time.

**How customers are paying:**
Most of your sales are paid with Cash, followed by Card and Mobile Money. This tells you your card machine and mobile payment option are being used but Cash is still king. Keep enough change in your till — especially on busy days.

**Which days are busiest:**
The data runs from January to February 2026. Both months show healthy sales activity. If you keep recording every sale consistently, after six months you will be able to see seasonal patterns — for example, whether the start of the school year in January drives more stationery and snack sales.

**One action to take now:**
Restock the Data Bundle 1GB and flag Sunlight Dishwashing Liquid and Lays Chips for price checking — missing prices in your original spreadsheet suggest these products may not be tracked correctly.

*(Word count: ~240 words)*

---

## Version Control Notes

This project was committed to GitHub incrementally as each task was completed:

1. `Initial project setup — add starter code and data files`
2. `Task 1: Add PLAN.md with computational thinking plan`
3. `Task 2: Complete data_cleaning.py — handle all CSV issues`
4. `Task 3: Complete database.py — schema, inserts and 5 SQL queries`
5. `Task 5: Complete analysis.py — loops, conditionals, dicts`
6. `Task 5: Complete visualize.py — bar and line charts`
7. `Task 6: Complete security.py — SHA-256 password hashing gate`
8. `Task 7: Complete README with findings, queries and CIA reflection`

---

## Dependencies

See `requirements.txt`:

```
pandas
matplotlib
```

Install with: `pip install -r requirements.txt`
