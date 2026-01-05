# SalesStream – Python Data Analysis

A data engineering project that transforms raw CSV data into actionable business insights using the Pandas "Split-Apply-Combine" logic.

## 📊 Business Insights Generated
- **Total Revenue:** Calculated the gross turnover ($₹12,365,048.00$).
- **Top Product:** Identified **Laptops** as the primary revenue driver.
- **Regional Performance:** Mapped sales across North, South, East, and West territories.

## 🛠️ Tech Stack
- **Library:** Pandas (DataFrames, Series)
- **Visualization:** Matplotlib (Bar, Pie, and Line charts)
- **Data Source:** CSV (100+ Transaction Records)

## Data Cleaning Process
- Removed duplicates using `drop_duplicates()`.
- Handled missing values via `dropna()`.
- Validated schemas using `df.head()` and `df.info()`.
