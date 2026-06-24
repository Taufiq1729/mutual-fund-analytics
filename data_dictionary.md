# data_dictionary.md

# 📚 Bluestock Mutual Fund – Data Dictionary

## Table: fact_nav
| Column     | Data Type | Description                          | Example       | Source          |
|------------|-----------|--------------------------------------|---------------|-----------------|
| nav_id     | INTEGER   | Auto-generated primary key           | 1, 2, 3       | System          |
| amfi_code  | TEXT      | Unique fund identifier (AMFI)        | "120503"      | nav_history.csv |
| date       | DATE      | Trading date (no weekends/holidays)  | 2023-01-05    | nav_history.csv |
| nav        | REAL      | Net Asset Value per unit in ₹        | 45.23         | nav_history.csv |

**Business Rule:** NAV must be > 0. Missing weekend/holiday NAVs are forward-filled from last trading day.

---

## Table: fact_transactions
| Column           | Data Type | Description                              | Example          |
|------------------|-----------|------------------------------------------|------------------|
| txn_id           | INTEGER   | Auto-generated primary key               | 1001             |
| investor_id      | TEXT      | Unique investor identifier               | "INV001"         |
| amfi_code        | TEXT      | Fund invested in                         | "120503"         |
| date             | DATE      | Transaction date                         | 2023-01-05       |
| transaction_type | TEXT      | Type: SIP / Lumpsum / Redemption         | "SIP"            |
| amount           | REAL      | Amount in ₹                              | 5000.00          |
| units            | REAL      | Units bought/sold                        | 110.5            |
| nav_at_txn       | REAL      | NAV on transaction date                  | 45.23            |
| kyc_status       | TEXT      | KYC_VERIFIED / KYC_PENDING / KYC_REJECTED| "KYC_VERIFIED"  |
| state            | TEXT      | Investor's state                         | "Maharashtra"    |

---

## Table: fact_performance
| Column        | Data Type | Description                          | Valid Range      |
|---------------|-----------|--------------------------------------|------------------|
| return_1yr    | REAL      | 1-year return in %                   | -50% to 100%     |
| return_3yr    | REAL      | 3-year return in %                   | -50% to 100%     |
| return_5yr    | REAL      | 5-year return in %                   | -50% to 100%     |
| expense_ratio | REAL      | Annual fee charged by fund in %      | 0.1% to 2.5%     |

---

## Table: dim_fund
| Column      | Data Type | Description                    | Example              |
|-------------|-----------|--------------------------------|----------------------|
| amfi_code   | TEXT      | Primary key – AMFI fund code   | "120503"             |
| scheme_name | TEXT      | Full fund name                 | "HDFC Top 100 Fund"  |
| fund_house  | TEXT      | Asset Management Company       | "HDFC AMC"           |
| category    | TEXT      | SEBI category                  | "Large Cap"          |