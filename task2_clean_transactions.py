import pandas as pd

df = pd.read_csv('data/raw/investor_transactions.csv')

# Example raw data:
# investor_id | date      | transaction_type | amount | kyc_status
# INV001      | 05/01/23  | sip              | 5000   | verified       ← bad format
# INV002      | 2023-01-06| LUMPSUM          | -100   | KYC_VERIFIED   ← negative!
# INV003      | 2023-01-07| Redemption       | 0      | pending        ← zero amount!

# Step 1: Fix date formats
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

# Step 2: Standardise transaction_type
# Make everything lowercase first, then map to standard names
df['transaction_type'] = df['transaction_type'].str.strip().str.lower()

type_map = {
    'sip': 'SIP',
    'lumpsum': 'Lumpsum',
    'lump sum': 'Lumpsum',
    'lump_sum': 'Lumpsum',
    'redemption': 'Redemption',
    'redeem': 'Redemption',
    'withdrawal': 'Redemption'
}
df['transaction_type'] = df['transaction_type'].map(type_map)

# Step 3: Validate amount > 0
df = df[df['amount'] > 0]

# Step 4: Fix KYC status
df['kyc_status'] = df['kyc_status'].str.strip().str.upper()

kyc_map = {
    'VERIFIED': 'KYC_VERIFIED',
    'KYC_VERIFIED': 'KYC_VERIFIED',
    'PENDING': 'KYC_PENDING',
    'KYC_PENDING': 'KYC_PENDING',
    'REJECTED': 'KYC_REJECTED',
    'KYC_REJECTED': 'KYC_REJECTED'
}
df['kyc_status'] = df['kyc_status'].map(kyc_map)

# Step 5: Drop rows with unmapped/invalid values
df = df.dropna(subset=['transaction_type', 'kyc_status'])

df.to_csv('data/processed/investor_transactions_clean.csv', index=False)
print(f"Cleaned rows: {len(df)}")