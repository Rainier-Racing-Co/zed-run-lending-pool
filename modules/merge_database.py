import pandas as pd

# Load the token IDs you queried into a DataFrame
lending_pool = pd.read_csv("data/lending_barn.csv")

# Load the other CSV file containing all token data into a DataFrame
horse_db = pd.read_csv("data/horse_db.csv")

# Merge the two DataFrames on the token ID column
merged_df = pd.merge(lending_pool, horse_db, on='horse_id')

# Show the resulting DataFrame
print(merged_df.head())

# Save to CSV
merged_df.to_csv('data/horse_in_public_lending_pool.csv')
