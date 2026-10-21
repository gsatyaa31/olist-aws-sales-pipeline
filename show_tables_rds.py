import os 
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")

print(pd.read_sql("SHOW TABLES", engine))
print(pd.read_sql("SELECT * FROM daily_sales LIMIT 5", engine))
print(pd.read_sql("SELECT * FROM top_products LIMIT 5", engine))