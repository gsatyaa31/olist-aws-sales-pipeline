import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

#connecting to the rds
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")

# reading the 4 curated tables
daily_sales = pd.read_parquet("curated_local/daily_sales.parquet")
top_products = pd.read_parquet("curated_local/top_products.parquet")
top_customers = pd.read_parquet("curated_local/top_customers.parquet")
monthly_state_revenue = pd.read_parquet("curated_local/monthly_state_revenue.parquet")

#loading them to the rds
daily_sales.to_sql("daily_sales", engine, if_exists="replace", index=False)
top_products.to_sql("top_products", engine, if_exists="replace", index=False)
top_customers.to_sql("top_customers", engine, if_exists="replace", index=False)
monthly_state_revenue.to_sql("monthly_state_revenue", engine, if_exists="replace", index=False)

#check the row counts
for table in ["daily_sales", "top_products", "top_customers", "monthly_state_revenue"]:
    count = pd.read_sql(f"SELECT COUNT(*) AS n FROM {table}", engine)
    print(table, count["n"][0], "rows")

print("Loaded into RDS!")
