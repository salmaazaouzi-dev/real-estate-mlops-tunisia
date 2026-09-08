import pandas as pd
from sqlalchemy import create_engine
import os

# SQLite Database Setup (Zero setup required)
DB_PATH = "database/real_estate.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

def ingest_data_to_sqlite():
    csv_file = "data/processed/cleaned_real_estate.csv"
    if not os.path.exists(csv_file):
        print("[ERROR] Cleaned CSV file not found!")
        return

    df = pd.read_csv(csv_file)
    print(f"[INFO] Loaded {len(df)} records from {csv_file}")

    try:
        engine = create_engine(DATABASE_URL)
        df.to_sql("tunisia_real_estate", con=engine, if_exists="replace", index=False)
        print(f"[SUCCESS] Successfully ingested {len(df)} rows into SQLite database at '{DB_PATH}'!")

    except Exception as e:
        print(f"[ERROR] Database ingestion failed: {e}")

if __name__ == "__main__":
    ingest_data_to_sqlite()