from sqlalchemy import create_engine

def save_to_db(df):
    engine = create_engine("sqlite:///database/wsn.db")
    df.to_sql("network_data", engine, if_exists="replace", index=False)