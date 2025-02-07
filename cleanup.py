import pandas as pd

# Load CSV file
df = pd.read_csv('./authors_publis.csv', delimiter=';', dtype=str)

# Convert integer columns properly
int_columns = ['year', 'pages_start', 'pages_end', 'journal_volume', 'pos']
for col in int_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# Save cleaned data
df.to_csv('./authors_publis_cleaned.csv', index=False, sep=';')
