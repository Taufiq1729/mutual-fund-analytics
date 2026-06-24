import pandas as pd

# Step 1: Load the file
df = pd.read_csv('data/raw/nav_history.csv')
print(df.head())
# Example raw data:
# amfi_code | date       | nav
# 120503    | 2023-1-5   | 45.23
# 120503    | 2023-1-6   | NaN     ← missing (weekend)
# 120503    | 2023-1-5   | 45.23   ← duplicate!
# 120503    | 2023-1-7   | -1.0    ← invalid!

# Step 2: Parse dates (convert text → real dates)
df['date'] = pd.to_datetime(df['date'], dayfirst=False, errors='coerce')
# Now "2023-1-5" becomes 2023-01-05 (proper datetime)

# Step 3: Sort by fund code + date
df = df.sort_values(['amfi_code', 'date'])

# Step 4: Forward-fill missing NAV (holiday/weekend has no trading)
# If Monday NAV = 50, Tuesday missing → fill Tuesday with 50
df['nav'] = df.groupby('amfi_code')['nav'].ffill()

# Step 5: Remove duplicates (keep first occurrence)
df = df.drop_duplicates(subset=['amfi_code', 'date'], keep='first')

# Step 6: Validate NAV > 0 (remove bad rows)
df = df[df['nav'] > 0]

# Step 7: Save cleaned file
df.to_csv('data/processed/nav_history_clean.csv', index=False)
print(f"Cleaned rows: {len(df)}")