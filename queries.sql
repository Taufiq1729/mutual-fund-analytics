-- queries.sql

-- Query 1: Top 5 funds by AUM (biggest funds by money managed)
SELECT 
    f.scheme_name,
    f.fund_house,
    SUM(a.aum_crores) AS total_aum
FROM fact_aum a
JOIN dim_fund f ON a.amfi_code = f.amfi_code
GROUP BY a.amfi_code
ORDER BY total_aum DESC
LIMIT 5;
-- Example result: HDFC Flexi Cap → ₹45,000 Cr


-- Query 2: Average NAV per month (how prices moved month by month)
SELECT 
    strftime('%Y-%m', date) AS month,
    amfi_code,
    ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month, amfi_code
ORDER BY month;


-- Query 3: SIP Year-over-Year growth (are more people doing SIPs each year?)
SELECT 
    strftime('%Y', date) AS year,
    COUNT(*) AS sip_count,
    SUM(amount) AS total_sip_amount,
    ROUND(
        (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY strftime('%Y', date))) 
        / LAG(SUM(amount)) OVER (ORDER BY strftime('%Y', date)) * 100, 2
    ) AS yoy_growth_pct
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year;


-- Query 4: Transactions by state (which states invest most?)
SELECT 
    state,
    COUNT(*) AS txn_count,
    ROUND(SUM(amount)/1e7, 2) AS amount_crores
FROM fact_transactions
GROUP BY state
ORDER BY txn_count DESC;


-- Query 5: Funds with expense_ratio < 1% (cheapest funds)
SELECT 
    f.scheme_name,
    f.category,
    p.expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;


-- Query 6: Best performing funds (highest 1-year return)
SELECT 
    f.scheme_name,
    p.return_1yr,
    p.return_3yr,
    p.return_5yr
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_1yr IS NOT NULL
ORDER BY p.return_1yr DESC
LIMIT 10;


-- Query 7: Monthly SIP amount trend (is SIP investing growing?)
SELECT 
    strftime('%Y-%m', date) AS month,
    COUNT(*) AS sip_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY month
ORDER BY month;


-- Query 8: KYC status distribution (compliance check)
SELECT 
    kyc_status,
    COUNT(*) AS investor_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_transactions), 2) AS percentage
FROM fact_transactions
GROUP BY kyc_status;


-- Query 9: Funds with consistent high returns (good across all periods)
SELECT 
    f.scheme_name,
    p.return_1yr,
    p.return_3yr,
    p.return_5yr,
    ROUND((p.return_1yr + p.return_3yr + p.return_5yr) / 3, 2) AS avg_return
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_1yr > 10 
  AND p.return_3yr > 10 
  AND p.return_5yr > 10
ORDER BY avg_return DESC;


-- Query 10: Redemption vs Purchase ratio by fund (are people leaving a fund?)
SELECT 
    f.scheme_name,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount ELSE 0 END) AS total_redemption,
    SUM(CASE WHEN t.transaction_type IN ('SIP','Lumpsum') THEN t.amount ELSE 0 END) AS total_purchase,
    ROUND(
        SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount ELSE 0 END) * 100.0 /
        NULLIF(SUM(CASE WHEN t.transaction_type IN ('SIP','Lumpsum') THEN t.amount ELSE 0 END), 0)
    , 2) AS redemption_ratio_pct
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY t.amfi_code
ORDER BY redemption_ratio_pct DESC;
