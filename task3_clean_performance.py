import pandas as pd
import numpy as np

df = pd.read_csv('data/raw/scheme_performance.csv')

# Example raw data:
# amfi_code | return_1yr | return_3yr | return_5yr | expense_ratio
# 120503    | "12.5%"    | 34.2       | N/A        | 1.5
# 120504    | 500        | -200       | 45.0       | 3.5   ← expense too high!
# 120505    | "na"       | 22.1       | 30.0       | 0.05  ← expense too low!

# Step 1: Clean return columns (remove % signs, convert to float)
return_cols = ['return_1yr', 'return_3yr', 'return_5yr']

for col in return_cols:
    df[col] = df[col].astype(str)
    df[col] = df[col].str.replace('%', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')  # "N/A","na" → NaN

# Step 2: Flag anomalies (returns > 100% or < -50% are suspicious)
for col in return_cols:
    anomaly_col = f'{col}_anomaly'
    df[anomaly_col] = (df[col] > 100) | (df[col] < -50)
    count = df[anomaly_col].sum()
    print(f"Anomalies in {col}: {count} rows")
    # You can choose to remove or just flag them

# Step 3: Validate expense_ratio range (0.1 to 2.5)
df['expense_ratio'] = pd.to_numeric(df['expense_ratio'], errors='coerce')
df['expense_ratio_valid'] = df['expense_ratio'].between(0.1, 2.5)

# Flag invalid ones (don't delete — just mark)
invalid_expense = df[~df['expense_ratio_valid']]
print(f"Invalid expense ratios: {len(invalid_expense)} rows")

df.to_csv('data/processed/scheme_performance_clean.csv', index=False)