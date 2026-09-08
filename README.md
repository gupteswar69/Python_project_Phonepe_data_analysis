# Python_project_Phonepe_data_analysis
Data Cleaning and Preprocessing, Exploratory Data Analysis (EDA), Data Visualization on a dataset of phonepe transactions.
# PhonePe Pulse Data Analysis & Insights (Q1 2018 - Q2 2021)

A comprehensive Python data analysis project built to explore, aggregate, and visualize Indian digital payment trends, user demographics, and device usage using data from PhonePe Pulse.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset Structure](#dataset-structure)
- [Key Features & Analysis](#key-features--analysis)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Key Insights & Visualizations](#key-insights--visualizations)
- [Project Structure](#project-structure)
- [License](#license)

---

## Project Overview

This project analyzes PhonePe transaction data across Indian states and districts from Q1 2018 to Q2 2021. By parsing transaction counts, user registration numbers, payment categories, device brand distributions, and district-level demographic metrics, the script uncovers digital payment adoption trends across India.

---

## Dataset Structure

The analysis uses `phonepe-raw-data.xlsx` containing the following core sheets:

| Sheet Name | Description | Key Fields |
| :--- | :--- | :--- |
| `State_Txn and Users` | State-level transaction totals and app usage | `State`, `Year`, `Quarter`, `Transactions`, `Amount (INR)`, `Registered Users`, `App Opens` |
| `State_TxnSplit` | Breakdown of transactions by payment type | `State`, `Year`, `Quarter`, `Transaction Type`, `Transactions`, `Amount (INR)` |
| `State_DeviceData` | Mobile brand distribution per state | `State`, `Year`, `Quarter`, `Brand`, `Registered Users` |
| `District_Txn and Users` | District-level transaction totals | `State`, `District`, `Code`, `Year`, `Quarter`, `Transactions`, `Amount (INR)` |
| `District Demographics` | Population metrics for geographic correlation | `State`, `District`, `Population`, `Area`, `Density` |

---

## Key Features & Analysis

1. **Data Audit & Cleaning:**
   - Automated missing value inspection and statistical summary generation across all sheets.
   - Cross-validation between aggregated district-level totals and state-level metrics to detect data discrepancies.

2. **Transaction & User Trends:**
   - Aggregated transaction volumes and total values ($INR$) across Indian states.
   - Average Transaction Value (ATV) per state and overall user-to-population ratios.
   - Time-series tracking of app opens and payment volume growth.

3. **Breakdown & Demographic Studies:**
   - Dominant payment categories (Peer-to-peer, Merchant payments, Recharge & Bills, etc.) over time.
   - Device brand adoption ratios across states.
   - Correlation analysis between district population density and digital transaction volume.

4. **Automated Exports:**
   - Unique district-to-code mapping extraction exported to `district_code_mapping.csv`.

---

## Installation & Setup

### Prerequisites
- **Python:** `3.8+`
- **Excel File:** Place `phonepe-raw-data.xlsx` inside your project directory (or adjust the path inside `phonepe_project.py`).

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/phonepe-data-analysis.git](https://github.com/your-username/phonepe-data-analysis.git)
   cd phonepe-data-analysis
