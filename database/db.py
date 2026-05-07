from sqlalchemy import create_engine, text
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wsn.db")

def save_to_db(df):
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df.to_sql("network_data", engine, if_exists="replace", index=False)
    print(f"  Saved {len(df)} rows to database.")

def load_from_db():
    import pandas as pd
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM network_data", conn)
    return df
