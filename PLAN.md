# PLAN.md — Computational Thinking Plan
## Thabo's Corner Store — Sales Insights System

---

## 1. Decomposition — Breaking the Problem Into Sub-Problems

The project can be broken into five clear sub-problems, each matching a starter code module:

| # | Sub-Problem | Module |
|---|---|---|
| 1 | Load and clean raw messy data | `data_cleaning.py` |
| 2 | Design and populate a relational database | `database.py` |
| 3 | Analyse the data with Python logic | `analysis.py` |
| 4 | Visualise findings as charts | `visualize.py` |
| 5 | Secure the reports behind a password | `security.py` |

---

## 2. Pattern Recognition — What I Expect to Find Messy

**In products.csv:**
- Missing `unit_price` on at least 2 rows — I will drop these rows since we cannot calculate revenue without a price.
- One row with no `product_name` — unusable, will be dropped.
- Inconsistent capitalisation in `category` (e.g. "beverages" vs "Beverages") — will standardise to Title Case.
- At least one exact duplicate row (P003 appears twice) — will drop duplicates.
- P015 (Coca-Cola 500ml) appears to be a duplicate of P001 with a different product_id — will keep both but flag it.

**In sales.csv:**
- `sale_date` in at least four formats: `YYYY-MM-DD`, `DD/MM/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY` — will parse all and standardise to `YYYY-MM-DD`.
- Ambiguous dates like `05-01-2026` could mean 5 Jan or 1 May. I will treat all `DD-MM-YYYY` and `DD/MM/YYYY` patterns as day-first (DD) since the dataset is South African and this is the local convention.
- Rows with missing `sale_date` — will drop them as we cannot place them on a timeline.
- Rows with missing `quantity` — will drop them as we cannot calculate revenue or trend.
- Rows referencing `P099` which does not exist in products — will drop these as orphaned records.
- One exact duplicate row (S0011) — will drop it.
- Missing `payment_method` — will fill with "Unknown" (honest, doesn't distort analysis).
- Missing `customer_type` — will fill with "Unknown".

---

## 3. Abstraction — What to Focus On, What to Ignore

- **Focus on:** data quality, correct schema design, working queries, clear charts, a functioning security gate.
- **Ignore / defer:** advanced ML analysis, multi-user authentication, a web UI — none of these are in scope.
- **Abstract away:** the details of how SQLite stores data internally; we use Python's `sqlite3` module as the abstraction layer.

---

## 4. Algorithm — Order of Implementation

I will tackle the modules in the natural data-flow order, since each depends on the one before it:

```
Step 1: data_cleaning.py  → produces clean DataFrames
Step 2: database.py       → stores clean data, runs SQL queries
Step 3: analysis.py       → programmatic analysis using loops/dicts
Step 4: visualize.py      → charts from analysis results
Step 5: security.py       → password gate wrapping the whole output
Step 6: README.md         → document all decisions and findings
```

**Rough algorithm for data_cleaning:**
```
load CSV files
for products:
    drop rows with missing product_name
    drop rows with missing unit_price
    standardise category to Title Case
    remove duplicate rows
for sales:
    parse all date formats → YYYY-MM-DD
    drop rows with unparseable or missing dates
    drop rows with missing quantity
    fill missing payment_method with "Unknown"
    fill missing customer_type with "Unknown"
    drop rows where product_id is not in the cleaned products list
    remove duplicate rows
```

---

## 5. Expected Outcome

- A clean `store.db` SQLite database with 2 related tables.
- 5+ working SQL queries including a JOIN and aggregations.
- 2 chart `.png` files showing revenue and monthly trend.
- A password-protected report gate using SHA-256 hashing.
- A fully documented README with business insights for Thabo.
