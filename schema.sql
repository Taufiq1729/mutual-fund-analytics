-- schema.sql

-- ============================================
-- DIMENSION TABLES (reference/lookup tables)
-- ============================================

-- dim_fund: One row per mutual fund
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code     TEXT NOT NULL UNIQUE,   -- Official AMFI fund code (e.g., "120503")
    scheme_name   TEXT NOT NULL,           -- "HDFC Top 100 Fund"
    fund_house    TEXT,                    -- "HDFC Mutual Fund"
    category      TEXT,                    -- "Large Cap", "Debt", "Hybrid"
    sub_category  TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- dim_date: One row per calendar date (pre-populated)
CREATE TABLE IF NOT EXISTS dim_date (
    date_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date     DATE NOT NULL UNIQUE,    -- 2023-01-05
    day           INTEGER,                 -- 5
    month         INTEGER,                 -- 1
    year          INTEGER,                 -- 2023
    quarter       INTEGER,                 -- 1 (Jan-Mar)
    day_of_week   TEXT,                    -- "Thursday"
    is_weekend    BOOLEAN,                 -- 0 or 1
    is_holiday    BOOLEAN                  -- 0 or 1
);

-- ============================================
-- FACT TABLES (actual data/measurements)
-- ============================================

-- fact_nav: Daily NAV prices
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code     TEXT NOT NULL,
    date          DATE NOT NULL,
    nav           REAL NOT NULL CHECK(nav > 0),  -- price per unit
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date) REFERENCES dim_date(full_date),
    UNIQUE(amfi_code, date)  -- no duplicate NAV for same fund+date
);

-- fact_transactions: Investor buy/sell records
CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id       TEXT NOT NULL,
    amfi_code         TEXT NOT NULL,
    date              DATE NOT NULL,
    transaction_type  TEXT CHECK(transaction_type IN ('SIP','Lumpsum','Redemption')),
    amount            REAL CHECK(amount > 0),
    units             REAL,
    nav_at_txn        REAL,
    kyc_status        TEXT CHECK(kyc_status IN ('KYC_VERIFIED','KYC_PENDING','KYC_REJECTED')),
    state             TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- fact_performance: Fund returns data
CREATE TABLE IF NOT EXISTS fact_performance (
    perf_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code      TEXT NOT NULL,
    as_of_date     DATE,
    return_1yr     REAL,
    return_3yr     REAL,
    return_5yr     REAL,
    expense_ratio  REAL CHECK(expense_ratio BETWEEN 0.1 AND 2.5),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- fact_aum: Assets Under Management (total money managed)
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code   TEXT NOT NULL,
    date        DATE NOT NULL,
    aum_crores  REAL CHECK(aum_crores >= 0),  -- in crore rupees
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);