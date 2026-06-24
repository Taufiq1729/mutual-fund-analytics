import pandas as pd

# Load the file
df = pd.read_csv("data/raw/loan.csv")

# Inspect the file's structure
print("--- Dataset Profile ---")
print("Shape (Rows, Columns):", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nFirst 5 Rows:\n", df.head())