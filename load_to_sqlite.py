# load_to_sqlite.py
import pandas as pd
from sqlalchemy import create_engine, text

# Create SQLite database file
engine = create_engine('sqlite:///bluestock_mf.db', echo=False)

# ---- Load each cleaned CSV ----

files = {
    'fact_nav':           'data/processed/nav_history_clean.csv',
    'fact_transactions':  'data/processed/investor_transactions_clean.csv',
    'fact_performance':   'data/processed/scheme_performance_clean.csv',
    # add aum, dim_fund, dim_date similarly
}

for table_name, filepath in files.items():
    df = pd.read_csv(filepath)
    
    # Load into SQLite (replace table if exists)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
    # Verify row count
    with engine.connect() as conn:
        db_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
    
    print(f"✅ {table_name}: CSV={len(df)} rows | DB={db_count} rows | Match={len(df)==db_count}")

# Example output:
# ✅ fact_nav: CSV=15234 rows | DB=15234 rows | Match=True
# ✅ fact_transactions: CSV=8901 rows | DB=8901 rows | Match=True