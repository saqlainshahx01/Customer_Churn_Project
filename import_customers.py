import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://saqlain:shah001@localhost/customer_churn"

engine = create_engine(DATABASE_URL)

# Read CSV
df = pd.read_csv("customers_for_db.csv")

# Fix customer_id
df["customer_id"] = (
    df["customer_id"]
    .astype(str)
    .str.replace(r"\.0$", "", regex=True)
)

# Insert into MySQL
df.to_sql(
    "customers",
    con=engine,
    if_exists="append",
    index=False
)

print(f"Successfully inserted {len(df)} customers.")
